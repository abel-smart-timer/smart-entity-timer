"""Status sensor for Smart Entity Timer."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    ACTION_TURN_ON,
    ATTR_DURATION_MINUTES,
    ATTR_END_ACTION,
    STATUS_ACTIVE,
    STATUS_ERROR,
    STATUS_EXECUTING,
)
from .entity import SmartEntityTimerEntity
from .manager import SmartEntityTimerManager
from .runtime import SmartEntityTimerRuntime


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    manager: SmartEntityTimerManager = entry.runtime_data
    for subentry_id, runtime in manager.iter_runtimes():
        async_add_entities(
            [SmartEntityTimerStatusSensor(runtime)],
            config_subentry_id=subentry_id,
        )


class SmartEntityTimerStatusSensor(SmartEntityTimerEntity, SensorEntity):
    """Main status entity and service target for a configured timer."""

    _attr_translation_key = "status"

    def __init__(self, runtime: SmartEntityTimerRuntime) -> None:
        super().__init__(runtime, "status")

    @property
    def native_value(self) -> str:
        return self.runtime.status

    @property
    def extra_state_attributes(self) -> dict:
        return self.runtime.state_attributes()

    @property
    def icon(self) -> str:
        if self.runtime.status == STATUS_ACTIVE:
            return "mdi:timer-sand"
        if self.runtime.status == STATUS_EXECUTING:
            return "mdi:timer-cog-outline"
        if self.runtime.status == STATUS_ERROR:
            return "mdi:timer-alert-outline"
        if self.runtime.selected_action == ACTION_TURN_ON:
            return "mdi:timer-play-outline"
        return "mdi:timer-off-outline"

    async def async_service_start(self, **service_data) -> None:
        await self.runtime.async_start(
            duration_minutes=service_data.get(ATTR_DURATION_MINUTES),
            end_action=service_data.get(ATTR_END_ACTION),
        )

    async def async_service_cancel(self) -> None:
        await self.runtime.async_cancel()

    async def async_service_set_values(self, **service_data) -> None:
        await self.runtime.async_set_values(
            duration_minutes=service_data.get(ATTR_DURATION_MINUTES),
            end_action=service_data.get(ATTR_END_ACTION),
        )
