# Smart Entity Timer

Persistent turn-on/turn-off timers for Home Assistant entities.

**Version:** 0.1.1  
**Minimum Home Assistant version:** 2026.7.0

This repository contains the backend integration. The visual Lovelace card will be developed after functional testing of this release.

## What version 0.1.1 does

Each configuration entry controls one entity and creates:

- one status sensor;
- one duration number in whole minutes;
- one final-action selector (`turn_on` / `turn_off`);
- one start button;
- one cancel button.

The timer runs inside Home Assistant, so the dashboard or mobile application does not need to remain open.

### Required behavior included

- The target can be turned **on or off**, selected before starting.
- Any whole-minute duration can be entered. The future card will add **−30 / +30 minute** shortcuts without limiting arbitrary input.
- If an OFF timer is active and the entity is turned off early, the timer cancels automatically.
- If an ON timer is active and the entity is turned on early, the timer cancels automatically.
- The early state change can come from the physical control, Home Assistant, the manufacturer's application, an automation, or another integration.
- The backend rechecks the state immediately before running the final action to avoid race conditions.
- A timer cannot start if the entity is unavailable or already in the requested final state.
- Active timers are restored after a Home Assistant restart.
- By default, an expired OFF timer is executed after startup, while an expired ON timer is skipped for safety.
- Notifications can target one or more Home Assistant notify entities, devices, or areas containing notify entities.

## Supported entity domains in 0.1.1

- `switch`
- `light`
- `fan`
- `climate`
- `media_player`
- `humidifier`
- `input_boolean`
- `remote`
- `water_heater`

Covers, locks, sirens, alarms, valves, and other domains are intentionally excluded until their state and safety semantics are designed and tested separately.

## Manual installation

1. Create a Home Assistant backup.
2. Extract the installation ZIP into the Home Assistant `/config` directory.
3. Confirm that this path exists:

   ```text
   /config/custom_components/smart_entity_timer/manifest.json
   ```

4. Restart Home Assistant.
5. Open **Settings → Devices & services → Add integration**.
6. Search for **Smart Entity Timer**.
7. Create one timer for each entity that needs this function.

The integration does not require YAML helpers.

## Entities created per timer

Assuming the entry is named `Temporizador A/C Cocina`, Home Assistant creates entities similar to:

```text
sensor.temporizador_a_c_cocina_estado
number.temporizador_a_c_cocina_duracion
select.temporizador_a_c_cocina_accion
button.temporizador_a_c_cocina_iniciar
button.temporizador_a_c_cocina_cancelar
```

Actual entity IDs are assigned by Home Assistant and may differ.

The entity named **Estado del temporizador** reports the timer lifecycle (`idle`, `active`, `executing`, or `error`); it is not a duplicate of the controlled light or switch. Its attributes publish the controlled entity state and stable data for the future card:

```yaml
state: active
attributes:
  target_entity: climate.ac_cocina
  target_entity_name: A/C Cocina
  target_entity_state: cool
  target_state_reached: false
  end_action: turn_off
  duration_minutes: 90
  duration_seconds: 5400
  started_at: "2026-08-05T04:00:00+00:00"
  finishes_at: "2026-08-05T05:30:00+00:00"
  can_start: false
  can_cancel: true
  backend_version: "0.1.1"
  card_api_version: 1
```

The future card will calculate the countdown and progress bar locally from `started_at`, `finishes_at`, and `duration_seconds`, avoiding a Home Assistant state update every second.

## Actions

The integration registers entity actions against its status sensor.

### Start with the selected duration and action

```yaml
action: smart_entity_timer.start
target:
  entity_id: sensor.temporizador_a_c_cocina_estado
```

### Start with optional overrides

```yaml
action: smart_entity_timer.start
target:
  entity_id: sensor.temporizador_a_c_cocina_estado
data:
  duration_minutes: 75
  end_action: turn_off
```

### Cancel

```yaml
action: smart_entity_timer.cancel
target:
  entity_id: sensor.temporizador_a_c_cocina_estado
```

Cancelling does not execute the final action.

## Notification behavior

Default behavior:

| Result | Notification |
|---|---:|
| Timer finishes and action is confirmed | Yes |
| Action fails or target is unavailable | Yes |
| Expired ON action is skipped after restart | Yes |
| Manual cancellation | No |
| Automatic cancellation because target state was reached early | No |

Manual and automatic cancellation notifications can be enabled in the integration options.

## Restart behavior

The runtime stores absolute UTC start and finish timestamps.

- If Home Assistant restarts before expiry, the remaining time is reconstructed.
- If an OFF timer expired while Home Assistant was offline, the default is to execute it at startup.
- If an ON timer expired while Home Assistant was offline, the default is to skip it and notify, preventing unexpected activation after a long outage.
- Both policies are configurable per timer.

## Development status

Version 0.1.1 is the current backend test release. It adds a one-second in-memory watchdog while a timer is active, so early target-state changes are detected even if an integration does not deliver the expected state-change callback. It still requires the complete functional Home Assistant test plan before the card is developed.

See:

- [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md)
- [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md)
- [`CHANGELOG.md`](CHANGELOG.md)

## Repository

Official source repository:

```text
https://github.com/abel-smart-timer/smart-entity-timer
```

This package is already prepared for the `abel-smart-timer` GitHub organization. The `codeowners` list is intentionally empty in version 0.1.1 until a personal GitHub username or organization team is selected as the maintainer.

## License

MIT
