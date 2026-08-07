"""Runtime and persistence for Smart Entity Timer."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from contextlib import suppress
from datetime import UTC, datetime, timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, State, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.event import (
    async_track_point_in_utc_time,
    async_track_state_change_event,
    async_track_time_interval,
)
from homeassistant.helpers.start import async_at_started
from homeassistant.helpers.storage import Store
from homeassistant.helpers import entity_registry as er

from .const import (
    ACTION_TURN_OFF,
    ACTION_TURN_ON,
    ACTIONS,
    CARD_API_VERSION,
    CONF_CONFIRMATION_TIMEOUT,
    CONF_DEFAULT_ACTION,
    CONF_DEFAULT_DURATION_MINUTES,
    CONF_EXECUTE_EXPIRED_TURN_OFF,
    CONF_EXECUTE_EXPIRED_TURN_ON,
    CONF_MAX_DURATION_MINUTES,
    CONF_NOTIFICATION_TARGET,
    CONF_NOTIFY_AUTO_CANCEL,
    CONF_NOTIFY_MANUAL_CANCEL,
    DEFAULT_ACTION,
    DEFAULT_CONFIRMATION_TIMEOUT,
    DEFAULT_DURATION_MINUTES,
    DEFAULT_EXECUTE_EXPIRED_TURN_OFF,
    DEFAULT_EXECUTE_EXPIRED_TURN_ON,
    DEFAULT_MAX_DURATION_MINUTES,
    DEFAULT_NOTIFY_AUTO_CANCEL,
    DEFAULT_NOTIFY_MANUAL_CANCEL,
    DOMAIN,
    REASON_ACTION_FAILED,
    REASON_ALREADY_TARGET,
    REASON_CONFIRMATION_TIMEOUT,
    REASON_EXPIRED_DURING_RESTART,
    REASON_MANUAL_CANCEL,
    REASON_TARGET_REACHED,
    REASON_TARGET_UNAVAILABLE,
    REASON_RESTORE_TARGET_UNAVAILABLE,
    RESULT_AUTO_CANCELLED,
    RESULT_CANCELLED,
    RESULT_COMPLETED,
    RESULT_ERROR,
    RESULT_SKIPPED,
    STATUS_ACTIVE,
    STATUS_ERROR,
    STATUS_EXECUTING,
    STATUS_IDLE,
    STORAGE_KEY,
    STORAGE_VERSION,
    VERSION,
    WATCHDOG_INTERVAL_SECONDS,
    RESTORE_TARGET_WAIT_SECONDS,
)
from .logic import format_duration, is_state_usable, target_state_reached

_LOGGER = logging.getLogger(__name__)

UpdateCallback = Callable[[], None]


class SmartEntityTimerRuntime:
    """Own one persistent timer associated with one Home Assistant entity."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._store: Store[dict[str, Any]] = Store(
            hass,
            STORAGE_VERSION,
            STORAGE_KEY.format(entry_id=entry.entry_id),
        )
        self._lock = asyncio.Lock()
        self._listeners: set[UpdateCallback] = set()
        self._finish_unsub: Callable[[], None] | None = None
        self._target_unsub: Callable[[], None] | None = None
        self._watchdog_unsub: Callable[[], None] | None = None
        self._startup_unsub: Callable[[], None] | None = None
        self._restore_task: asyncio.Task[None] | None = None
        self._target_available_event = asyncio.Event()
        self._target_check_pending = False
        self._restore_pending = False

        self.status = STATUS_IDLE
        self.selected_action = self.default_action
        self.selected_duration_minutes = self.default_duration_minutes
        self.started_at: datetime | None = None
        self.finishes_at: datetime | None = None
        self.last_result: str | None = None
        self.last_reason: str | None = None
        self.last_message: str | None = None
        self.last_finished_at: datetime | None = None

    @property
    def _effective(self) -> dict[str, Any]:
        """Return config data with options taking precedence."""
        return {**self.entry.data, **self.entry.options}

    @property
    def target_entity_id(self) -> str:
        return str(self._effective["target_entity"])

    @property
    def default_action(self) -> str:
        return str(self._effective.get(CONF_DEFAULT_ACTION, DEFAULT_ACTION))

    @property
    def default_duration_minutes(self) -> int:
        return int(
            self._effective.get(
                CONF_DEFAULT_DURATION_MINUTES,
                DEFAULT_DURATION_MINUTES,
            )
        )

    @property
    def max_duration_minutes(self) -> int:
        return int(
            self._effective.get(
                CONF_MAX_DURATION_MINUTES,
                DEFAULT_MAX_DURATION_MINUTES,
            )
        )

    @property
    def notification_target(self) -> dict[str, Any]:
        value = self._effective.get(CONF_NOTIFICATION_TARGET, {})
        return dict(value) if isinstance(value, dict) else {}

    @property
    def confirmation_timeout(self) -> int:
        return int(
            self._effective.get(
                CONF_CONFIRMATION_TIMEOUT,
                DEFAULT_CONFIRMATION_TIMEOUT,
            )
        )

    @property
    def is_active(self) -> bool:
        return self.status == STATUS_ACTIVE

    @property
    def is_busy(self) -> bool:
        return self.status in (STATUS_ACTIVE, STATUS_EXECUTING)

    @property
    def remaining_seconds(self) -> int:
        if not self.is_active or self.finishes_at is None:
            return 0
        return max(0, int((self.finishes_at - datetime.now(UTC)).total_seconds()))

    @property
    def current_target_state_reached(self) -> bool:
        return target_state_reached(
            self.target_entity_id,
            self.hass.states.get(self.target_entity_id),
            self.selected_action,
        )

    @property
    def can_start(self) -> bool:
        if self.is_busy:
            return False
        if not 1 <= self.selected_duration_minutes <= self.max_duration_minutes:
            return False
        state = self.hass.states.get(self.target_entity_id)
        if not is_state_usable(state):
            return False
        return not target_state_reached(
            self.target_entity_id,
            state,
            self.selected_action,
        )

    @property
    def can_cancel(self) -> bool:
        return self.status == STATUS_ACTIVE

    async def async_initialize(self) -> None:
        """Load persisted state and defer restoration until startup is complete."""
        stored = await self._store.async_load() or {}
        self._restore_fields(stored)

        self._target_unsub = async_track_state_change_event(
            self.hass,
            [self.target_entity_id],
            self._handle_target_state_event,
        )
        if is_state_usable(self.hass.states.get(self.target_entity_id)):
            self._target_available_event.set()

        needs_startup_restore = False

        async with self._lock:
            if self.status not in (STATUS_ACTIVE, STATUS_EXECUTING):
                self.status = STATUS_IDLE if self.status != STATUS_ERROR else STATUS_ERROR
                self._restore_pending = False
                await self._async_save_locked()
            elif self.finishes_at is None:
                self._set_idle_locked(
                    RESULT_ERROR,
                    REASON_ACTION_FAILED,
                    self._localize(
                        "No se pudo restaurar el temporizador porque no tenía una fecha final.",
                        "The timer could not be restored because it had no finish time.",
                    ),
                    as_error=True,
                )
                await self._async_save_locked()
            else:
                # During startup, the target may only have a temporary restored state
                # or may not have loaded yet. Do not execute or cancel from that state.
                self.status = STATUS_ACTIVE
                self._restore_pending = True
                self._cancel_finish_schedule_locked()
                self._cancel_watchdog_locked()
                needs_startup_restore = True
                await self._async_save_locked()

        self._async_notify_listeners()

        if needs_startup_restore:
            self._startup_unsub = async_at_started(
                self.hass,
                self._handle_home_assistant_started,
            )

    async def async_shutdown(self) -> None:
        """Stop listeners, pending restoration work, and persist state."""
        if self._startup_unsub is not None:
            self._startup_unsub()
            self._startup_unsub = None

        restore_task = self._restore_task
        self._restore_task = None
        if restore_task is not None and restore_task is not asyncio.current_task():
            restore_task.cancel()
            with suppress(asyncio.CancelledError):
                await restore_task

        async with self._lock:
            self._cancel_finish_schedule_locked()
            self._cancel_watchdog_locked()
            await self._async_save_locked()
        if self._target_unsub is not None:
            self._target_unsub()
            self._target_unsub = None
        self._listeners.clear()

    @callback
    def async_add_listener(self, listener: UpdateCallback) -> Callable[[], None]:
        """Register an entity update callback."""
        self._listeners.add(listener)

        @callback
        def remove_listener() -> None:
            self._listeners.discard(listener)

        return remove_listener

    @callback
    def async_publish_state(self) -> None:
        """Publish the current runtime state after platform/registry changes."""
        self._async_notify_listeners()

    @callback
    def _async_notify_listeners(self) -> None:
        for listener in tuple(self._listeners):
            listener()

    @callback
    def _handle_target_state_event(
        self,
        event: Event[EventStateChangedData],
    ) -> None:
        """React immediately when the configured target changes state."""
        new_state = event.data["new_state"]
        _LOGGER.debug(
            "Target state event for %s: %s -> %s while timer status=%s action=%s",
            self.target_entity_id,
            event.data["old_state"].state if event.data["old_state"] else None,
            new_state.state if new_state else None,
            self.status,
            self.selected_action,
        )

        if is_state_usable(new_state):
            self._target_available_event.set()

        # Refresh attributes such as target_entity_state even while the timer is idle.
        self._async_notify_listeners()

        if self.status != STATUS_ACTIVE:
            return
        if target_state_reached(
            self.target_entity_id,
            new_state,
            self.selected_action,
        ):
            self._request_target_state_check()

    @callback
    def _handle_watchdog_interval(self, _now: datetime) -> None:
        """Catch a target state that was not observed through the event listener."""
        if self.status != STATUS_ACTIVE:
            return
        if target_state_reached(
            self.target_entity_id,
            self.hass.states.get(self.target_entity_id),
            self.selected_action,
        ):
            _LOGGER.debug(
                "Target-state watchdog detected completion for %s",
                self.target_entity_id,
            )
            self._async_notify_listeners()
            self._request_target_state_check()

    @callback
    def _handle_home_assistant_started(self, _hass: HomeAssistant) -> None:
        """Resume a persisted timer only after Home Assistant has fully started."""
        self._startup_unsub = None
        if self._restore_task is not None and not self._restore_task.done():
            return
        self._restore_task = self.hass.async_create_task(
            self._async_restore_after_startup()
        )

    async def _async_restore_after_startup(self) -> None:
        """Restore scheduling or process an expired timer after startup."""
        notification: tuple[str, str] | None = None
        execute_expired = False
        current_task = asyncio.current_task()

        try:
            async with self._lock:
                if self.status != STATUS_ACTIVE or not self._restore_pending:
                    return

                finishes_at = self.finishes_at
                state = self.hass.states.get(self.target_entity_id)
                if finishes_at is None:
                    self._set_idle_locked(
                        RESULT_ERROR,
                        REASON_ACTION_FAILED,
                        self._localize(
                            "No se pudo restaurar el temporizador porque no tenía una fecha final.",
                            "The timer could not be restored because it had no finish time.",
                        ),
                        as_error=True,
                    )
                    await self._async_save_locked()
                elif is_state_usable(state) and target_state_reached(
                    self.target_entity_id,
                    state,
                    self.selected_action,
                ):
                    self._set_idle_locked(
                        RESULT_AUTO_CANCELLED,
                        REASON_ALREADY_TARGET,
                        self._already_target_message(),
                    )
                    await self._async_save_locked()
                elif finishes_at > datetime.now(UTC):
                    # Home Assistant is now running; resume the original absolute deadline.
                    self._restore_pending = False
                    self._schedule_finish_locked(finishes_at)
                    self._start_watchdog_locked()
                    await self._async_save_locked()
                else:
                    should_execute = (
                        self.selected_action == ACTION_TURN_OFF
                        and bool(
                            self._effective.get(
                                CONF_EXECUTE_EXPIRED_TURN_OFF,
                                DEFAULT_EXECUTE_EXPIRED_TURN_OFF,
                            )
                        )
                    ) or (
                        self.selected_action == ACTION_TURN_ON
                        and bool(
                            self._effective.get(
                                CONF_EXECUTE_EXPIRED_TURN_ON,
                                DEFAULT_EXECUTE_EXPIRED_TURN_ON,
                            )
                        )
                    )

                    if should_execute:
                        execute_expired = True
                    else:
                        message = self._localize(
                            f"El temporizador de {self._action_label()} venció durante el reinicio y la acción fue omitida por seguridad.",
                            f"The {self._action_label()} timer expired during restart and the action was skipped for safety.",
                        )
                        self._set_idle_locked(
                            RESULT_SKIPPED,
                            REASON_EXPIRED_DURING_RESTART,
                            message,
                        )
                        await self._async_save_locked()
                        notification = (
                            self._localize("Temporizador omitido", "Timer skipped"),
                            message,
                        )

            self._async_notify_listeners()

            if not execute_expired:
                if notification:
                    await self._async_send_notification(*notification)
                return

            state = await self._async_wait_for_real_target_state(
                RESTORE_TARGET_WAIT_SECONDS
            )

            async with self._lock:
                if self.status != STATUS_ACTIVE or not self._restore_pending:
                    return

                # Re-read under the lock after waiting; the event may be stale.
                state = self.hass.states.get(self.target_entity_id)
                if not is_state_usable(state):
                    message = self._localize(
                        f"El temporizador venció durante el reinicio, pero {self._target_name()} no estuvo disponible después de esperar {RESTORE_TARGET_WAIT_SECONDS} segundos.",
                        f"The timer expired during restart, but {self._target_name()} was not available after waiting {RESTORE_TARGET_WAIT_SECONDS} seconds.",
                    )
                    self._set_idle_locked(
                        RESULT_ERROR,
                        REASON_RESTORE_TARGET_UNAVAILABLE,
                        message,
                        as_error=True,
                    )
                    await self._async_save_locked()
                    notification = (
                        self._localize("Error en el temporizador", "Timer error"),
                        message,
                    )
                    execute_expired = False
                elif target_state_reached(
                    self.target_entity_id,
                    state,
                    self.selected_action,
                ):
                    message = self._already_target_message()
                    self._set_idle_locked(
                        RESULT_AUTO_CANCELLED,
                        REASON_ALREADY_TARGET,
                        message,
                    )
                    await self._async_save_locked()
                    execute_expired = False
                    notification = None
                else:
                    self._restore_pending = False
                    self._start_watchdog_locked()
                    await self._async_save_locked()

            self._async_notify_listeners()

            if execute_expired:
                await self.async_finish(restored=True)
            elif notification:
                await self._async_send_notification(*notification)
        finally:
            if self._restore_task is current_task:
                self._restore_task = None

    async def _async_wait_for_real_target_state(
        self,
        timeout_seconds: int,
    ) -> State | None:
        """Wait for a usable, non-restored target state after startup."""
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout_seconds

        while True:
            state = self.hass.states.get(self.target_entity_id)
            if is_state_usable(state):
                return state

            remaining = deadline - loop.time()
            if remaining <= 0:
                return None

            self._target_available_event.clear()
            # Close the race between the previous read and clearing the event.
            state = self.hass.states.get(self.target_entity_id)
            if is_state_usable(state):
                return state

            try:
                await asyncio.wait_for(
                    self._target_available_event.wait(),
                    timeout=remaining,
                )
            except TimeoutError:
                return None

    @callback
    def _request_target_state_check(self) -> None:
        """Schedule exactly one race-safe automatic-cancellation check."""
        if self._target_check_pending:
            return
        self._target_check_pending = True
        self.hass.async_create_task(self._async_process_target_state_change())

    async def _async_process_target_state_change(self) -> None:
        """Cancel an active timer when its requested final state is reached early."""
        notify = False
        title = ""
        message = ""

        try:
            async with self._lock:
                if self.status != STATUS_ACTIVE:
                    return

                # Re-read under the lock. The event that scheduled this task may be stale.
                state = self.hass.states.get(self.target_entity_id)
                if not target_state_reached(
                    self.target_entity_id,
                    state,
                    self.selected_action,
                ):
                    return

                message = self._localize(
                    f"{self._target_name()} alcanzó antes el estado objetivo. El temporizador se canceló automáticamente.",
                    f"{self._target_name()} reached the target state early. The timer was cancelled automatically.",
                )
                self._set_idle_locked(
                    RESULT_AUTO_CANCELLED,
                    REASON_TARGET_REACHED,
                    message,
                )
                await self._async_save_locked()
                notify = bool(
                    self._effective.get(
                        CONF_NOTIFY_AUTO_CANCEL,
                        DEFAULT_NOTIFY_AUTO_CANCEL,
                    )
                )
                title = self._localize(
                    "Temporizador cancelado",
                    "Timer cancelled",
                )
        finally:
            self._target_check_pending = False

        self._async_notify_listeners()
        if notify:
            await self._async_send_notification(title, message)

    async def async_start(
        self,
        duration_minutes: int | None = None,
        end_action: str | None = None,
    ) -> None:
        """Start the timer after validating the target and requested state."""
        async with self._lock:
            if self.is_busy:
                raise HomeAssistantError(
                    self._localize(
                        "El temporizador ya está activo.",
                        "The timer is already active.",
                    )
                )

            action = end_action or self.selected_action
            if action not in ACTIONS:
                raise HomeAssistantError(
                    self._localize(
                        "La acción final no es válida.",
                        "The final action is invalid.",
                    )
                )

            duration = int(
                duration_minutes
                if duration_minutes is not None
                else self.selected_duration_minutes
            )
            if not 1 <= duration <= self.max_duration_minutes:
                raise HomeAssistantError(
                    self._localize(
                        f"La duración debe estar entre 1 y {self.max_duration_minutes} minutos.",
                        f"Duration must be between 1 and {self.max_duration_minutes} minutes.",
                    )
                )

            state = self.hass.states.get(self.target_entity_id)
            if not is_state_usable(state):
                raise HomeAssistantError(
                    self._localize(
                        "La entidad objetivo no está disponible.",
                        "The target entity is unavailable.",
                    )
                )
            if target_state_reached(self.target_entity_id, state, action):
                raise HomeAssistantError(self._already_target_message(action))

            now = datetime.now(UTC)
            self.selected_action = action
            self.selected_duration_minutes = duration
            self.started_at = now
            self.finishes_at = now + timedelta(minutes=duration)
            self.status = STATUS_ACTIVE
            self._restore_pending = False
            self.last_result = None
            self.last_reason = None
            self.last_message = None
            self._schedule_finish_locked(self.finishes_at)
            self._start_watchdog_locked()
            await self._async_save_locked()

        self._async_notify_listeners()

    async def async_cancel(self) -> None:
        """Cancel an active timer without executing the final action."""
        notify = False
        title = ""
        message = ""
        async with self._lock:
            if self.status != STATUS_ACTIVE:
                raise HomeAssistantError(
                    self._localize(
                        "No hay un temporizador activo para cancelar.",
                        "There is no active timer to cancel.",
                    )
                )

            self._cancel_finish_schedule_locked()
            message = self._localize(
                f"El temporizador de {self._target_name()} fue cancelado manualmente.",
                f"The timer for {self._target_name()} was cancelled manually.",
            )
            self._set_idle_locked(
                RESULT_CANCELLED,
                REASON_MANUAL_CANCEL,
                message,
            )
            await self._async_save_locked()
            notify = bool(
                self._effective.get(
                    CONF_NOTIFY_MANUAL_CANCEL,
                    DEFAULT_NOTIFY_MANUAL_CANCEL,
                )
            )
            title = self._localize(
                "Temporizador cancelado",
                "Timer cancelled",
            )

        self._async_notify_listeners()
        if notify:
            await self._async_send_notification(title, message)

    async def async_set_values(
        self,
        *,
        duration_minutes: int | None = None,
        end_action: str | None = None,
    ) -> None:
        """Atomically update idle timer values for cards and native controls."""
        if duration_minutes is None and end_action is None:
            raise HomeAssistantError(
                self._localize(
                    "Debes indicar una duración, una acción o ambas.",
                    "Provide a duration, an action, or both.",
                )
            )

        async with self._lock:
            if self.is_busy:
                raise HomeAssistantError(
                    self._localize(
                        "No se pueden cambiar los valores mientras el temporizador está activo.",
                        "Timer values cannot be changed while the timer is active.",
                    )
                )

            if duration_minutes is not None:
                value = int(duration_minutes)
                if not 1 <= value <= self.max_duration_minutes:
                    raise HomeAssistantError(
                        self._localize(
                            f"La duración debe estar entre 1 y {self.max_duration_minutes} minutos.",
                            f"Duration must be between 1 and {self.max_duration_minutes} minutes.",
                        )
                    )
                self.selected_duration_minutes = value

            if end_action is not None:
                if end_action not in ACTIONS:
                    raise HomeAssistantError(
                        self._localize(
                            "La acción final no es válida.",
                            "The final action is invalid.",
                        )
                    )
                self.selected_action = end_action

            await self._async_save_locked()

        self._async_notify_listeners()

    async def async_set_duration(self, minutes: int) -> None:
        """Set the idle duration in whole minutes."""
        await self.async_set_values(duration_minutes=minutes)

    async def async_select_action(self, action: str) -> None:
        """Set turn_on or turn_off while idle."""
        await self.async_set_values(end_action=action)

    async def async_finish(self, *, restored: bool = False) -> None:
        """Execute the requested final action after a final race-safe check."""
        notification: tuple[str, str] | None = None

        async with self._lock:
            if self.status != STATUS_ACTIVE:
                return

            self._restore_pending = False
            self._cancel_finish_schedule_locked()
            self._cancel_watchdog_locked()
            state = self.hass.states.get(self.target_entity_id)

            if target_state_reached(
                self.target_entity_id,
                state,
                self.selected_action,
            ):
                message = self._localize(
                    f"{self._target_name()} ya había alcanzado el estado objetivo. El temporizador se canceló automáticamente.",
                    f"{self._target_name()} had already reached the target state. The timer was cancelled automatically.",
                )
                self._set_idle_locked(
                    RESULT_AUTO_CANCELLED,
                    REASON_TARGET_REACHED,
                    message,
                )
                await self._async_save_locked()
                if bool(
                    self._effective.get(
                        CONF_NOTIFY_AUTO_CANCEL,
                        DEFAULT_NOTIFY_AUTO_CANCEL,
                    )
                ):
                    notification = (
                        self._localize(
                            "Temporizador cancelado",
                            "Timer cancelled",
                        ),
                        message,
                    )
            elif not is_state_usable(state):
                message = self._localize(
                    f"No fue posible ejecutar el temporizador porque {self._target_name()} no estaba disponible.",
                    f"The timer could not run because {self._target_name()} was unavailable.",
                )
                self._set_idle_locked(
                    RESULT_ERROR,
                    REASON_TARGET_UNAVAILABLE,
                    message,
                    as_error=True,
                )
                await self._async_save_locked()
                notification = (
                    self._localize(
                        "Error en el temporizador",
                        "Timer error",
                    ),
                    message,
                )
            else:
                # Re-read immediately before calling the service to close the last race window.
                state = self.hass.states.get(self.target_entity_id)
                if target_state_reached(
                    self.target_entity_id,
                    state,
                    self.selected_action,
                ):
                    message = self._localize(
                        f"{self._target_name()} alcanzó el estado objetivo justo antes de finalizar. El temporizador se canceló automáticamente.",
                        f"{self._target_name()} reached the target state just before completion. The timer was cancelled automatically.",
                    )
                    self._set_idle_locked(
                        RESULT_AUTO_CANCELLED,
                        REASON_TARGET_REACHED,
                        message,
                    )
                    await self._async_save_locked()
                else:
                    self.status = STATUS_EXECUTING
                    await self._async_save_locked()
                    self._async_notify_listeners()

                    try:
                        await self.hass.services.async_call(
                            "homeassistant",
                            self.selected_action,
                            {},
                            target={ATTR_ENTITY_ID: self.target_entity_id},
                            blocking=True,
                        )
                    except Exception as err:  # Home Assistant service exceptions vary by platform.
                        _LOGGER.exception(
                            "Failed to %s %s",
                            self.selected_action,
                            self.target_entity_id,
                        )
                        message = self._localize(
                            f"No fue posible {self._action_infinitive()} {self._target_name()}: {err}",
                            f"Unable to {self._action_infinitive()} {self._target_name()}: {err}",
                        )
                        self._set_idle_locked(
                            RESULT_ERROR,
                            REASON_ACTION_FAILED,
                            message,
                            as_error=True,
                        )
                        await self._async_save_locked()
                        notification = (
                            self._localize(
                                "Error en el temporizador",
                                "Timer error",
                            ),
                            message,
                        )
                    else:
                        confirmed = await self._async_wait_for_target_state_locked()
                        if confirmed:
                            restored_text_es = " después de restaurar Home Assistant" if restored else ""
                            restored_text_en = " after Home Assistant was restored" if restored else ""
                            message = self._localize(
                                f"{self._target_name()} fue {self._action_participle_es()} después de {format_duration(self.selected_duration_minutes, spanish=True)}{restored_text_es}.",
                                f"{self._target_name()} was {self._action_participle_en()} after {format_duration(self.selected_duration_minutes)}{restored_text_en}.",
                            )
                            self._set_idle_locked(
                                RESULT_COMPLETED,
                                None,
                                message,
                            )
                            await self._async_save_locked()
                            notification = (
                                self._localize(
                                    "Temporizador finalizado",
                                    "Timer finished",
                                ),
                                message,
                            )
                        else:
                            message = self._localize(
                                f"Se envió la orden para {self._action_infinitive()} {self._target_name()}, pero no se confirmó el estado objetivo en {self.confirmation_timeout} segundos.",
                                f"The command to {self._action_infinitive()} {self._target_name()} was sent, but the target state was not confirmed within {self.confirmation_timeout} seconds.",
                            )
                            self._set_idle_locked(
                                RESULT_ERROR,
                                REASON_CONFIRMATION_TIMEOUT,
                                message,
                                as_error=True,
                            )
                            await self._async_save_locked()
                            notification = (
                                self._localize(
                                    "Error en el temporizador",
                                    "Timer error",
                                ),
                                message,
                            )

        self._async_notify_listeners()
        if notification:
            await self._async_send_notification(*notification)

    async def _async_wait_for_target_state_locked(self) -> bool:
        loop = asyncio.get_running_loop()
        deadline = loop.time() + self.confirmation_timeout
        while loop.time() < deadline:
            if target_state_reached(
                self.target_entity_id,
                self.hass.states.get(self.target_entity_id),
                self.selected_action,
            ):
                return True
            await asyncio.sleep(0.25)
        return target_state_reached(
            self.target_entity_id,
            self.hass.states.get(self.target_entity_id),
            self.selected_action,
        )

    @callback
    def _schedule_finish_locked(self, when: datetime) -> None:
        self._cancel_finish_schedule_locked()
        self._finish_unsub = async_track_point_in_utc_time(
            self.hass,
            self._handle_finish_time,
            when,
        )

    @callback
    def _handle_finish_time(self, _now: datetime) -> None:
        self._finish_unsub = None
        self.hass.async_create_task(self.async_finish())

    @callback
    def _cancel_finish_schedule_locked(self) -> None:
        if self._finish_unsub is not None:
            self._finish_unsub()
            self._finish_unsub = None

    @callback
    def _start_watchdog_locked(self) -> None:
        """Start a lightweight one-second state watchdog only while active."""
        self._cancel_watchdog_locked()
        self._watchdog_unsub = async_track_time_interval(
            self.hass,
            self._handle_watchdog_interval,
            timedelta(seconds=WATCHDOG_INTERVAL_SECONDS),
        )

    @callback
    def _cancel_watchdog_locked(self) -> None:
        if self._watchdog_unsub is not None:
            self._watchdog_unsub()
            self._watchdog_unsub = None

    async def _async_send_notification(self, title: str, message: str) -> None:
        target = self.notification_target
        if not target:
            return
        try:
            await self.hass.services.async_call(
                "notify",
                "send_message",
                {
                    "title": title,
                    "message": message,
                },
                target=target,
                blocking=True,
            )
        except Exception:
            _LOGGER.exception(
                "Timer action completed, but notification delivery failed for %s",
                self.entry.entry_id,
            )

    def _restore_fields(self, stored: dict[str, Any]) -> None:
        self.status = str(stored.get("status", STATUS_IDLE))
        action = str(stored.get("selected_action", self.default_action))
        self.selected_action = action if action in ACTIONS else self.default_action
        duration = int(
            stored.get(
                "selected_duration_minutes",
                self.default_duration_minutes,
            )
        )
        self.selected_duration_minutes = min(
            max(1, duration),
            self.max_duration_minutes,
        )
        self.started_at = self._parse_datetime(stored.get("started_at"))
        self.finishes_at = self._parse_datetime(stored.get("finishes_at"))
        self.last_result = stored.get("last_result")
        self.last_reason = stored.get("last_reason")
        self.last_message = stored.get("last_message")
        self.last_finished_at = self._parse_datetime(stored.get("last_finished_at"))

    async def _async_save_locked(self) -> None:
        await self._store.async_save(
            {
                "status": self.status,
                "selected_action": self.selected_action,
                "selected_duration_minutes": self.selected_duration_minutes,
                "started_at": self._iso(self.started_at),
                "finishes_at": self._iso(self.finishes_at),
                "last_result": self.last_result,
                "last_reason": self.last_reason,
                "last_message": self.last_message,
                "last_finished_at": self._iso(self.last_finished_at),
            }
        )

    def _set_idle_locked(
        self,
        result: str,
        reason: str | None,
        message: str,
        *,
        as_error: bool = False,
    ) -> None:
        self._cancel_finish_schedule_locked()
        self._cancel_watchdog_locked()
        self.status = STATUS_ERROR if as_error else STATUS_IDLE
        self._restore_pending = False
        self.started_at = None
        self.finishes_at = None
        self.last_result = result
        self.last_reason = reason
        self.last_message = message
        self.last_finished_at = datetime.now(UTC)

    def _companion_entities(self) -> dict[str, str | None]:
        """Return native companion entity IDs by stable unique ID."""
        registry = er.async_get(self.hass)
        prefix = self.entry.entry_id
        return {
            "duration": registry.async_get_entity_id(
                "number", DOMAIN, f"{prefix}_duration"
            ),
            "action": registry.async_get_entity_id(
                "select", DOMAIN, f"{prefix}_end_action"
            ),
            "start": registry.async_get_entity_id(
                "button", DOMAIN, f"{prefix}_start"
            ),
            "cancel": registry.async_get_entity_id(
                "button", DOMAIN, f"{prefix}_cancel"
            ),
        }

    def state_attributes(self) -> dict[str, Any]:
        """Return stable attributes for native UI and card API v2."""
        state = self.hass.states.get(self.target_entity_id)
        return {
            "target_entity": self.target_entity_id,
            "target_entity_name": self._target_name(),
            "target_entity_state": state.state if state else None,
            "target_state_reached": target_state_reached(
                self.target_entity_id,
                state,
                self.selected_action,
            ),
            "end_action": self.selected_action,
            "duration_minutes": self.selected_duration_minutes,
            "duration_seconds": self.selected_duration_minutes * 60,
            "started_at": self._iso(self.started_at),
            "finishes_at": self._iso(self.finishes_at),
            "remaining_seconds_snapshot": self.remaining_seconds,
            "can_start": self.can_start,
            "can_cancel": self.can_cancel,
            "last_result": self.last_result,
            "last_reason": self.last_reason,
            "last_message": self.last_message,
            "last_finished_at": self._iso(self.last_finished_at),
            "backend_version": VERSION,
            "card_api_version": CARD_API_VERSION,
            "capabilities": [
                ACTION_TURN_ON,
                ACTION_TURN_OFF,
                "set_duration",
                "set_action",
                "start",
                "cancel",
            ],
            "constraints": {
                "min_seconds": 60,
                "max_seconds": self.max_duration_minutes * 60,
                "step_seconds": 60,
            },
            "companion_entities": self._companion_entities(),
            "watchdog_active": self._watchdog_unsub is not None,
            "restore_pending": self._restore_pending,
            "restore_target_wait_seconds": RESTORE_TARGET_WAIT_SECONDS,
        }

    def diagnostics(self) -> dict[str, Any]:
        """Return diagnostic information without notification destination IDs."""
        return {
            "status": self.status,
            "target_entity": self.target_entity_id,
            "target_state": (
                self.hass.states.get(self.target_entity_id).state
                if self.hass.states.get(self.target_entity_id)
                else None
            ),
            "selected_action": self.selected_action,
            "selected_duration_minutes": self.selected_duration_minutes,
            "started_at": self._iso(self.started_at),
            "finishes_at": self._iso(self.finishes_at),
            "last_result": self.last_result,
            "last_reason": self.last_reason,
            "last_message": self.last_message,
            "backend_version": VERSION,
            "card_api_version": CARD_API_VERSION,
            "capabilities": [
                ACTION_TURN_ON,
                ACTION_TURN_OFF,
                "set_duration",
                "set_action",
                "start",
                "cancel",
            ],
            "constraints": {
                "min_seconds": 60,
                "max_seconds": self.max_duration_minutes * 60,
                "step_seconds": 60,
            },
            "watchdog_active": self._watchdog_unsub is not None,
            "restore_pending": self._restore_pending,
            "restore_target_wait_seconds": RESTORE_TARGET_WAIT_SECONDS,
        }

    def _already_target_message(self, action: str | None = None) -> str:
        requested_action = action or self.selected_action
        if requested_action == ACTION_TURN_ON:
            return self._localize(
                f"{self._target_name()} ya está encendido.",
                f"{self._target_name()} is already on.",
            )
        return self._localize(
            f"{self._target_name()} ya está apagado.",
            f"{self._target_name()} is already off.",
        )

    def _target_name(self) -> str:
        state = self.hass.states.get(self.target_entity_id)
        if state is not None:
            return str(state.attributes.get("friendly_name", self.target_entity_id))
        return self.target_entity_id

    def _action_label(self) -> str:
        if self.selected_action == ACTION_TURN_ON:
            return self._localize("encendido", "turn-on")
        return self._localize("apagado", "turn-off")

    def _action_infinitive(self) -> str:
        if self.selected_action == ACTION_TURN_ON:
            return self._localize("encender", "turn on")
        return self._localize("apagar", "turn off")

    def _action_participle_es(self) -> str:
        return "encendido" if self.selected_action == ACTION_TURN_ON else "apagado"

    def _action_participle_en(self) -> str:
        return "turned on" if self.selected_action == ACTION_TURN_ON else "turned off"

    def _localize(self, spanish: str, english: str) -> str:
        return spanish if self.hass.config.language.lower().startswith("es") else english

    @staticmethod
    def _parse_datetime(value: Any) -> datetime | None:
        if not isinstance(value, str) or not value:
            return None
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)

    @staticmethod
    def _iso(value: datetime | None) -> str | None:
        return value.astimezone(UTC).isoformat() if value else None
