"""Start and cancel buttons for Smart Entity Timer."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

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
            [
                SmartEntityTimerStartButton(runtime),
                SmartEntityTimerCancelButton(runtime),
            ],
            config_subentry_id=subentry_id,
        )


class SmartEntityTimerStartButton(SmartEntityTimerEntity, ButtonEntity):
    """Start the configured timer."""

    _attr_icon = "mdi:timer-play-outline"
    _attr_translation_key = "start"

    def __init__(self, runtime: SmartEntityTimerRuntime) -> None:
        super().__init__(runtime, "start")

    @property
    def available(self) -> bool:
        return self.runtime.can_start

    async def async_press(self) -> None:
        await self.runtime.async_start()


class SmartEntityTimerCancelButton(SmartEntityTimerEntity, ButtonEntity):
    """Cancel an active timer."""

    _attr_icon = "mdi:timer-cancel-outline"
    _attr_translation_key = "cancel"

    def __init__(self, runtime: SmartEntityTimerRuntime) -> None:
        super().__init__(runtime, "cancel")

    @property
    def available(self) -> bool:
        return self.runtime.can_cancel

    async def async_press(self) -> None:
        await self.runtime.async_cancel()
