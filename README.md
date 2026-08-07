# Smart Entity Timer

Persistent turn-on/turn-off timers for Home Assistant entities.

**Development candidate:** 0.2.0  
**Current stable release:** 0.1.3  
**Minimum Home Assistant version:** 2026.7.0  
**Card API:** 2

This repository contains the backend integration used by the companion [Smart Entity Timer Card](https://github.com/abel-smart-timer/smart-entity-timer-card). Smart Entity Timer Card 0.2.2 remains compatible with backend 0.2.0 because Card API stays at version 2.

## Core timer features

- Arbitrary whole-minute durations.
- Turn-on or turn-off final action.
- Manual cancellation.
- Automatic cancellation when the target reaches the requested state early.
- Race-safe final state check before execution.
- Persistent restart restoration.
- Expired OFF timers execute after startup by default.
- Expired ON timers are skipped after startup by default for safety.
- Multiple independent timers.
- Optional notification destinations.
- Card API v2 synchronization across dashboards.

## New in 0.2.0: customizable notifications

The existing notification behavior remains the default. In **Helper options**, each title/message field can be left blank or customized independently for:

- normal completion;
- errors;
- actions skipped after restart;
- manual cancellation;
- automatic cancellation.

Manual and automatic cancellation notifications still respect their existing enable/disable switches.

### Available placeholders

Custom notification text uses a deliberately small, safe placeholder system rather than arbitrary Jinja templates:

| Placeholder | Meaning |
|---|---|
| `{timer_name}` | Smart Entity Timer helper/config-entry name |
| `{target_name}` | Friendly name of the controlled entity |
| `{target_entity}` | Entity ID |
| `{action}` | Localized action, such as `encender` / `apagar` |
| `{action_id}` | Stable value `turn_on` / `turn_off` |
| `{action_past}` | Localized completed action |
| `{duration}` | Localized duration |
| `{duration_minutes}` | Duration as an integer |
| `{result}` | Stable result value |
| `{reason}` | Stable reason value, when present |
| `{finished_at}` | Local finish timestamp |
| `{restored}` | Localized yes/no indicating restored execution |
| `{default_title}` | Built-in localized notification title |
| `{default_message}` | Built-in localized notification message |

Example:

```text
Title: Temporizador de {target_name}
Message: {target_name} fue {action_past} después de {duration}.
```

If either custom field is empty, that field keeps the normal built-in localized text. Invalid placeholders are rejected by the options flow. The Helper options screen also shows the full placeholder list near the notification fields and a practical example below each title/message field, so users do not need to keep the README open while configuring notifications.

## New in 0.2.0: lifecycle events

Automations can listen for:

```text
smart_entity_timer.started
smart_entity_timer.completed
smart_entity_timer.cancelled
smart_entity_timer.skipped
smart_entity_timer.error
```

The `cancelled` event covers both manual and automatic cancellation; inspect `result` and `reason` to distinguish them.

Typical event data:

```yaml
event_schema_version: 1
entry_id: abc123
timer_name: Temporizador baño
target_entity: light.luz_del_bano
target_name: Luz del baño
target_state: "off"
action: turn_off
duration_minutes: 30
result: completed
reason: null
restored: false
finished_at: "2026-08-07T19:00:00+00:00"
event_time: "2026-08-07T19:00:00+00:00"
```

These events make it possible to build custom automations, alternate notification systems, logging, announcements, dashboards, or integrations without adding product-specific options to Smart Entity Timer.

## Supported domains

`switch`, `light`, `fan`, `climate`, `media_player`, `humidifier`, `input_boolean`, `remote`, and `water_heater`.

## Installation for 0.2.0 testing

Version 0.1.3 remains the current stable release. Test 0.2.0 manually before publishing a new GitHub Release.

1. Create a Home Assistant backup.
2. Copy `custom_components/smart_entity_timer` to `/config/custom_components/smart_entity_timer`.
3. Replace the existing 0.1.3 files.
4. Restart Home Assistant.
5. Existing helpers should remain in place; do not delete them.
6. Confirm `backend_version: 0.2.0` and `card_api_version: 2` on the status sensor.

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

## Compatibility

- Existing 0.1.3 config entries require no destructive migration.
- Existing notification targets and cancellation-notification switches keep their meaning.
- Empty custom notification fields preserve all 0.1.3 notification wording.
- Card API remains `2`; no Smart Entity Timer Card update is required.

## Validation

The repository includes Python compilation checks, dependency-light unit tests, Hassfest, HACS validation, and the manual test plan in [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md).

## License

MIT
