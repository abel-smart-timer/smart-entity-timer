# Smart Entity Timer roadmap

## Current stable baseline — 0.3.0

- Persistent entity timers.
- One parent integration with Timer Config Subentries.
- Card API v2.
- Personalized notification templates.
- Lifecycle events.
- Smart Entity Timer Card 0.3.0 with Expanded, Compact, Mini and Tile/Mosaico layouts.

## 1.0.0 candidate — all-in-one distribution

Goal: make Smart Entity Timer a complete one-installation HACS product.

Scope:

- bundle the compiled Smart Entity Timer Card inside the integration;
- serve it through Home Assistant's static-path API;
- register it through Home Assistant's frontend extra-module API;
- preserve `custom:smart-entity-timer-card` and Card API v2;
- preserve existing timer entity IDs, Config Subentries, storage, automations, notifications and events;
- retire the separate Card repository from the default HACS catalog after 1.0.0 is verified, while keeping that GitHub repository for frontend development.

## After 1.0.0

Use normal semantic versioning:

- `1.0.x` for compatible bug fixes;
- `1.x.0` for compatible features;
- `2.0.0` only for a deliberate breaking public-contract change.
