# Smart Entity Timer roadmap

## Current stable — 1.0.0

- One HACS installation for backend + dashboard card.
- Persistent entity timers.
- One parent integration with Timer Config Subentries.
- Card API v2.
- Personalized notification templates.
- Lifecycle events.
- Bundled dashboard Card with Expanded, Compact, Mini and Tile/Mosaico layouts.
- Automatic bundled Lovelace module-resource registration.
- Upgrade path from the previous 0.3.0 integration + standalone Card installation.

## Frontend repository transition

`abel-smart-timer/smart-entity-timer-card` remains the frontend development source, but the user-facing 1.x product is distributed from the integration repository. After 1.0.0 is verified in HACS, request removal of the standalone Card from the default HACS catalog.

## After 1.0.0

Use normal semantic versioning:

- `1.0.x` for compatible bug fixes;
- `1.x.0` for compatible features;
- `2.0.0` only for a deliberate breaking public-contract change.
