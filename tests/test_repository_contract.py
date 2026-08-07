"""Static architecture regression tests that do not require Home Assistant installed."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "smart_entity_timer"


class RepositoryContractTests(unittest.TestCase):
    def test_all_entities_use_modern_names(self):
        entity_source = (COMPONENT / "entity.py").read_text()
        self.assertIn("_attr_has_entity_name = True", entity_source)
        for filename, key in [
            ("sensor.py", "status"),
            ("number.py", "duration"),
            ("select.py", "end_action"),
            ("button.py", "start"),
            ("button.py", "cancel"),
        ]:
            source = (COMPONENT / filename).read_text()
            self.assertIn(f'_attr_translation_key = "{key}"', source)

    def test_options_do_not_structurally_reconfigure_target(self):
        source = (COMPONENT / "config_flow.py").read_text()
        options_start = source.index("class SmartEntityTimerOptionsFlow")
        options_source = source[options_start:]
        self.assertNotIn("CONF_TARGET_ENTITY,\n                    default=current", options_source)
        self.assertIn("async_step_reconfigure", source)

    def test_card_api_v2_attributes_and_service(self):
        runtime = (COMPONENT / "runtime.py").read_text()
        init = (COMPONENT / "__init__.py").read_text()
        self.assertIn('"companion_entities": self._companion_entities()', runtime)
        self.assertIn('"constraints": {', runtime)
        self.assertIn("async_service_set_values", (COMPONENT / "sensor.py").read_text())
        self.assertIn("SERVICE_SET_VALUES", init)

    def test_notification_templates_and_lifecycle_events(self):
        runtime = (COMPONENT / "runtime.py").read_text()
        config_flow = (COMPONENT / "config_flow.py").read_text()
        const = (COMPONENT / "const.py").read_text()
        diagnostics = (COMPONENT / "diagnostics.py").read_text()
        self.assertIn("NOTIFICATION_TEMPLATE_KEYS", runtime)
        self.assertIn("validate_notification_template", config_flow)
        for event_name in ["EVENT_STARTED", "EVENT_COMPLETED", "EVENT_CANCELLED", "EVENT_SKIPPED", "EVENT_ERROR"]:
            self.assertIn(event_name, const)
        self.assertIn("_fire_result_event", runtime)
        self.assertIn("custom_notification_templates_configured", diagnostics)


if __name__ == "__main__":
    unittest.main()
