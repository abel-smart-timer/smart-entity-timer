"""Smart Entity Timer integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import service

from .const import (
    ACTIONS,
    ATTR_DURATION_MINUTES,
    ATTR_END_ACTION,
    DOMAIN,
    PLATFORMS,
    SERVICE_CANCEL,
    SERVICE_START,
)
from .runtime import SmartEntityTimerRuntime


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Register integration-wide entity services."""
    hass.data.setdefault(DOMAIN, {})

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        SERVICE_START,
        entity_domain="sensor",
        func="async_service_start",
        schema={
            vol.Optional(ATTR_DURATION_MINUTES): vol.All(
                vol.Coerce(int),
                vol.Range(min=1),
            ),
            vol.Optional(ATTR_END_ACTION): vol.In(ACTIONS),
        },
    )
    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        SERVICE_CANCEL,
        entity_domain="sensor",
        func="async_service_cancel",
        schema={},
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up one configured timer."""
    runtime = SmartEntityTimerRuntime(hass, entry)
    entry.runtime_data = runtime
    await runtime.async_initialize()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload one configured timer."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        runtime: SmartEntityTimerRuntime = entry.runtime_data
        await runtime.async_shutdown()
    return unloaded
