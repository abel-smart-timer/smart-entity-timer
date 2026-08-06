# Changelog

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
