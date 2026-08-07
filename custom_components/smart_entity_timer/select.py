"""Final-action selector for Smart Entity Timer."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import ACTIONS
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
            [SmartEntityTimerActionSelect(runtime)],
            config_subentry_id=subentry_id,
        )


class SmartEntityTimerActionSelect(SmartEntityTimerEntity, SelectEntity):
    """Choose whether the target will be turned on or off at completion."""

    _attr_icon = "mdi:power-settings"
    _attr_options = list(ACTIONS)
    _attr_translation_key = "end_action"

    def __init__(self, runtime: SmartEntityTimerRuntime) -> None:
        super().__init__(runtime, "end_action")

    @property
    def current_option(self) -> str:
        return self.runtime.selected_action

    @property
    def available(self) -> bool:
        return not self.runtime.is_busy

    async def async_select_option(self, option: str) -> None:
        await self.runtime.async_select_action(option)
