# Smart Entity Timer

Persistent turn-on/turn-off timers for Home Assistant entities, with the dashboard card included.

**Version:** 1.0.0  
**Minimum Home Assistant version:** 2026.7.0  
**Card API:** 2  
**Installation:** one HACS integration package — backend + Smart Entity Timer Card

## Smart Entity Timer 1.0.0

Smart Entity Timer 1.0.0 is the first all-in-one release. Installing the integration also installs and registers the Smart Entity Timer Card; a separate HACS card download is no longer required.

```text
Smart Entity Timer 1.0.0
├── Backend
│   ├── Config Subentries
│   ├── persistent timers
│   ├── notifications
│   └── lifecycle events
└── Bundled dashboard card
    ├── Expanded
    ├── Compact
    ├── Mini
    └── Tile / Mosaico
```

The public Card API remains **v2**, and existing dashboard YAML keeps the same card type:

```yaml
type: custom:smart-entity-timer-card
entity: sensor.luz_del_bano_estado
```

## Upgrade from 0.3.0

If you currently have both **Smart Entity Timer 0.3.0** and **Smart Entity Timer Card 0.3.0** installed from HACS:

1. Wait for every Smart Entity Timer timer to become idle.
2. Create a Home Assistant backup.
3. Update Smart Entity Timer to 1.0.0.
4. **Before restarting Home Assistant, remove the standalone Smart Entity Timer Card repository from HACS.**
5. Restart Home Assistant.
6. Fully reload the browser or close/reopen the Companion App.
7. Verify that existing Smart Entity Timer cards still render.

The standalone card should be removed because 1.0.0 already ships and loads the same custom element from the integration package. Existing card YAML does not need to change.

No timer entity IDs, automations, Config Subentries, notification templates, persistent timer storage, or Card API v2 contracts are intentionally changed by this packaging transition.

## Architecture

Smart Entity Timer uses one parent Home Assistant integration entry with one Config Subentry per timer.

```text
Smart Entity Timer
├── Bathroom light timer
├── Air conditioner timer
├── Bedroom fan timer
└── Water heater timer
```

Each timer creates five native entities:

- timer status sensor;
- duration number in whole minutes;
- final-action selector (`turn_on` / `turn_off`);
- start button;
- cancel button.

The timer runs in Home Assistant itself; no dashboard or browser needs to remain open.

## Bundled dashboard card

The compiled card is shipped inside:

```text
custom_components/smart_entity_timer/www/smart-entity-timer-card.js
```

At startup the integration serves the file through Home Assistant and registers a Lovelace JavaScript module resource using a versioned URL. On a clean 1.0.0 installation the expected resource is:

```text
/smart_entity_timer_static/smart-entity-timer-card.js?v=1.0.0
```

There is no separate `/hacsfiles/smart-entity-timer-card/...` resource on a clean 1.0.0 installation.

### Mini example

```yaml
type: custom:smart-entity-timer-card
entity: sensor.aire_sala_aire_estado
layout: mini
action_mode: turn_off
button_mode: auto
progress_style: bar
quick_times:
  - "30"
  - "60"
  - "120"
  - "180"
```

### Tile / Mosaico example

```yaml
type: custom:smart-entity-timer-card
entity: sensor.aire_sala_aire_estado
layout: tile
action_mode: turn_off
button_mode: auto
progress_style: bar
```

## Core timer behavior

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
- Multiple independent timer Config Subentries.
- Card API v2.

## Supported domains

`switch`, `light`, `fan`, `climate`, `media_player`, `humidifier`, `input_boolean`, `remote`, and `water_heater`.

## Notifications

Custom title/message fields support:

`{timer_name}`, `{target_name}`, `{target_entity}`, `{action}`, `{action_id}`, `{action_past}`, `{duration}`, `{duration_minutes}`, `{result}`, `{reason}`, `{finished_at}`, `{restored}`, `{default_title}`, `{default_message}`.

Leave a custom field blank to preserve the built-in message.

## Lifecycle events

- `smart_entity_timer.started`
- `smart_entity_timer.completed`
- `smart_entity_timer.cancelled`
- `smart_entity_timer.skipped`
- `smart_entity_timer.error`

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

### HACS — recommended

Install **Smart Entity Timer** from HACS and restart Home Assistant when requested. The dashboard card is included automatically.

Do **not** install Smart Entity Timer Card separately on a clean 1.0.0 installation.

### Manual

1. Create a Home Assistant backup.
2. Ensure all Smart Entity Timer timers are idle before an upgrade.
3. Copy `custom_components/smart_entity_timer` into `/config/custom_components/smart_entity_timer`.
4. Replace the existing files.
5. If upgrading from the old standalone card, remove that HACS repository/resource before restarting.
6. Restart Home Assistant.
7. Fully reload the frontend.

## Frontend development

The frontend source continues to be developed in:

`abel-smart-timer/smart-entity-timer-card`

That repository remains public for frontend development, source history and issues. The user-facing 1.x product is distributed from `abel-smart-timer/smart-entity-timer` with the compiled card bundled inside the integration.

## Validation

The 1.0.0 release gate was exercised through the RC2 candidate, including:

- clean HACS installation with only Smart Entity Timer;
- automatic Lovelace resource creation;
- existing dashboard cards without YAML changes;
- creation of new timer Config Subentries;
- Mini, Tile, Compact and Expanded layouts;
- start, completion, manual cancel and external-state auto-cancel;
- restart persistence;
- notifications and lifecycle behavior;
- GitHub Python checks, bundled frontend checks, Hassfest and HACS validation.

See `docs/TEST_PLAN_1.0.0.md` for the release-gate procedure.

## License

MIT
