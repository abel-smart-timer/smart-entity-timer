"""Diagnostics support for Smart Entity Timer."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_NOTIFICATION_TARGET
from .runtime import SmartEntityTimerRuntime


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict:
    """Return non-sensitive diagnostics for one timer."""
    runtime: SmartEntityTimerRuntime = entry.runtime_data
    data = {**entry.data, **entry.options}
    data.pop(CONF_NOTIFICATION_TARGET, None)
    return {
        "config": data,
        "runtime": runtime.diagnostics(),
        "notification_target_configured": bool(runtime.notification_target),
    }
