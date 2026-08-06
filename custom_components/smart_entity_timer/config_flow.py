"""Config flow for Smart Entity Timer."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    ACTIONS,
    CONF_CONFIRMATION_TIMEOUT,
    CONF_DEFAULT_ACTION,
    CONF_DEFAULT_DURATION_MINUTES,
    CONF_EXECUTE_EXPIRED_TURN_OFF,
    CONF_EXECUTE_EXPIRED_TURN_ON,
    CONF_MAX_DURATION_MINUTES,
    CONF_NOTIFICATION_TARGET,
    CONF_NOTIFY_AUTO_CANCEL,
    CONF_NOTIFY_MANUAL_CANCEL,
    CONF_TARGET_ENTITY,
    DEFAULT_ACTION,
    DEFAULT_CONFIRMATION_TIMEOUT,
    DEFAULT_DURATION_MINUTES,
    DEFAULT_EXECUTE_EXPIRED_TURN_OFF,
    DEFAULT_EXECUTE_EXPIRED_TURN_ON,
    DEFAULT_MAX_DURATION_MINUTES,
    DEFAULT_NOTIFY_AUTO_CANCEL,
    DEFAULT_NOTIFY_MANUAL_CANCEL,
    DOMAIN,
    SUPPORTED_DOMAINS,
)

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
        CONF_EXECUTE_EXPIRED_TURN_OFF: DEFAULT_EXECUTE_EXPIRED_TURN_OFF,
        CONF_EXECUTE_EXPIRED_TURN_ON: DEFAULT_EXECUTE_EXPIRED_TURN_ON,
        CONF_CONFIRMATION_TIMEOUT: DEFAULT_CONFIRMATION_TIMEOUT,
    }


class SmartEntityTimerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Create Smart Entity Timer entries from the UI."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            errors = self._validate(user_input)
            if not errors:
                title = str(user_input.pop(CONF_NAME)).strip()
                return self.async_create_entry(title=title, data=user_input)

        defaults = _base_defaults()
        schema = vol.Schema(
            {
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_TARGET_ENTITY): ENTITY_SELECTOR,
                vol.Required(
                    CONF_DEFAULT_ACTION,
                    default=(
                        user_input or defaults
                    ).get(CONF_DEFAULT_ACTION, DEFAULT_ACTION),
                ): ACTION_SELECTOR,
                vol.Required(
                    CONF_DEFAULT_DURATION_MINUTES,
                    default=(user_input or defaults).get(
                        CONF_DEFAULT_DURATION_MINUTES,
                        DEFAULT_DURATION_MINUTES,
                    ),
                ): _duration_selector(DEFAULT_MAX_DURATION_MINUTES),
                vol.Optional(
                    CONF_NOTIFICATION_TARGET,
                    default=(user_input or defaults).get(
                        CONF_NOTIFICATION_TARGET,
                        {},
                    ),
                ): NOTIFICATION_TARGET_SELECTOR,
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    def _validate(self, user_input: dict[str, Any]) -> dict[str, str]:
        errors: dict[str, str] = {}
        name = str(user_input.get(CONF_NAME, "")).strip()
        target = str(user_input.get(CONF_TARGET_ENTITY, ""))
        domain = target.split(".", 1)[0] if "." in target else ""

        if not name:
            errors[CONF_NAME] = "name_required"
        if domain not in SUPPORTED_DOMAINS:
            errors[CONF_TARGET_ENTITY] = "unsupported_domain"
        elif self.hass.states.get(target) is None:
            errors[CONF_TARGET_ENTITY] = "entity_not_found"
        elif self._target_is_configured(target):
            errors[CONF_TARGET_ENTITY] = "already_configured"
        return errors

    def _target_is_configured(
        self,
        target: str,
        *,
        exclude_entry_id: str | None = None,
    ) -> bool:
        for entry in self._async_current_entries():
            if entry.entry_id == exclude_entry_id:
                continue
            effective = {**entry.data, **entry.options}
            if effective.get(CONF_TARGET_ENTITY) == target:
                return True
        return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return SmartEntityTimerOptionsFlow()


class SmartEntityTimerOptionsFlow(config_entries.OptionsFlowWithReload):
    """Edit timer behavior and reload the entry automatically."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}
        current = {**_base_defaults(), **self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            runtime = getattr(self.config_entry, "runtime_data", None)
            if runtime is not None and runtime.is_busy:
                errors["base"] = "timer_active"
            else:
                target = str(user_input[CONF_TARGET_ENTITY])
                domain = target.split(".", 1)[0] if "." in target else ""
                if domain not in SUPPORTED_DOMAINS:
                    errors[CONF_TARGET_ENTITY] = "unsupported_domain"
                elif self.hass.states.get(target) is None:
                    errors[CONF_TARGET_ENTITY] = "entity_not_found"
                elif self._target_is_configured(target):
                    errors[CONF_TARGET_ENTITY] = "already_configured"

                default_duration = int(user_input[CONF_DEFAULT_DURATION_MINUTES])
                maximum = int(user_input[CONF_MAX_DURATION_MINUTES])
                if default_duration > maximum:
                    errors[CONF_DEFAULT_DURATION_MINUTES] = "duration_above_maximum"

            if not errors:
                return self.async_create_entry(title="", data=user_input)
            current.update(user_input)

        maximum_for_selector = max(
            DEFAULT_MAX_DURATION_MINUTES,
            int(current.get(CONF_MAX_DURATION_MINUTES, DEFAULT_MAX_DURATION_MINUTES)),
        )
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_TARGET_ENTITY,
                    default=current[CONF_TARGET_ENTITY],
                ): ENTITY_SELECTOR,
                vol.Required(
                    CONF_DEFAULT_ACTION,
                    default=current[CONF_DEFAULT_ACTION],
                ): ACTION_SELECTOR,
                vol.Required(
                    CONF_DEFAULT_DURATION_MINUTES,
                    default=current[CONF_DEFAULT_DURATION_MINUTES],
                ): _duration_selector(maximum_for_selector),
                vol.Required(
                    CONF_MAX_DURATION_MINUTES,
                    default=current[CONF_MAX_DURATION_MINUTES],
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=10080,
                        step=1,
                        mode=selector.NumberSelectorMode.BOX,
                        unit_of_measurement="min",
                    )
                ),
                vol.Optional(
                    CONF_NOTIFICATION_TARGET,
                    default=current.get(CONF_NOTIFICATION_TARGET, {}),
                ): NOTIFICATION_TARGET_SELECTOR,
                vol.Required(
                    CONF_NOTIFY_MANUAL_CANCEL,
                    default=current[CONF_NOTIFY_MANUAL_CANCEL],
                ): selector.BooleanSelector(),
                vol.Required(
                    CONF_NOTIFY_AUTO_CANCEL,
                    default=current[CONF_NOTIFY_AUTO_CANCEL],
                ): selector.BooleanSelector(),
                vol.Required(
                    CONF_EXECUTE_EXPIRED_TURN_OFF,
                    default=current[CONF_EXECUTE_EXPIRED_TURN_OFF],
                ): selector.BooleanSelector(),
                vol.Required(
                    CONF_EXECUTE_EXPIRED_TURN_ON,
                    default=current[CONF_EXECUTE_EXPIRED_TURN_ON],
                ): selector.BooleanSelector(),
                vol.Required(
                    CONF_CONFIRMATION_TIMEOUT,
                    default=current[CONF_CONFIRMATION_TIMEOUT],
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
        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            errors=errors,
        )

    def _target_is_configured(self, target: str) -> bool:
        for entry in self.hass.config_entries.async_entries(DOMAIN):
            if entry.entry_id == self.config_entry.entry_id:
                continue
            effective = {**entry.data, **entry.options}
            if effective.get(CONF_TARGET_ENTITY) == target:
                return True
        return False
