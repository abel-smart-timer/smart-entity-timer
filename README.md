# Smart Entity Timer

Persistent turn-on/turn-off timers for Home Assistant entities.

**Version:** 0.1.3  
**Minimum Home Assistant version:** 2026.7.0  
**Card API:** 2

This repository contains the backend integration used by the companion [Smart Entity Timer Card](https://github.com/abel-smart-timer/smart-entity-timer-card).

## Features

Each configured timer controls one Home Assistant entity and creates five native entities:

- timer status sensor;
- duration number in whole minutes;
- final-action selector (`turn_on` / `turn_off`);
- start button;
- cancel button.

The timer runs inside Home Assistant, so no dashboard or browser must remain open.

- Arbitrary whole-minute durations.
- Turn-on or turn-off final action.
- Manual cancellation.
- Automatic cancellation when the target reaches the requested state early.
- Final race-safe state check before execution.
- Persistent restart restoration.
- Expired OFF timers execute after startup by default.
- Expired ON timers are skipped after startup by default for safety.
- Optional notification targets.
- Multiple independent timers.
- Card API v2 with backend-owned values and constraints.

## Supported domains

`switch`, `light`, `fan`, `climate`, `media_player`, `humidifier`, `input_boolean`, `remote`, and `water_heater`.

## Manual installation

1. Create a Home Assistant backup.
2. Copy `custom_components/smart_entity_timer` to `/config/custom_components/smart_entity_timer`.
3. Restart Home Assistant.
4. Open **Settings → Devices & services → Helpers**.
5. Select **Create helper → Smart Entity Timer**.

Existing 0.1.2 helpers are migrated automatically when 0.1.3 loads.

## Configuration vs options

The controlled target entity is structural configuration. To change it, use **Reconfigure** for the helper/config entry.

Timer preferences remain in **Options**, including default action, default duration, maximum duration, notification targets, restart policies, and confirmation timeout.

This separation follows current Home Assistant config-flow conventions.

## Card API v2

The status sensor is the source of truth for the dashboard card. It publishes data similar to:

```yaml
state: active
attributes:
  target_entity: light.luz_del_bano
  target_entity_name: Luz del baño
  target_entity_state: "on"
  target_state_reached: false
  end_action: turn_off
  duration_minutes: 90
  duration_seconds: 5400
  started_at: "2026-08-07T01:00:00+00:00"
  finishes_at: "2026-08-07T02:30:00+00:00"
  can_start: false
  can_cancel: true
  backend_version: "0.1.3"
  card_api_version: 2
  capabilities:
    - turn_on
    - turn_off
    - set_duration
    - set_action
    - start
    - cancel
  constraints:
    min_seconds: 60
    max_seconds: 86400
    step_seconds: 60
  companion_entities:
    duration: number.luz_del_bano_duracion
    action: select.luz_del_bano_accion
    start: button.luz_del_bano_iniciar
    cancel: button.luz_del_bano_cancelar
```

The companion entity IDs are published for interoperability, but Smart Entity Timer Card 0.1.1 no longer needs to query the Home Assistant entity registry to discover them.

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

Both fields are optional individually; at least one must be supplied.

### Start

```yaml
action: smart_entity_timer.start
target:
  entity_id: sensor.luz_del_bano_estado
```

Optional per-run overrides are still supported:

```yaml
action: smart_entity_timer.start
target:
  entity_id: sensor.luz_del_bano_estado
data:
  duration_minutes: 45
  end_action: turn_on
```

### Cancel

```yaml
action: smart_entity_timer.cancel
target:
  entity_id: sensor.luz_del_bano_estado
```

## Entity naming

Version 0.1.3 adopts Home Assistant's modern `has_entity_name = True` model and translated entity names for all five entities. Existing unique IDs are unchanged, so an upgrade does not intentionally replace the existing entities.

## Validation

The repository includes:

- Python compilation checks;
- dependency-light regression tests for target-state semantics and the card API contract;
- Hassfest;
- HACS validation;
- the manual functional test plan in [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md).

## License

MIT
