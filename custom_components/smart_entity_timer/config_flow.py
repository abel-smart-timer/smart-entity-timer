"""Config flow for Smart Entity Timer."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import (
    SOURCE_USER,
    ConfigEntry,
    ConfigSubentryFlow,
    FlowType,
    SubentryFlowContext,
)
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    ACTIONS,
    ARCHITECTURE_SUBENTRIES_V1,
    CONF_ARCHITECTURE,
    CONF_CONFIRMATION_TIMEOUT,
    CONF_DEFAULT_ACTION,
    CONF_DEFAULT_DURATION_MINUTES,
    CONF_EXECUTE_EXPIRED_TURN_OFF,
    CONF_EXECUTE_EXPIRED_TURN_ON,
    CONF_MAX_DURATION_MINUTES,
    CONF_NOTIFICATION_TARGET,
    CONF_NOTIFICATION_AUTO_CANCEL_MESSAGE,
    CONF_NOTIFICATION_AUTO_CANCEL_TITLE,
    CONF_NOTIFICATION_COMPLETED_MESSAGE,
    CONF_NOTIFICATION_COMPLETED_TITLE,
    CONF_NOTIFICATION_ERROR_MESSAGE,
    CONF_NOTIFICATION_ERROR_TITLE,
    CONF_NOTIFICATION_MANUAL_CANCEL_MESSAGE,
    CONF_NOTIFICATION_MANUAL_CANCEL_TITLE,
    CONF_NOTIFICATION_SKIPPED_MESSAGE,
    CONF_NOTIFICATION_SKIPPED_TITLE,
    CONF_NOTIFY_AUTO_CANCEL,
    CONF_NOTIFY_MANUAL_CANCEL,
    CONF_TARGET_ENTITY,
    CONF_TIMER_ID,
    CONFIG_ENTRY_VERSION,
    DEFAULT_ACTION,
    DEFAULT_CONFIRMATION_TIMEOUT,
    DEFAULT_DURATION_MINUTES,
    DEFAULT_EXECUTE_EXPIRED_TURN_OFF,
    DEFAULT_EXECUTE_EXPIRED_TURN_ON,
    DEFAULT_MAX_DURATION_MINUTES,
    DEFAULT_NOTIFICATION_TEMPLATE,
    DEFAULT_NOTIFY_AUTO_CANCEL,
    DEFAULT_NOTIFY_MANUAL_CANCEL,
    DOMAIN,
    NAME,
    NOTIFICATION_TEMPLATE_CONFIG_KEYS,
    SUBENTRY_TYPE_TIMER,
    SUPPORTED_DOMAINS,
)
from .manager import SmartEntityTimerManager
from .notifications import validate_notification_template

ENTITY_SELECTOR = selector.EntitySelector(
    selector.EntitySelectorConfig(domain=list(SUPPORTED_DOMAINS))
)
ACTION_SELECTOR = selector.SelectSelector(
    selector.SelectSelectorConfig(
        options=list(ACTIONS),
        mode=selector.SelectSelectorMode.DROPDOWN,
        translation_key="end_action",
    )
)
NOTIFICATION_TARGET_SELECTOR = selector.TargetSelector(
    selector.TargetSelectorConfig(
        entity=selector.EntitySelectorConfig(domain=["notify"]),
    )
)
NOTIFICATION_TITLE_SELECTOR = selector.TextSelector(
    selector.TextSelectorConfig(multiline=False)
)
NOTIFICATION_MESSAGE_SELECTOR = selector.TextSelector(
    selector.TextSelectorConfig(multiline=True)
)
NAME_SELECTOR = selector.TextSelector(selector.TextSelectorConfig(multiline=False))


def _duration_selector(maximum: int) -> selector.NumberSelector:
    return selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=1,
            max=maximum,
            step=1,
            mode=selector.NumberSelectorMode.BOX,
            unit_of_measurement="min",
        )
    )


def _base_defaults() -> dict[str, Any]:
    return {
        CONF_DEFAULT_ACTION: DEFAULT_ACTION,
        CONF_DEFAULT_DURATION_MINUTES: DEFAULT_DURATION_MINUTES,
        CONF_MAX_DURATION_MINUTES: DEFAULT_MAX_DURATION_MINUTES,
        CONF_NOTIFICATION_TARGET: {},
        CONF_NOTIFY_MANUAL_CANCEL: DEFAULT_NOTIFY_MANUAL_CANCEL,
        CONF_NOTIFY_AUTO_CANCEL: DEFAULT_NOTIFY_AUTO_CANCEL,
        CONF_NOTIFICATION_COMPLETED_TITLE: DEFAULT_NOTIFICATION_TEMPLATE,
        CONF_NOTIFICATION_COMPLETED_MESSAGE: DEFAULT_NOTIFICATION_TEMPLATE,
        CONF_NOTIFICATION_ERROR_TITLE: DEFAULT_NOTIFICATION_TEMPLATE,
        CONF_NOTIFICATION_ERROR_MESSAGE: DEFAULT_NOTIFICATION_TEMPLATE,
        CONF_NOTIFICATION_SKIPPED_TITLE: DEFAULT_NOTIFICATION_TEMPLATE,
        CONF_NOTIFICATION_SKIPPED_MESSAGE: DEFAULT_NOTIFICATION_TEMPLATE,
        CONF_NOTIFICATION_MANUAL_CANCEL_TITLE: DEFAULT_NOTIFICATION_TEMPLATE,
        CONF_NOTIFICATION_MANUAL_CANCEL_MESSAGE: DEFAULT_NOTIFICATION_TEMPLATE,
        CONF_NOTIFICATION_AUTO_CANCEL_TITLE: DEFAULT_NOTIFICATION_TEMPLATE,
        CONF_NOTIFICATION_AUTO_CANCEL_MESSAGE: DEFAULT_NOTIFICATION_TEMPLATE,
        CONF_EXECUTE_EXPIRED_TURN_OFF: DEFAULT_EXECUTE_EXPIRED_TURN_OFF,
        CONF_EXECUTE_EXPIRED_TURN_ON: DEFAULT_EXECUTE_EXPIRED_TURN_ON,
        CONF_CONFIRMATION_TIMEOUT: DEFAULT_CONFIRMATION_TIMEOUT,
    }


def _timer_schema(current: dict[str, Any]) -> vol.Schema:
    """Return the complete add/reconfigure form for one timer subentry."""
    name_key = (
        vol.Required(CONF_NAME, default=current[CONF_NAME])
        if current.get(CONF_NAME)
        else vol.Required(CONF_NAME)
    )
    target_key = (
        vol.Required(CONF_TARGET_ENTITY, default=current[CONF_TARGET_ENTITY])
        if current.get(CONF_TARGET_ENTITY)
        else vol.Required(CONF_TARGET_ENTITY)
    )
    return vol.Schema(
        {
            name_key: NAME_SELECTOR,
            target_key: ENTITY_SELECTOR,
            vol.Required(
                CONF_DEFAULT_ACTION,
                default=current.get(CONF_DEFAULT_ACTION, DEFAULT_ACTION),
            ): ACTION_SELECTOR,
            vol.Required(
                CONF_DEFAULT_DURATION_MINUTES,
                default=current.get(
                    CONF_DEFAULT_DURATION_MINUTES, DEFAULT_DURATION_MINUTES
                ),
            ): _duration_selector(10080),
            vol.Required(
                CONF_MAX_DURATION_MINUTES,
                default=current.get(
                    CONF_MAX_DURATION_MINUTES, DEFAULT_MAX_DURATION_MINUTES
                ),
            ): _duration_selector(10080),
            vol.Optional(
                CONF_NOTIFICATION_TARGET,
                default=current.get(CONF_NOTIFICATION_TARGET, {}),
            ): NOTIFICATION_TARGET_SELECTOR,
            vol.Required(
                CONF_NOTIFY_MANUAL_CANCEL,
                default=current.get(
                    CONF_NOTIFY_MANUAL_CANCEL, DEFAULT_NOTIFY_MANUAL_CANCEL
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_NOTIFY_AUTO_CANCEL,
                default=current.get(CONF_NOTIFY_AUTO_CANCEL, DEFAULT_NOTIFY_AUTO_CANCEL),
            ): selector.BooleanSelector(),
            vol.Optional(
                CONF_NOTIFICATION_COMPLETED_TITLE,
                default=current.get(CONF_NOTIFICATION_COMPLETED_TITLE, ""),
            ): NOTIFICATION_TITLE_SELECTOR,
            vol.Optional(
                CONF_NOTIFICATION_COMPLETED_MESSAGE,
                default=current.get(CONF_NOTIFICATION_COMPLETED_MESSAGE, ""),
            ): NOTIFICATION_MESSAGE_SELECTOR,
            vol.Optional(
                CONF_NOTIFICATION_ERROR_TITLE,
                default=current.get(CONF_NOTIFICATION_ERROR_TITLE, ""),
            ): NOTIFICATION_TITLE_SELECTOR,
            vol.Optional(
                CONF_NOTIFICATION_ERROR_MESSAGE,
                default=current.get(CONF_NOTIFICATION_ERROR_MESSAGE, ""),
            ): NOTIFICATION_MESSAGE_SELECTOR,
            vol.Optional(
                CONF_NOTIFICATION_SKIPPED_TITLE,
                default=current.get(CONF_NOTIFICATION_SKIPPED_TITLE, ""),
            ): NOTIFICATION_TITLE_SELECTOR,
            vol.Optional(
                CONF_NOTIFICATION_SKIPPED_MESSAGE,
                default=current.get(CONF_NOTIFICATION_SKIPPED_MESSAGE, ""),
            ): NOTIFICATION_MESSAGE_SELECTOR,
            vol.Optional(
                CONF_NOTIFICATION_MANUAL_CANCEL_TITLE,
                default=current.get(CONF_NOTIFICATION_MANUAL_CANCEL_TITLE, ""),
            ): NOTIFICATION_TITLE_SELECTOR,
            vol.Optional(
                CONF_NOTIFICATION_MANUAL_CANCEL_MESSAGE,
                default=current.get(CONF_NOTIFICATION_MANUAL_CANCEL_MESSAGE, ""),
            ): NOTIFICATION_MESSAGE_SELECTOR,
            vol.Optional(
                CONF_NOTIFICATION_AUTO_CANCEL_TITLE,
                default=current.get(CONF_NOTIFICATION_AUTO_CANCEL_TITLE, ""),
            ): NOTIFICATION_TITLE_SELECTOR,
            vol.Optional(
                CONF_NOTIFICATION_AUTO_CANCEL_MESSAGE,
                default=current.get(CONF_NOTIFICATION_AUTO_CANCEL_MESSAGE, ""),
            ): NOTIFICATION_MESSAGE_SELECTOR,
            vol.Required(
                CONF_EXECUTE_EXPIRED_TURN_OFF,
                default=current.get(
                    CONF_EXECUTE_EXPIRED_TURN_OFF,
                    DEFAULT_EXECUTE_EXPIRED_TURN_OFF,
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_EXECUTE_EXPIRED_TURN_ON,
                default=current.get(
                    CONF_EXECUTE_EXPIRED_TURN_ON,
                    DEFAULT_EXECUTE_EXPIRED_TURN_ON,
                ),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_CONFIRMATION_TIMEOUT,
                default=current.get(
                    CONF_CONFIRMATION_TIMEOUT, DEFAULT_CONFIRMATION_TIMEOUT
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=60,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="s",
                )
            ),
        }
    )


class SmartEntityTimerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Create the single Smart Entity Timer parent integration entry."""

    VERSION = CONFIG_ENTRY_VERSION
    MINOR_VERSION = 0

    @classmethod
    @callback
    def async_get_supported_subentry_types(
        cls, config_entry: ConfigEntry
    ) -> dict[str, type[ConfigSubentryFlow]]:
        """Expose Timer as the child configuration type."""
        return {SUBENTRY_TYPE_TIMER: SmartEntityTimerSubentryFlow}

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Create the singleton parent; the first timer flow opens immediately."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return self.async_create_entry(
            title=NAME,
            data={CONF_ARCHITECTURE: ARCHITECTURE_SUBENTRIES_V1},
        )

    async def async_on_create_entry(self, result):
        """Open the first Timer subentry flow immediately after parent creation."""
        subentry_result = await self.hass.config_entries.subentries.async_init(
            (result["result"].entry_id, SUBENTRY_TYPE_TIMER),
            context=SubentryFlowContext(source=SOURCE_USER),
        )
        result["next_flow"] = (
            FlowType.CONFIG_SUBENTRIES_FLOW,
            subentry_result["flow_id"],
        )
        return result


class SmartEntityTimerSubentryFlow(ConfigSubentryFlow):
    """Add and reconfigure individual timers under the parent integration."""

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Add one timer."""
        errors: dict[str, str] = {}
        current = {**_base_defaults(), **(user_input or {})}

        if user_input is not None:
            parent = self._get_entry()
            manager = getattr(parent, "runtime_data", None)
            if isinstance(manager, SmartEntityTimerManager) and manager.is_busy:
                errors["base"] = "timer_active"
            else:
                errors = self._validate_timer_input(user_input)
            if not errors:
                title = str(user_input[CONF_NAME]).strip()
                data = dict(user_input)
                data.pop(CONF_NAME, None)
                return self.async_create_entry(
                    title=title,
                    data=data,
                    unique_id=str(data[CONF_TARGET_ENTITY]),
                )

        return self.async_show_form(
            step_id="user",
            data_schema=_timer_schema(current),
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ):
        """Edit one timer, including its target and all timer preferences."""
        parent = self._get_entry()
        subentry = self._get_reconfigure_subentry()
        errors: dict[str, str] = {}
        current = {
            **_base_defaults(),
            **dict(subentry.data),
            CONF_NAME: subentry.title,
        }

        if user_input is not None:
            manager = getattr(parent, "runtime_data", None)
            if isinstance(manager, SmartEntityTimerManager) and manager.is_busy:
                errors["base"] = "timer_active"
            else:
                errors = self._validate_timer_input(
                    user_input,
                    exclude_subentry_id=subentry.subentry_id,
                )

            if not errors:
                title = str(user_input[CONF_NAME]).strip()
                # Preserve the legacy timer identity on migrated timers. New 0.3.x
                # timers intentionally use their subentry_id and therefore have no key.
                data = dict(subentry.data)
                data.update(user_input)
                data.pop(CONF_NAME, None)
                if CONF_TIMER_ID not in subentry.data:
                    data.pop(CONF_TIMER_ID, None)
                return self.async_update_and_abort(
                    parent,
                    subentry,
                    title=title,
                    unique_id=str(data[CONF_TARGET_ENTITY]),
                    data=data,
                )
            current.update(user_input)

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_timer_schema(current),
            errors=errors,
        )

    def _validate_timer_input(
        self,
        user_input: dict[str, Any],
        *,
        exclude_subentry_id: str | None = None,
    ) -> dict[str, str]:
        errors: dict[str, str] = {}
        name = str(user_input.get(CONF_NAME, "")).strip()
        if not name:
            errors[CONF_NAME] = "name_required"

        target = str(user_input.get(CONF_TARGET_ENTITY, ""))
        domain = target.split(".", 1)[0] if "." in target else ""
        if domain not in SUPPORTED_DOMAINS:
            errors[CONF_TARGET_ENTITY] = "unsupported_domain"
        elif self.hass.states.get(target) is None:
            errors[CONF_TARGET_ENTITY] = "entity_not_found"
        elif self._target_is_configured(
            target,
            exclude_subentry_id=exclude_subentry_id,
        ):
            errors[CONF_TARGET_ENTITY] = "already_configured"

        try:
            default_duration = int(user_input[CONF_DEFAULT_DURATION_MINUTES])
            maximum = int(user_input[CONF_MAX_DURATION_MINUTES])
            if default_duration > maximum:
                errors[CONF_DEFAULT_DURATION_MINUTES] = "duration_above_maximum"
        except (KeyError, TypeError, ValueError):
            errors[CONF_DEFAULT_DURATION_MINUTES] = "duration_above_maximum"

        for template_key in NOTIFICATION_TEMPLATE_CONFIG_KEYS:
            try:
                validate_notification_template(
                    str(user_input.get(template_key, "") or "")
                )
            except ValueError:
                errors[template_key] = "invalid_notification_template"
        return errors

    def _target_is_configured(
        self,
        target: str,
        *,
        exclude_subentry_id: str | None = None,
    ) -> bool:
        for entry in self.hass.config_entries.async_entries(DOMAIN):
            for subentry in entry.subentries.values():
                if subentry.subentry_type != SUBENTRY_TYPE_TIMER:
                    continue
                if subentry.subentry_id == exclude_subentry_id:
                    continue
                if subentry.data.get(CONF_TARGET_ENTITY) == target:
                    return True

            # Also guard against a legacy entry if a setup/migration error left one in
            # storage. This path is not expected during normal 0.3.x operation.
            if not entry.subentries:
                effective = {**entry.data, **entry.options}
                if effective.get(CONF_TARGET_ENTITY) == target:
                    return True
        return False
