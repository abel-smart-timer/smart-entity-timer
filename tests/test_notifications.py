"""Dependency-light tests for notification template helpers."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "custom_components" / "smart_entity_timer" / "notifications.py"

spec = importlib.util.spec_from_file_location("smart_entity_timer_notifications", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class NotificationTemplateTests(unittest.TestCase):
    def test_valid_template_renders(self):
        context = {key: "x" for key in module.ALLOWED_TEMPLATE_FIELDS}
        context.update({"target_name": "Luz del baño", "duration": "30 minutos"})
        rendered = module.render_notification_template(
            "{target_name}: {duration}",
            "default",
            context,
        )
        self.assertEqual(rendered, "Luz del baño: 30 minutos")

    def test_empty_template_uses_default(self):
        self.assertEqual(
            module.render_notification_template("", "Built in", {}),
            "Built in",
        )

    def test_unknown_placeholder_is_rejected(self):
        with self.assertRaises(ValueError):
            module.validate_notification_template("{unknown_field}")

    def test_attribute_and_format_access_are_rejected(self):
        with self.assertRaises(ValueError):
            module.validate_notification_template("{target_name.upper}")
        with self.assertRaises(ValueError):
            module.validate_notification_template("{duration_minutes:04d}")

    def test_escaped_braces_are_allowed(self):
        context = {key: "x" for key in module.ALLOWED_TEMPLATE_FIELDS}
        self.assertEqual(
            module.render_notification_template("{{timer}} {timer_name}", "", context),
            "{timer} x",
        )


if __name__ == "__main__":
    unittest.main()
