"""Smart Entity Timer integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, service
from homeassistant.helpers.typing import ConfigType

from .const import (
    ACTIONS,
    ATTR_DURATION_MINUTES,
    ATTR_END_ACTION,
    CONF_TARGET_ENTITY,
    DOMAIN,
    PLATFORMS,
    SERVICE_CANCEL,
    SERVICE_SET_VALUES,
    SERVICE_START,
)
from .runtime import SmartEntityTimerRuntime

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
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
    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        SERVICE_SET_VALUES,
        entity_domain="sensor",
        func="async_service_set_values",
        schema={
            vol.Optional(ATTR_DURATION_MINUTES): vol.All(
                vol.Coerce(int),
                vol.Range(min=1),
            ),
            vol.Optional(ATTR_END_ACTION): vol.In(ACTIONS),
        },
    )
    return True


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate v0.1.2 entries so structural data lives in config-entry data."""
    if entry.version == 1 and entry.minor_version < 2:
        data = dict(entry.data)
        options = dict(entry.options)
        if CONF_TARGET_ENTITY in options:
            data[CONF_TARGET_ENTITY] = options.pop(CONF_TARGET_ENTITY)
        hass.config_entries.async_update_entry(
            entry,
            data=data,
            options=options,
            version=1,
            minor_version=2,
        )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up one configured timer."""
    runtime = SmartEntityTimerRuntime(hass, entry)
    entry.runtime_data = runtime
    await runtime.async_initialize()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # All companion entities are now registered; republish Card API v2 attributes.
    runtime.async_publish_state()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload one configured timer."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        runtime: SmartEntityTimerRuntime = entry.runtime_data
        await runtime.async_shutdown()
    return unloaded
