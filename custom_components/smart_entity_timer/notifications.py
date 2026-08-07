"""Safe, user-configurable notification templates for Smart Entity Timer."""

from __future__ import annotations

from string import Formatter
from typing import Mapping

ALLOWED_TEMPLATE_FIELDS: frozenset[str] = frozenset(
    {
        "timer_name",
        "target_name",
        "target_entity",
        "action",
        "action_id",
        "action_past",
        "duration",
        "duration_minutes",
        "result",
        "reason",
        "finished_at",
        "restored",
        "default_title",
        "default_message",
    }
)


def validate_notification_template(value: str) -> str:
    """Validate a simple named-field template and return it unchanged."""
    template = str(value or "")
    if not template:
        return ""

    try:
        parsed = Formatter().parse(template)
        for _literal, field_name, format_spec, conversion in parsed:
            if field_name is None:
                continue
            if field_name not in ALLOWED_TEMPLATE_FIELDS:
                raise ValueError(f"Unsupported placeholder: {field_name}")
            if format_spec:
                raise ValueError("Format specifications are not supported")
            if conversion:
                raise ValueError("Conversions are not supported")
    except ValueError as err:
        raise ValueError(f"Invalid notification template: {err}") from err

    return template


def render_notification_template(
    template: str,
    default: str,
    context: Mapping[str, object],
) -> str:
    """Render one validated template, falling back to the supplied default."""
    template = str(template or "").strip()
    if not template:
        return default
    validate_notification_template(template)
    return template.format_map({key: str(value) for key, value in context.items()})
