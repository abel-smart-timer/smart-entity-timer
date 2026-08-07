"""Smart Entity Timer integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, service
from homeassistant.helpers.typing import ConfigType

from .const import (
    ACTIONS,
    ARCHITECTURE_SUBENTRIES_V1,
    ATTR_DURATION_MINUTES,
    ATTR_END_ACTION,
    CONF_ARCHITECTURE,
    CONFIG_ENTRY_VERSION,
    DOMAIN,
    PLATFORMS,
    SERVICE_CANCEL,
    SERVICE_SET_VALUES,
    SERVICE_START,
)
from .manager import SmartEntityTimerManager
from .migration import async_consolidate_legacy_entries

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Prepare topology migration and register integration-wide entity services."""
    # Home Assistant performs normal integration setup before config-entry setup. This
    # gives 0.3.x a safe window to consolidate legacy one-timer config entries into the
    # new single parent + config-subentry topology before any timer runtime is loaded.
    await async_consolidate_legacy_entries(hass)

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
    """Migrate legacy per-timer entries to the 0.3.x parent/subentry architecture."""
    if entry.version < CONFIG_ENTRY_VERSION:
        await async_consolidate_legacy_entries(hass)
        current = hass.config_entries.async_get_entry(entry.entry_id)
        # A non-parent legacy entry can be removed by consolidation. That is expected;
        # its entities and configuration now belong to the selected parent entry.
        if current is None:
            return True
        return (
            current.version == CONFIG_ENTRY_VERSION
            and current.data.get(CONF_ARCHITECTURE) == ARCHITECTURE_SUBENTRIES_V1
        )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the single parent entry and all configured timer subentries."""
    manager = SmartEntityTimerManager(hass, entry)
    entry.runtime_data = manager
    await manager.async_initialize()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # All companion entities are now registered; republish Card API v2 attributes.
    manager.async_publish_states()
    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))
    return True


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the parent when timer subentries are added, changed, or removed."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload all timers owned by the parent entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        manager: SmartEntityTimerManager = entry.runtime_data
        await manager.async_shutdown()
    return unloaded
