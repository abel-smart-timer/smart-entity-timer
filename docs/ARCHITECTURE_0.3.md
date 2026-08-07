# Smart Entity Timer 0.3 architecture

## Goal

Expose Smart Entity Timer as one normal integration entry and manage individual timers as Home Assistant config subentries.

## Topology

```text
ConfigEntry: Smart Entity Timer
└── runtime_data: SmartEntityTimerManager
    ├── ConfigSubentry(timer): Bathroom light → SmartEntityTimerRuntime
    ├── ConfigSubentry(timer): Air conditioner → SmartEntityTimerRuntime
    └── ConfigSubentry(timer): Bedroom fan → SmartEntityTimerRuntime
```

Each platform registers its entities with the parent `config_entry_id` and the relevant `config_subentry_id`.

## Stable timer identity

The mature 0.2.x timer runtime uses one stable ID for:

- persistent storage key;
- entity unique-ID prefix;
- Card API companion-entity lookup;
- lifecycle event `entry_id` field.

0.3.0 keeps that contract through `SmartEntityTimerRuntimeConfig`:

- migrated timer → old config-entry ID;
- newly created 0.3 timer → config-subentry ID.

This allows topology migration without deliberately changing existing entity IDs or storage files.

## Legacy consolidation

The integration's normal `async_setup` runs before config-entry setup. During that phase 0.3.0:

1. finds all legacy Smart Entity Timer config entries;
2. chooses the oldest entry as the new parent;
3. creates one `timer` config subentry for every legacy timer;
4. flattens legacy `data + options` into the timer subentry;
5. stores the old config-entry ID as `timer_id`;
6. moves existing entity-registry ownership to the parent + timer subentry without changing entity IDs or unique IDs;
7. marks the parent as `subentries_v1` architecture;
8. removes the now-empty extra legacy config entries.

The component creates no Smart Entity Timer devices, so 0.3.0 has no device-registry migration requirement.

## Reload model

Adding, reconfiguring, or removing a timer changes the parent's `subentries` mapping. A config-entry update listener reloads the parent so every platform sees the new set of timers.

The add/reconfigure flows block configuration changes while any timer is active or executing, avoiding a planned parent reload during an active countdown.

## Compatibility goals

0.3.0 intentionally keeps:

- Card API v2;
- status/number/select/button entity unique-ID format;
- current entity services;
- restart persistence;
- notification templates;
- lifecycle events;
- Smart Entity Timer Card 0.2.2 compatibility.
