# Smart Entity Timer

Persistent turn-on/turn-off timers for Home Assistant entities.

**Version:** 0.3.0  
**Minimum Home Assistant version:** 2026.7.0  
**Card API:** 2  
**Recommended card:** [Smart Entity Timer Card 0.2.2 or newer](https://github.com/abel-smart-timer/smart-entity-timer-card)

## What changes in 0.3.0

Smart Entity Timer is now modeled as **one Home Assistant integration entry with one config subentry per timer**.

```text
Smart Entity Timer
├── Bathroom light timer
├── Air conditioner timer
├── Bedroom fan timer
└── Water heater timer
```

This replaces the old 0.2.x model where every timer was an independent Helper config entry.

The practical result is a more intuitive UI:

- Smart Entity Timer is managed from **Settings → Devices & services → Integrations**.
- The integration has a single parent entry.
- Use **Add timer** to create additional timer subentries.
- Reconfigure each timer directly from the Smart Entity Timer integration page.
- All timer preferences, notification templates, target entity, and restart settings are managed in that timer's reconfigure flow.

The manifest uses `integration_type: hub` because the single parent entry manages multiple timer services, and `single_config_entry: true` prevents accidental duplicate parent entries.

## Upgrade from 0.2.x

On the first Home Assistant start with 0.3.0, existing Smart Entity Timer 0.1.x/0.2.x entries are consolidated automatically:

```text
Before
ConfigEntry A → Bathroom light
ConfigEntry B → Air conditioner
ConfigEntry C → Bedroom fan

After
Smart Entity Timer parent
├── Subentry → Bathroom light
├── Subentry → Air conditioner
└── Subentry → Bedroom fan
```

The migration preserves:

- existing `entity_id` values;
- existing entity `unique_id` values;
- timer persistent-storage keys;
- configured target entities and preferences;
- personalized notification templates;
- dashboard cards and automations that reference the existing status sensor.

For migrated timers, the old config-entry ID becomes the timer's stable internal ID. New 0.3.x timers use their config-subentry ID as their stable timer ID.

### Important upgrade procedure

Before upgrading from 0.2.x to 0.3.0:

1. **Wait for every active timer to finish or cancel it.** Do not update while any Smart Entity Timer is active or executing.
2. Create a Home Assistant backup.
3. Install/update Smart Entity Timer.
4. Restart Home Assistant.
5. Open **Settings → Devices & services → Integrations → Smart Entity Timer** and verify that all previous timers appear under the single integration entry.

Updating while a timer is active is not part of the supported upgrade procedure for the 0.2.x → 0.3.0 topology migration.

## Existing timer behavior remains unchanged

Each timer still creates five native entities:

- timer status sensor;
- duration number in whole minutes;
- final-action selector (`turn_on` / `turn_off`);
- start button;
- cancel button.

The timer still runs entirely in Home Assistant, so no dashboard or browser must remain open.

- Arbitrary whole-minute durations.
- Turn-on or turn-off final action.
- Manual cancellation.
- Automatic cancellation when the target reaches the requested state early.
- Final race-safe state check before execution.
- Persistent restart restoration during normal Home Assistant restarts.
- Expired OFF timers execute after startup by default.
- Expired ON timers are skipped after startup by default for safety.
- Personalized lifecycle notifications.
- Lifecycle events for advanced automations.
- Multiple independent timers.
- Card API v2.

## Supported domains

`switch`, `light`, `fan`, `climate`, `media_player`, `humidifier`, `input_boolean`, `remote`, and `water_heater`.

## Notifications

0.3.0 keeps the notification customization introduced in 0.2.0. Custom title/message fields support:

`{timer_name}`, `{target_name}`, `{target_entity}`, `{action}`, `{action_id}`, `{action_past}`, `{duration}`, `{duration_minutes}`, `{result}`, `{reason}`, `{finished_at}`, `{restored}`, `{default_title}`, `{default_message}`.

Leave a custom field blank to preserve the built-in message. The available variables and examples are also shown directly in the timer configuration UI.

## Lifecycle events

The public event contract remains:

- `smart_entity_timer.started`
- `smart_entity_timer.completed`
- `smart_entity_timer.cancelled`
- `smart_entity_timer.skipped`
- `smart_entity_timer.error`

## Card API v2 compatibility

Card API remains version 2. Smart Entity Timer Card 0.2.2 continues working without changes, including existing cards that point to migrated sensor entity IDs.

The status sensor remains the source of truth for the dashboard card and publishes `capabilities`, `constraints`, `companion_entities`, duration, action, timestamps, and timer lifecycle data.

## Actions

### Set duration and/or action while idle

```yaml
action: smart_entity_timer.set_values
target:
  entity_id: sensor.luz_del_bano_estado
data:
  duration_minutes: 75
  end_action: turn_off
```

### Start

```yaml
action: smart_entity_timer.start
target:
  entity_id: sensor.luz_del_bano_estado
```

### Cancel

```yaml
action: smart_entity_timer.cancel
target:
  entity_id: sensor.luz_del_bano_estado
```

## Installation

### HACS (recommended)

Install or update **Smart Entity Timer** from HACS and restart Home Assistant when requested.

For an upgrade from 0.2.x, first follow the upgrade procedure above: stop/cancel all timers and create a backup.

### Manual installation

1. Create a Home Assistant backup.
2. Ensure all Smart Entity Timer timers are idle if upgrading from 0.2.x.
3. Copy `custom_components/smart_entity_timer` into `/config/custom_components/smart_entity_timer`.
4. Replace the existing files when upgrading.
5. Restart Home Assistant.
6. Open **Settings → Devices & services → Integrations → Smart Entity Timer**.

Do not delete existing 0.2.x helpers before the first 0.3.0 start; they are the migration input.

## Validation

0.3.0 was validated on real Home Assistant installations for:

- clean installation on Raspberry Pi 5;
- adding multiple timers under one parent integration;
- centralized timer reconfiguration;
- blocking add/reconfigure while any timer is active;
- deleting one timer without affecting the others;
- migration of one and multiple 0.2.0 timers;
- preservation of existing entity IDs;
- Smart Entity Timer Card 0.2.2 compatibility;
- personalized notifications and lifecycle events after migration.

The repository also includes Python compilation, dependency-light regression tests, Hassfest, HACS validation, and a manual functional/migration test plan.

## License

MIT
