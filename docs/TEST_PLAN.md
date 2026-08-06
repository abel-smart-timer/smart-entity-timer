# Functional test plan — Smart Entity Timer 0.1.0

Run these tests on a Home Assistant test instance before using the integration on a customer installation.

## Preparation

Use at least:

- one `input_boolean` or test switch;
- one real entity from another supported domain, preferably `climate`;
- one mobile-app notification destination;
- Home Assistant logs open in another tab.

Use a duration of one or two minutes for most tests.

Record for every test:

- Home Assistant version;
- entity domain and integration;
- expected result;
- actual result;
- relevant log messages;
- pass/fail.

## Installation and setup

### T01 — Clean installation

1. Copy `custom_components/smart_entity_timer` into `/config/custom_components`.
2. Restart Home Assistant.
3. Add **Smart Entity Timer** from Devices & services.
4. Select a supported entity.

Expected:

- configuration completes without YAML;
- five entities are created;
- no error appears in the log.

### T02 — Duplicate target protection

Try to create a second timer for the same entity.

Expected: the flow rejects the duplicate.

### T03 — Unsupported domain

Attempt to select or configure an unsupported domain.

Expected: it is not offered by the selector or is rejected by backend validation.

## Duration and action controls

### T04 — Arbitrary duration

Set the duration to 37 minutes, then to 95 minutes.

Expected: both whole-minute values are accepted and persisted.

### T05 — Change final action

Switch between `turn_on` and `turn_off` while idle.

Expected: selection changes and persists after a restart.

### T06 — Controls locked while active

Start a timer.

Expected:

- duration number is unavailable;
- action select is unavailable;
- start button is unavailable;
- cancel button is available.

## Normal execution

### T07 — OFF timer completes

1. Turn the target on.
2. Select `turn_off`.
3. Start a one-minute timer.

Expected:

- status becomes `active`;
- `started_at` and `finishes_at` are populated;
- at expiry, status briefly becomes `executing`;
- target turns off;
- status returns to `idle`;
- `last_result` becomes `completed`;
- completion notification arrives.

### T08 — ON timer completes

Repeat T07 from an off target using `turn_on`.

Expected: inverse result, with completion notification.

### T09 — Start action with overrides

Call:

```yaml
action: smart_entity_timer.start
target:
  entity_id: sensor.YOUR_TIMER_STATUS
data:
  duration_minutes: 2
  end_action: turn_off
```

Expected: this run uses the override values and updates the number/select entities.

## Automatic cancellation

### T10 — OFF timer cancelled by early manual OFF

1. Start an OFF timer while the target is on.
2. Before expiry, turn the entity off physically or from another interface.

Expected:

- timer cancels immediately;
- status returns to `idle`;
- `last_result` is `auto_cancelled`;
- `last_reason` is `target_reached_early`;
- no final action is later executed;
- no completion notification is sent.

### T11 — ON timer cancelled by early manual ON

Repeat T10 in reverse.

Expected: same automatic-cancellation behavior.

### T12 — State changed by another automation

Use an automation or manufacturer application to reach the target state early.

Expected: cancellation is based on state, not on the origin of the command.

### T13 — Last-second race

Change the target to the requested state as close as practical to expiry.

Expected: no duplicate or incorrect completion action; the final state recheck prevents a false completion claim.

## Validation and errors

### T14 — Already in target state

Try to start an OFF timer while the entity is already off, and an ON timer while it is already on.

Expected: start button is unavailable and the action call is rejected if invoked directly.

### T15 — Target unavailable at start

Make the entity unavailable, then try to start.

Expected: start is unavailable/rejected.

### T16 — Target unavailable at finish

Start a timer, then disconnect the target before expiry.

Expected:

- status becomes `error`;
- `last_reason` is `target_unavailable`;
- an error notification is sent;
- no misleading completion notification is sent.

### T17 — Confirmation timeout

Use a test entity or mocked failure where `turn_on`/`turn_off` returns but the state does not change.

Expected: after the configured timeout, status becomes `error` and an error notification is sent.

### T18 — Cancel button

Start and cancel manually.

Expected:

- target is not changed;
- result is `cancelled`;
- no completion notification;
- optional cancellation notification follows the selected option.

## Restart persistence

### T19 — Restart before expiry

Start a five-minute timer and restart Home Assistant after one minute.

Expected:

- timer restores as active;
- original absolute finish time is retained;
- only the remaining time is counted;
- action executes once at the original expiry.

### T20 — OFF timer expires while Home Assistant is down

Start a short OFF timer, shut Home Assistant down before expiry, and restart it after expiry.

Expected with defaults: target is turned off after startup and notification describes restored execution.

### T21 — ON timer expires while Home Assistant is down

Repeat using an ON timer.

Expected with defaults:

- target is not turned on;
- result is `skipped`;
- reason is `expired_during_restart`;
- warning notification is sent.

### T22 — Configurable restart policies

Reverse each restart policy in integration options and repeat T20/T21.

Expected: configured behavior is respected.

## Notifications

### T23 — Multiple notification targets

Select two notify destinations or a device/area target that resolves to multiple notify entities.

Expected: all selected destinations receive completion notification.

### T24 — Notification service failure

Temporarily use a destination that fails.

Expected: timer result remains correct; notification failure is logged but does not undo the entity action.

## Options, diagnostics, and unload

### T25 — Block options while active

Open integration options during an active timer and attempt to save.

Expected: save is rejected until the timer finishes or is cancelled.

### T26 — Change target while idle

Change the target entity in options.

Expected: entry reloads, entities remain associated with the timer entry, and the new target is monitored.

### T27 — Download diagnostics

Download diagnostics from the integration entry.

Expected: runtime details are present, but notification destination identifiers are omitted.

### T28 — Reload/unload

Reload the integration entry several times.

Expected: no duplicate listeners, duplicate actions, or repeated notifications.

## Acceptance gate for card development

Proceed to card version 0.1.0 only after:

- T01–T16 pass on `input_boolean` or `switch`;
- T07–T22 pass on at least one real `climate` entity;
- notifications pass on at least one Companion App device;
- no unexplained errors remain in the Home Assistant log.
