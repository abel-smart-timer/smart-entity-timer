"""Architecture migration helpers for Smart Entity Timer 0.3.x."""

from __future__ import annotations

import logging
from types import MappingProxyType
from typing import Any

from homeassistant.config_entries import ConfigEntry, ConfigSubentry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import (
    ARCHITECTURE_SUBENTRIES_V1,
    CONF_ARCHITECTURE,
    CONF_TARGET_ENTITY,
    CONF_TIMER_ID,
    CONFIG_ENTRY_VERSION,
    DOMAIN,
    NAME,
    SUBENTRY_TYPE_TIMER,
)

_LOGGER = logging.getLogger(__name__)


def is_parent_entry(entry: ConfigEntry) -> bool:
    """Return True when an entry already uses the 0.3.x parent/subentry model."""
    return (
        entry.data.get(CONF_ARCHITECTURE) == ARCHITECTURE_SUBENTRIES_V1
        or any(
            subentry.subentry_type == SUBENTRY_TYPE_TIMER
            for subentry in entry.subentries.values()
        )
    )


def legacy_timer_data(entry: ConfigEntry) -> dict[str, Any]:
    """Flatten legacy config-entry data/options into one timer subentry mapping."""
    data = {**entry.data, **entry.options}
    # 0.1.2 could temporarily keep the structural target in options; the merge above
    # intentionally lets options win before the legacy mappings are discarded.
    data.pop(CONF_ARCHITECTURE, None)
    data[CONF_TIMER_ID] = entry.entry_id
    return data


async def async_consolidate_legacy_entries(hass: HomeAssistant) -> ConfigEntry | None:
    """Merge 0.1.x/0.2.x one-timer entries into one parent with timer subentries.

    This runs from integration ``async_setup``. Home Assistant runs normal integration
    setup before config-entry setup, so the registry associations can be moved before
    any Smart Entity Timer entry creates runtime objects for this boot.
    """
    entries = list(hass.config_entries.async_entries(DOMAIN))
    if not entries:
        return None

    parents = [entry for entry in entries if is_parent_entry(entry)]
    if len(parents) > 1:
        _LOGGER.error(
            "Smart Entity Timer found multiple 0.3.x parent entries; refusing automatic "
            "consolidation to avoid data loss"
        )
        return parents[0]

    if parents:
        parent = parents[0]
    else:
        parent = min(entries, key=lambda item: (item.created_at, item.entry_id))

    existing_timer_ids = {
        str(subentry.data.get(CONF_TIMER_ID) or "")
        for subentry in parent.subentries.values()
        if subentry.subentry_type == SUBENTRY_TYPE_TIMER
    }
    existing_targets = {
        str(subentry.data.get(CONF_TARGET_ENTITY) or "")
        for subentry in parent.subentries.values()
        if subentry.subentry_type == SUBENTRY_TYPE_TIMER
    }

    entity_registry = er.async_get(hass)
    legacy_entries = [entry for entry in entries if not is_parent_entry(entry)]
    # If the selected parent itself is legacy, include it first so its existing entity
    # registry entries only need a subentry association, not a config-entry move.
    if not is_parent_entry(parent):
        legacy_entries = [parent, *[entry for entry in legacy_entries if entry is not parent]]

    migrated: list[tuple[ConfigEntry, ConfigSubentry]] = []
    for legacy in legacy_entries:
        timer_data = legacy_timer_data(legacy)
        target = str(timer_data.get(CONF_TARGET_ENTITY) or "")
        timer_id = legacy.entry_id

        if timer_id in existing_timer_ids:
            continue
        if target and target in existing_targets:
            _LOGGER.error(
                "Cannot migrate timer %s because target %s already exists in the parent "
                "entry",
                legacy.title,
                target,
            )
            continue

        subentry = ConfigSubentry(
            data=MappingProxyType(timer_data),
            subentry_type=SUBENTRY_TYPE_TIMER,
            title=legacy.title,
            unique_id=target or timer_id,
        )
        hass.config_entries.async_add_subentry(parent, subentry)
        existing_timer_ids.add(timer_id)
        if target:
            existing_targets.add(target)
        migrated.append((legacy, subentry))

        # Keep every entity_id and unique_id exactly as it was. Only registry ownership
        # changes from the legacy timer config entry to the parent + timer subentry.
        for entity in er.async_entries_for_config_entry(
            entity_registry, legacy.entry_id
        ):
            entity_registry.async_update_entity(
                entity.entity_id,
                config_entry_id=parent.entry_id,
                config_subentry_id=subentry.subentry_id,
            )

    if migrated or not is_parent_entry(parent):
        hass.config_entries.async_update_entry(
            parent,
            title=NAME,
            unique_id=DOMAIN,
            data={CONF_ARCHITECTURE: ARCHITECTURE_SUBENTRIES_V1},
            options={},
            version=CONFIG_ENTRY_VERSION,
            minor_version=0,
        )

    # Remove legacy entries only after their entities point at the parent. The parent
    # itself is repurposed and therefore must stay.
    for legacy, _subentry in migrated:
        if legacy.entry_id == parent.entry_id:
            continue
        _LOGGER.info(
            "Migrated legacy Smart Entity Timer '%s' (%s) into parent entry %s",
            legacy.title,
            legacy.entry_id,
            parent.entry_id,
        )
        await hass.config_entries.async_remove(legacy.entry_id)

    return parent
