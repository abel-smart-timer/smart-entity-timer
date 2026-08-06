"""Start and cancel buttons for Smart Entity Timer."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
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
    async_add_entities(
        [
            SmartEntityTimerStartButton(runtime),
            SmartEntityTimerCancelButton(runtime),
        ]
    )


class SmartEntityTimerStartButton(SmartEntityTimerEntity, ButtonEntity):
    """Start the configured timer."""

    _attr_icon = "mdi:timer-play-outline"

    def __init__(self, runtime: SmartEntityTimerRuntime) -> None:
        super().__init__(runtime, "start", "Iniciar", "Start")

    @property
    def available(self) -> bool:
        return self.runtime.can_start

    async def async_press(self) -> None:
        await self.runtime.async_start()


class SmartEntityTimerCancelButton(SmartEntityTimerEntity, ButtonEntity):
    """Cancel an active timer."""

    _attr_icon = "mdi:timer-cancel-outline"

    def __init__(self, runtime: SmartEntityTimerRuntime) -> None:
        super().__init__(runtime, "cancel", "Cancelar", "Cancel")

    @property
    def available(self) -> bool:
        return self.runtime.can_cancel

    async def async_press(self) -> None:
        await self.runtime.async_cancel()
