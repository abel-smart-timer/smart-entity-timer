"""Duration number for Smart Entity Timer."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .entity import SmartEntityTimerEntity
from .runtime import SmartEntityTimerRuntime


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    runtime: SmartEntityTimerRuntime = entry.runtime_data
    async_add_entities([SmartEntityTimerDurationNumber(runtime)])


class SmartEntityTimerDurationNumber(SmartEntityTimerEntity, NumberEntity):
    """Arbitrary timer duration in whole minutes."""

    _attr_icon = "mdi:timer-edit-outline"
    _attr_native_min_value = 1
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_mode = NumberMode.BOX

    def __init__(self, runtime: SmartEntityTimerRuntime) -> None:
        super().__init__(runtime, "duration", "Duración", "Duration")

    @property
    def native_value(self) -> float:
        return float(self.runtime.selected_duration_minutes)

    @property
    def native_max_value(self) -> float:
        return float(self.runtime.max_duration_minutes)

    @property
    def available(self) -> bool:
        return not self.runtime.is_busy

    async def async_set_native_value(self, value: float) -> None:
        await self.runtime.async_set_duration(int(round(value)))
