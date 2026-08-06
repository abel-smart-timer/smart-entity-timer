# Changelog

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
