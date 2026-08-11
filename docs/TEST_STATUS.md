# Smart Entity Timer test status

## Published baseline — 0.3.0

Smart Entity Timer 0.3.0 has been validated on real Home Assistant installations for the centralized parent + Config Subentry architecture, migration from older entries, preservation of entity IDs, Card API v2, notifications and lifecycle events. Smart Entity Timer Card 0.3.0 has also been validated on real mobile dashboards, including Mini and Tile/Mosaico layouts.

## 1.0.0 all-in-one candidate

Automated local checks currently pass for:

- Python compilation;
- 26 dependency-light regression tests;
- backend version `1.0.0`;
- Card API v2 unchanged;
- manifest `hub` + `single_config_entry` contract;
- bundled frontend presence and version;
- Home Assistant static-path and extra-module registration source contract;
- JavaScript syntax of the bundled Card;
- existing notifications, events, Config Subentries and migration source contracts.

Real Home Assistant acceptance is still required before release. Complete `docs/TEST_PLAN_1.0.0.md`, especially the clean HACS install and upgrade from the separated 0.3.0 integration + Card installation.
