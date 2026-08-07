"""Base entities for Smart Entity Timer."""

from __future__ import annotations

from collections.abc import Callable

from homeassistant.helpers.entity import Entity

from .runtime import SmartEntityTimerRuntime


class SmartEntityTimerEntity(Entity):
    """Base class connected directly to one timer runtime."""

    _attr_should_poll = False
    _attr_has_entity_name = True

    def __init__(self, runtime: SmartEntityTimerRuntime, key: str) -> None:
        self.runtime = runtime
        self._attr_unique_id = f"{runtime.entry.entry_id}_{key}"
        # Keep the configured helper title in the translated entity name while
        # following Home Assistant's modern has_entity_name convention.
        self._attr_translation_placeholders = {"timer_name": runtime.entry.title}
        self._remove_runtime_listener: Callable[[], None] | None = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self._remove_runtime_listener = self.runtime.async_add_listener(
            self._handle_runtime_update
        )

    async def async_will_remove_from_hass(self) -> None:
        if self._remove_runtime_listener is not None:
            self._remove_runtime_listener()
            self._remove_runtime_listener = None
        await super().async_will_remove_from_hass()

    def _handle_runtime_update(self) -> None:
        self.async_write_ha_state()
