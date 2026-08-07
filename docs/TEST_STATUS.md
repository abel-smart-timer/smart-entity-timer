# Smart Entity Timer test status

## Stable baseline

Smart Entity Timer 0.2.0 behavior was validated on real Home Assistant installations, including default/custom notifications, manual and automatic cancellation notifications, lifecycle events, restart behavior, Card API v2, and Smart Entity Timer Card 0.2.2 compatibility.

The card/integration combination was also installed successfully from HACS on a clean Raspberry Pi 5 Home Assistant installation.

## 0.3.0 acceptance status

The 0.3.0 centralized Config Subentries architecture has passed the required real Home Assistant acceptance tests:

- **T40** clean installation on Raspberry Pi 5: passed;
- **T41** first and additional timer subentries: passed;
- **T42** centralized reconfiguration: passed;
- **T43** add/reconfigure blocked while any timer is active: passed;
- **T44** deleting one timer subentry leaves the others intact: passed;
- **T45** upgrade of one existing 0.2.0 timer with entity-ID preservation: passed;
- **T46** upgrade of multiple existing 0.2.0 timers into one parent integration: passed;
- **T48** Smart Entity Timer Card 0.2.2 compatibility after migration: passed;
- **T49** personalized notifications and lifecycle events after migration: passed.

**T47 (upgrading while a timer is active) is not a release requirement.** The supported 0.2.x → 0.3.0 upgrade procedure requires every timer to be idle before updating. T47 remains an optional robustness test only.

Automated dependency-light checks cover:

- version and Card API constants;
- existing target-state semantics;
- notification template safety;
- manifest `hub` + `single_config_entry` contract;
- Timer Config Subentry flow presence;
- subentry entity-registry ownership;
- migration source contract preserving entity IDs/unique IDs;
- stable legacy timer ID adapter;
- notification/event compatibility;
- English/Spanish Timer subentry translations.

The remaining release gate is repository CI: Python checks, Hassfest, and HACS validation must be green for the exact commit used to publish `v0.3.0`.
