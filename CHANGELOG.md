# Changelog

## 1.0.2 — 2026-08-14

Visual README and product-presentation release.

- Added four repository-hosted promotional images under `docs/images/`, built around real Smart Entity Timer card screenshots.
- Added a visual hero banner so the GitHub/HACS documentation immediately shows what Smart Entity Timer is and how the bundled card looks.
- Added a real-card-states graphic showing active and idle/configuration states.
- Added a dashboard showcase illustrating Smart Entity Timer in desktop and mobile Home Assistant dashboards.
- Added a feature infographic summarizing timers, presets, running status, start/cancel controls, restart persistence and the bundled-card architecture.
- Reorganized the main README so visuals appear alongside the relevant technical documentation instead of being isolated from it.
- Bumped package/backend/frontend version metadata to 1.0.2 so the bundled Lovelace resource is cache-busted as `?v=1.0.2`.
- Card API remains v2 and the compiled card behavior is unchanged; only its version metadata changes.
- No timer runtime, migration, service, entity-ID, Config Subentry, notification, lifecycle-event or dashboard-card configuration behavior changes.

## 1.0.1 — 2026-08-14

Unified documentation and packaging-maintenance release.

- Expanded the main repository README so Smart Entity Timer is documented as one product: integration + bundled dashboard card.
- Added the card visual-editor workflow, layout guide, YAML examples, fixed-action behavior, configuration reference, visibility options, colors, visual styles, progress modes, and synchronization contract to the main README.
- Clarified clean HACS installation, 1.0.0 upgrade, and migration from the old 0.3.0 + standalone-card installation.
- Bumped the integration package/backend version to 1.0.1 and therefore the versioned Lovelace resource URL to `?v=1.0.1`.
- The compiled Smart Entity Timer Card is intentionally unchanged from 1.0.0; Card API remains v2 and all card YAML/options remain compatible.
- Updated repository contract validation so documentation-only integration patches may reuse the unchanged compiled frontend artifact while still validating the 1.x package version and Card API contract.
- No timer runtime, migration, notification, lifecycle-event, entity-ID, Config Subentry, or service behavior changes.

## 1.0.0 — 2026-08-14

First all-in-one stable release.

- Smart Entity Timer is now one HACS installation containing backend + dashboard card.
- Bundles `smart-entity-timer-card.js` inside `custom_components/smart_entity_timer/www/`.
- Serves the bundled JavaScript through Home Assistant static paths.
- Automatically creates/updates the Lovelace JavaScript module resource with a versioned URL.
- Keeps a frontend extra-module fallback for non-standard Lovelace configurations.
- Keeps Card API v2 and `custom:smart-entity-timer-card` unchanged.
- Keeps the 0.3.0 parent + Timer Config Subentry architecture unchanged.
- Preserves existing dashboard YAML, timer entity IDs, persistent storage, notifications and lifecycle events through the packaging transition.
- Includes the Card 0.3.0 mobile-first feature set: Expanded, Compact, Mini and Tile/Mosaico layouts, button modes, density controls, colors and progress styles.
- Validated through the RC2 release gate on a real Home Assistant installation and through Python, bundled frontend, Hassfest and HACS checks.
- The standalone `smart-entity-timer-card` repository remains the frontend development source and is intended to leave the default HACS catalog after 1.0.0 is verified.

## 0.3.0 — test candidate

Centralized integration-management architecture.

- Changed the manifest from `integration_type: helper` to `integration_type: hub`.
- Added `single_config_entry: true`.
- Replaced one-config-entry-per-timer storage with one parent config entry plus one `timer` config subentry per timer.
- Added a parent runtime manager that owns all timer runtimes.
- Added Timer config-subentry add and reconfigure flows.
- New installations open the first Add timer flow immediately after creating the parent integration.
- Existing 0.1.x/0.2.x entries are automatically consolidated before config-entry setup.
- Migration preserves existing entity IDs and unique IDs by moving entity-registry ownership to the new parent/subentry without renaming entities.
- Migration preserves the legacy timer id for persistent storage and Card API companion entity lookup.
- Entity platforms now register every timer with `config_subentry_id`.
- Card API remains v2 and Smart Entity Timer Card 0.2.2 compatibility is intentionally preserved.
- Personalized notifications and lifecycle events from 0.2.0 remain unchanged.
- Added 0.3.0 topology/migration regression checks and a dedicated manual migration test plan.

## 0.2.0 — 2026-08-07

Notification customization and lifecycle-events release candidate.

- Added optional custom titles and messages for completion, errors, skipped restart actions, manual cancellation, and automatic cancellation.
- Empty template fields keep the existing localized notification text unchanged.
- Added safe named placeholders without arbitrary Jinja execution.
- Added lifecycle events: `smart_entity_timer.started`, `smart_entity_timer.completed`, `smart_entity_timer.cancelled`, `smart_entity_timer.skipped`, and `smart_entity_timer.error`.
- Lifecycle events expose stable timer/result metadata but never notification destination identifiers.
- Custom templates are redacted from diagnostics; diagnostics only report whether each template is configured.
- Card API remains version 2, so Smart Entity Timer Card 0.2.2 remains compatible without changes.
- Fixed the last-second automatic-cancellation path so the existing automatic-cancel notification preference applies consistently.

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
