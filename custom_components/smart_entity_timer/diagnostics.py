"""Diagnostics support for Smart Entity Timer."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_NOTIFICATION_TARGET,
    NOTIFICATION_TEMPLATE_CONFIG_KEYS,
    SUBENTRY_TYPE_TIMER,
)
from .manager import SmartEntityTimerManager


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict:
    """Return non-sensitive diagnostics for the parent and all timer subentries."""
    manager: SmartEntityTimerManager = entry.runtime_data
    timers: list[dict] = []

    for subentry_id, runtime in manager.iter_runtimes():
        subentry = entry.subentries[subentry_id]
        if subentry.subentry_type != SUBENTRY_TYPE_TIMER:
            continue
        data = dict(subentry.data)
        notification_target_configured = bool(data.pop(CONF_NOTIFICATION_TARGET, {}))
        custom_templates_configured = {
            key: bool(data.pop(key, "")) for key in NOTIFICATION_TEMPLATE_CONFIG_KEYS
        }
        timers.append(
            {
                "subentry_id": subentry_id,
                "title": subentry.title,
                "config": data,
                "runtime": runtime.diagnostics(),
                "notification_target_configured": notification_target_configured,
                "custom_notification_templates_configured": (
                    custom_templates_configured
                ),
            }
        )

    return {
        "parent": {
            "entry_id": entry.entry_id,
            "title": entry.title,
            "version": entry.version,
            "minor_version": entry.minor_version,
            "data": dict(entry.data),
            "timer_count": len(timers),
        },
        "timers": timers,
    }
