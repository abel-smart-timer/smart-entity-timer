# Roadmap

This file separates the current stable release from development candidates and later ideas.

## Current stable release

- Smart Entity Timer 0.1.3
- Smart Entity Timer Card 0.2.2
- Card API 2

## 0.2.0 development candidate

The following features are implemented in the 0.2.0 test candidate but are not considered stable until HAOS testing is completed:

- customizable completion notification title/message;
- customizable error notification title/message;
- customizable skipped-during-restart title/message;
- customizable manual-cancellation title/message;
- customizable automatic-cancellation title/message;
- safe documented placeholders;
- lifecycle events for started, completed, cancelled, skipped, and error outcomes.

The 0.1.3 built-in notification wording remains the default whenever custom fields are blank.

## Possible later improvements

Only consider these after 0.2.0 is stable:

- optional notification preview/test action from the options UI;
- additional lifecycle event fields if real automation use cases require them;
- more notification delivery policies only when there is a concrete need;
- localization improvements for human-readable event/template values.

Avoid arbitrary Jinja execution in notification options unless there is a strong reason. The simple placeholder contract is easier to validate, document, and support.

## Design principle

Timer execution and notifications belong in the backend integration so they continue working with no dashboard open and across Home Assistant restarts. Card API v2 remains unchanged unless a future card/backend capability genuinely requires a new contract.
