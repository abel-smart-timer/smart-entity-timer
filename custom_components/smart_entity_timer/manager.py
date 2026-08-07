"""Parent config-entry manager for Smart Entity Timer config subentries."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from homeassistant.config_entries import ConfigEntry, ConfigSubentry
from homeassistant.core import HomeAssistant

from .const import CONF_TIMER_ID, SUBENTRY_TYPE_TIMER
from .runtime import SmartEntityTimerRuntime


@dataclass(slots=True)
class SmartEntityTimerRuntimeConfig:
    """Compatibility view exposing one timer subentry like the legacy config entry.

    The mature runtime from 0.2.x intentionally keeps using ``entry_id``, ``title``,
    ``data`` and ``options``.  This adapter lets 0.3.x move configuration into
    config subentries without changing persistent-store keys or entity unique IDs.
    """

    parent_entry: ConfigEntry
    subentry: ConfigSubentry

    @property
    def entry_id(self) -> str:
        """Return the stable timer identity used by storage and entity unique IDs."""
        return str(self.subentry.data.get(CONF_TIMER_ID) or self.subentry.subentry_id)

    @property
    def title(self) -> str:
        """Return the timer display name."""
        return self.subentry.title

    @property
    def data(self) -> Mapping[str, Any]:
        """Return timer configuration."""
        return self.subentry.data

    @property
    def options(self) -> Mapping[str, Any]:
        """Keep the legacy runtime merge contract; subentries store one data mapping."""
        return MappingProxyType({})

    @property
    def config_entry_id(self) -> str:
        """Return the owning parent config-entry id."""
        return self.parent_entry.entry_id

    @property
    def config_subentry_id(self) -> str:
        """Return the owning timer subentry id."""
        return self.subentry.subentry_id


class SmartEntityTimerManager:
    """Own all timer runtimes under the single Smart Entity Timer config entry."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self.runtimes: dict[str, SmartEntityTimerRuntime] = {}

    async def async_initialize(self) -> None:
        """Initialize every configured timer subentry."""
        initialized: list[SmartEntityTimerRuntime] = []
        try:
            for subentry in self.entry.subentries.values():
                if subentry.subentry_type != SUBENTRY_TYPE_TIMER:
                    continue
                config = SmartEntityTimerRuntimeConfig(self.entry, subentry)
                runtime = SmartEntityTimerRuntime(self.hass, config)
                await runtime.async_initialize()
                self.runtimes[subentry.subentry_id] = runtime
                initialized.append(runtime)
        except Exception:
            for runtime in reversed(initialized):
                await runtime.async_shutdown()
            self.runtimes.clear()
            raise

    async def async_shutdown(self) -> None:
        """Stop all timer runtimes."""
        for runtime in tuple(self.runtimes.values()):
            await runtime.async_shutdown()
        self.runtimes.clear()

    @property
    def is_busy(self) -> bool:
        """Return True when any child timer is active or executing."""
        return any(runtime.is_busy for runtime in self.runtimes.values())

    def runtime_for_subentry(self, subentry_id: str) -> SmartEntityTimerRuntime | None:
        """Return one runtime by config-subentry id."""
        return self.runtimes.get(subentry_id)

    def iter_runtimes(self):
        """Iterate ``(subentry_id, runtime)`` pairs in stored order."""
        return self.runtimes.items()

    def async_publish_states(self) -> None:
        """Republish Card API attributes after entities have entered the registry."""
        for runtime in self.runtimes.values():
            runtime.async_publish_state()
