# Notifications and lifecycle events — 0.2.0

Smart Entity Timer 0.2.0 keeps the existing notification delivery model and adds optional per-result text customization plus public lifecycle events.

## Notification categories

- completed
- error
- skipped
- manual cancel
- automatic cancel

Titles and messages are configured independently. Empty values use the built-in localized text.


## Quick examples for the options screen

Leave a field blank to keep the built-in localized text. The options screen also shows the supported placeholders and examples directly above/below the notification fields.

### Completion

```text
Title: Timer for {target_name}
Message: {target_name} was {action_past} after {duration}.
```

Spanish example:

```text
Título: Temporizador de {target_name}
Mensaje: {target_name} fue {action_past} después de {duration}.
```

### Error

```text
Title: Timer error — {target_name}
Message: {target_name} could not complete {action}. Reason: {reason}.
```

### Skipped after restart

```text
Title: Timer action skipped
Message: {action} for {target_name} was skipped. Reason: {reason}.
```

### Manual cancellation

```text
Title: Timer cancelled
Message: {timer_name} was cancelled manually.
```

### Automatic cancellation

```text
Title: Timer cancelled automatically
Message: {target_name} reached the requested state before the timer finished.
```

## Template safety

Templates use only named fields listed in README. Arbitrary Jinja, attribute access, indexing, conversions, and format specifications are not executed. This keeps configuration predictable and avoids turning notification text into a general-purpose template execution surface.

## Event contract

Event schema version 1 is emitted on the Home Assistant event bus. `smart_entity_timer.cancelled` represents both `cancelled` and `auto_cancelled`; consumers should use `result` and `reason`.

Events deliberately exclude notification targets and custom template text.
