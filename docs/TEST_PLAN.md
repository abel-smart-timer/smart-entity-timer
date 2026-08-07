# Functional test plan — Smart Entity Timer 0.1.3

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
3. Open **Settings → Devices & services → Helpers**, select **Create helper**, and choose **Smart Entity Timer**.
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

### T26 — Reconfigure target while idle

Use the config entry Reconfigure flow to change the target entity.

Expected: entry reloads, existing unique IDs remain associated with the timer entry, and the new target is monitored.

### T27 — Download diagnostics

Download diagnostics from the integration entry.

Expected: runtime details are present, but notification destination identifiers are omitted.

### T28 — Reload/unload

Reload the integration entry several times.

Expected: no duplicate listeners, duplicate actions, or repeated notifications.

## Acceptance gate for card development

Proceed to the first card test version only after:

- T01–T16 pass on `input_boolean` or `switch`;
- T07–T22 pass on at least one real `climate` entity;
- notifications pass on at least one Companion App device;
- no unexplained errors remain in the Home Assistant log.


### T29 — Card API v2 synchronization

While idle, call `smart_entity_timer.set_values` to change duration and action.

Expected:

- status sensor attributes update immediately;
- native number/select entities show the same values;
- `card_api_version` is `2`;
- `constraints` and `capabilities` are present;
- `companion_entities` resolves the four native companion entities.

## 0.2.0 notification and lifecycle-event tests

### T30 — Default notification backward compatibility

Leave every custom notification field blank and complete a normal timer.

Expected: the same localized title/message used by 0.1.3 is delivered.

### T31 — Custom completion notification

Configure a custom completion title and message using `{target_name}`, `{action_past}`, and `{duration}`.

Expected: placeholders render correctly and the notification reaches the selected destination.

### T32 — Custom error and skipped notifications

#### T32A — Custom error notification

1. Configure a notification destination.
2. Set **Custom error title** to `Error: {target_name}`.
3. Set **Custom error message** to `{target_name} no pudo completar {action}. Motivo: {reason}.`
4. Start a short timer while the target is in the opposite state.
5. Before expiry, make the real target entity `unavailable` (for example, disconnect its device/network) and leave it unavailable through expiry.

Expected:

- status becomes `error`;
- `last_result` is `error`;
- `last_reason` is `target_unavailable`;
- the notification uses the custom error title/message.

#### T32B — Custom skipped notification

1. Keep **Execute an expired turn-on after restart** disabled.
2. Set **Custom skipped title** to `Acción omitida: {target_name}`.
3. Set **Custom skipped message** to `Se omitió {action} para {target_name}. Motivo: {reason}.`
4. Leave the target off and start a one-minute **turn_on** timer.
5. Shut Home Assistant down before expiry, wait until after the timer should have expired, then start Home Assistant again.

Expected:

- the target remains off;
- `last_result` is `skipped`;
- `last_reason` is `expired_during_restart`;
- the skipped notification uses the custom text.

### T33 — Manual and automatic cancellation templates

Enable both cancellation notification switches, configure distinct templates, then test manual and automatic cancellation.

Expected: the correct template is used for each cancellation type. Disable each switch and confirm the corresponding notification is suppressed while the lifecycle event still fires.

### T34 — Invalid placeholder validation

1. Open the timer options.
2. Put `{unknown_field}` in any custom notification field and try to save.
3. Repeat with an unmatched `{`.

Expected:

- Options rejects the invalid field and remains open;
- the integration does not reload with the invalid value;
- the previously saved valid notification configuration remains intact.

### T35 — Lifecycle events

For events that happen while Home Assistant is running, open **Developer Tools → Events**, enter one event type under **Listen to events**, and select **Start listening**. Home Assistant displays the event-data JSON when the event fires.

Test at least:

- `smart_entity_timer.started`: start a timer; expect one event with `result: started`.
- `smart_entity_timer.completed`: let a timer finish normally; expect one event with `result: completed`.
- `smart_entity_timer.cancelled`: cancel manually; expect `result: cancelled`, then repeat an early target-state change and expect `result: auto_cancelled`.
- `smart_entity_timer.error`: make a target unavailable through expiry; expect `result: error`.

For `smart_entity_timer.skipped`, the event occurs during Home Assistant startup, so a browser listener cannot remain connected across shutdown. Create a temporary automation **before** the restart with an Event trigger for `smart_entity_timer.skipped` and an action such as creating a persistent notification. Then perform T32B and confirm the automation triggers exactly once.

Every lifecycle event must include:

- `event_schema_version: 1`;
- `timer_name`;
- `target_entity` and `target_name`;
- `action`;
- `duration_minutes`;
- `result`;
- `reason`;
- timestamps.

Notification destination IDs and custom notification template text must not be present.

### T36 — Existing card compatibility

Use Smart Entity Timer Card 0.2.2 without changing its configuration.

1. Confirm the status sensor still reports `card_api_version: 2`.
2. Open the existing card.
3. Change duration and action from the card.
4. Start and cancel once.
5. Run one normal completion.
6. If practical, open the same card in two browsers and confirm both stay synchronized.

Expected: the card behaves exactly as with backend 0.1.3 and no card configuration changes are required.

