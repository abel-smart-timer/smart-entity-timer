"""Pure logic helpers for Smart Entity Timer."""

from __future__ import annotations

from homeassistant.core import State

from .const import (
    ACTION_TURN_OFF,
    ACTION_TURN_ON,
    MEDIA_PLAYER_OFF_STATES,
    MODE_DOMAINS,
    STRICT_ON_OFF_DOMAINS,
    UNAVAILABLE_STATES,
)


def is_state_usable(state: State | None) -> bool:
    """Return whether a Home Assistant state can be evaluated."""
    return state is not None and state.state not in UNAVAILABLE_STATES


def is_entity_on(entity_id: str, state: State | None) -> bool | None:
    """Classify an entity as on/off, or None when the state is indeterminate."""
    if not is_state_usable(state):
        return None

    domain = entity_id.split(".", 1)[0]
    raw_state = state.state

    if domain in STRICT_ON_OFF_DOMAINS:
        if raw_state == "on":
            return True
        if raw_state == "off":
            return False
        return None

    if domain in MODE_DOMAINS:
        return raw_state != "off"

    if domain == "media_player":
        return raw_state not in MEDIA_PLAYER_OFF_STATES

    return None


def target_state_reached(
    entity_id: str,
    state: State | None,
    action: str,
) -> bool:
    """Return whether the requested final state has already been reached."""
    is_on = is_entity_on(entity_id, state)
    if is_on is None:
        return False
    if action == ACTION_TURN_ON:
        return is_on
    if action == ACTION_TURN_OFF:
        return not is_on
    return False


def format_duration(minutes: int, *, spanish: bool = False) -> str:
    """Return a human-readable duration without decimal hours."""
    total_minutes = max(0, int(minutes))
    hours, mins = divmod(total_minutes, 60)

    if spanish:
        parts: list[str] = []
        if hours:
            parts.append(f"{hours} {'hora' if hours == 1 else 'horas'}")
        if mins or not parts:
            parts.append(f"{mins} {'minuto' if mins == 1 else 'minutos'}")
        return " ".join(parts)

    parts = []
    if hours:
        parts.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
    if mins or not parts:
        parts.append(f"{mins} {'minute' if mins == 1 else 'minutes'}")
    return " ".join(parts)
