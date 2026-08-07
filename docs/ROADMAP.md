# Smart Entity Timer roadmap

## Current published functionality — 0.2.0

- Persistent entity timers.
- Card API v2.
- Smart Entity Timer Card 0.2.2 compatibility.
- Personalized notification templates.
- Lifecycle events.
- HACS installation/update support.

## 0.3.0 candidate — centralized management

Goal: move administration from one Helper entry per timer to one normal Smart Entity Timer integration with one Timer Config Subentry per configured timer.

Candidate scope:

- one parent config entry;
- `integration_type: hub`;
- `single_config_entry: true`;
- add/reconfigure Timer subentries from the integration page;
- automatic conversion of existing 0.1.x/0.2.x timer entries;
- preserve entity IDs, unique IDs, storage identity, Card API v2, notifications, events, cards, and automations.

No Card API v3 or new timer behavior is planned as part of this architecture change.

## After 0.3.0

Only add new functions when they solve a concrete use case or bug. Possible future work can include configuration-form organization, richer diagnostics, and additional notification/event capabilities without changing the core timer semantics unnecessarily.
