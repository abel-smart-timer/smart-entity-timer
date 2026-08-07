# Changelog

## 0.1.3 — 2026-08-06

Architecture and card-contract stabilization release.

- Added Card API v2 and made the status sensor the authoritative card state source.
- Added atomic `smart_entity_timer.set_values` for duration and/or action changes.
- Added `capabilities`, `constraints`, and `companion_entities` status attributes.
- Adopted `has_entity_name = True` and translated names for all five entities.
- Moved target-entity changes to a dedicated Reconfigure flow.
- Added automatic migration of 0.1.2 entries that stored an overridden target in Options.
- Kept native number/select/button entities for normal Home Assistant use without making the card depend on registry discovery.
- Added dependency-light automated regression tests and a Python CI job.
- Updated documentation for the existing companion card.

## 0.1.2 — 2026-08-05

- Fixed expired OFF timers after a Home Assistant restart.
- Restoration now waits until Home Assistant has fully started before resuming or processing a persisted timer.
- Restored placeholder entity states are no longer treated as live, actionable states.
- An expired action that must execute waits up to 120 seconds for the real target entity to become available.
- Added `restore_pending` and `restore_target_wait_seconds` diagnostic attributes.
- Expired ON timers continue to be skipped by default for safety.

## 0.1.1 — 2026-08-05

Automatic-cancellation reliability update.

- Renamed the native status entity label to **Timer status / Estado del temporizador** to clarify that it reports the timer lifecycle, not the target entity state.
- Kept immediate cancellation through `async_track_state_change_event`.
- Added a lightweight one-second in-memory watchdog only while a timer is active. It detects the requested target state even when a device integration misses or delays the expected event callback.
- Added a single-flight race-safe state check so duplicate events cannot cancel the same timer twice.
- Added `target_state_reached` and `watchdog_active` diagnostic attributes.
- The watchdog stops immediately when the timer finishes, is cancelled, errors, or the integration unloads.

## 0.1.0 — 2026-08-04

Initial functional backend release.

- One persistent timer per selected Home Assistant entity.
- Selectable final action: `turn_on` or `turn_off`.
- Arbitrary whole-minute duration; the future card will provide ±30-minute shortcuts.
- Native status sensor, duration number, action select, start button, and cancel button.
- Entity services: `smart_entity_timer.start` and `smart_entity_timer.cancel`.
- Automatic cancellation when the target reaches the requested state before expiry.
- Race-safe state check immediately before executing the final action.
- Persistent restoration after Home Assistant restarts.
- Safe default for timers that expire while Home Assistant is offline:
  - expired OFF action: execute after startup;
  - expired ON action: skip and notify.
- Optional multi-target notifications using Home Assistant notification targets.
- Spanish and English configuration translations.
- Diagnostics output that omits notification target identifiers.
