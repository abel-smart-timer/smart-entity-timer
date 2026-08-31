"""Static architecture regression tests that do not require Home Assistant installed."""

import json
from pathlib import Path
import re
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

    def test_manifest_exposes_single_hub_entry(self):
        manifest = json.loads((COMPONENT / "manifest.json").read_text())
        self.assertRegex(manifest["version"], r"^1\.\d+\.\d+(?:-rc\d+)?$")
        self.assertEqual(manifest["integration_type"], "hub")
        self.assertTrue(manifest["single_config_entry"])

        const = (COMPONENT / "const.py").read_text()
        self.assertIn(f'VERSION = "{manifest["version"]}"', const)

    def test_config_flow_uses_timer_subentries(self):
        source = (COMPONENT / "config_flow.py").read_text()
        self.assertIn("async_get_supported_subentry_types", source)
        self.assertIn("SmartEntityTimerSubentryFlow", source)
        self.assertIn("async_on_create_entry", source)
        self.assertIn("FlowType.CONFIG_SUBENTRIES_FLOW", source)
        self.assertIn("async_step_reconfigure", source)
        self.assertNotIn("OptionsFlowWithReload", source)
        self.assertNotIn("SmartEntityTimerOptionsFlow", source)

    def test_platform_entities_are_owned_by_subentries(self):
        for filename in ["sensor.py", "number.py", "select.py", "button.py"]:
            source = (COMPONENT / filename).read_text()
            self.assertIn("SmartEntityTimerManager", source)
            self.assertIn("config_subentry_id=subentry_id", source)

    def test_legacy_migration_preserves_entity_identity(self):
        source = (COMPONENT / "migration.py").read_text()
        self.assertIn("async_add_subentry", source)
        self.assertIn("config_entry_id=parent.entry_id", source)
        self.assertIn("config_subentry_id=subentry.subentry_id", source)
        self.assertIn("await hass.config_entries.async_remove", source)
        self.assertNotIn("new_unique_id=", source)
        self.assertNotIn("new_entity_id=", source)

    def test_runtime_adapter_preserves_legacy_storage_and_unique_id_prefix(self):
        manager = (COMPONENT / "manager.py").read_text()
        entity = (COMPONENT / "entity.py").read_text()
        runtime = (COMPONENT / "runtime.py").read_text()
        self.assertIn("self.subentry.data.get(CONF_TIMER_ID)", manager)
        self.assertIn("self.subentry.subentry_id", manager)
        self.assertIn('f"{runtime.entry.entry_id}_{key}"', entity)
        self.assertIn("STORAGE_KEY.format(entry_id=entry.entry_id)", runtime)

    def test_card_api_v2_attributes_and_service_unchanged(self):
        runtime = (COMPONENT / "runtime.py").read_text()
        init = (COMPONENT / "__init__.py").read_text()
        self.assertIn('"companion_entities": self._companion_entities()', runtime)
        self.assertIn('"constraints": {', runtime)
        self.assertIn("async_service_set_values", (COMPONENT / "sensor.py").read_text())
        self.assertIn("SERVICE_SET_VALUES", init)

    def test_notification_templates_and_lifecycle_events_remain(self):
        runtime = (COMPONENT / "runtime.py").read_text()
        config_flow = (COMPONENT / "config_flow.py").read_text()
        const = (COMPONENT / "const.py").read_text()
        diagnostics = (COMPONENT / "diagnostics.py").read_text()
        self.assertIn("NOTIFICATION_TEMPLATE_KEYS", runtime)
        self.assertIn("validate_notification_template", config_flow)
        for event_name in [
            "EVENT_STARTED",
            "EVENT_COMPLETED",
            "EVENT_CANCELLED",
            "EVENT_SKIPPED",
            "EVENT_ERROR",
        ]:
            self.assertIn(event_name, const)
        self.assertIn("_fire_result_event", runtime)
        self.assertIn("custom_notification_templates_configured", diagnostics)

    def test_translations_expose_timer_subentry_ui(self):
        for lang in ["en", "es", "es-419"]:
            payload = json.loads((COMPONENT / "translations" / f"{lang}.json").read_text())
            timer = payload["config_subentries"]["timer"]
            self.assertIn("entry_type", timer)
            self.assertIn("user", timer["initiate_flow"])
            self.assertIn("user", timer["step"])
            self.assertIn("reconfigure", timer["step"])

    def test_english_runtime_translation_matches_strings_source(self):
        strings_payload = json.loads((COMPONENT / "strings.json").read_text())
        english_payload = json.loads((COMPONENT / "translations" / "en.json").read_text())
        self.assertEqual(strings_payload, english_payload)

    def test_config_flow_notification_help_has_no_translation_placeholders(self):
        placeholder_names = (
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
        )
        placeholder = re.compile(
            r"\{(?:" + "|".join(re.escape(name) for name in placeholder_names) + r")\}"
        )

        for lang in ["en", "es", "es-419"]:
            payload = json.loads((COMPONENT / "translations" / f"{lang}.json").read_text())
            steps = payload["config_subentries"]["timer"]["step"]
            for step_name in ["user", "reconfigure"]:
                step = steps[step_name]
                self.assertIsNone(
                    placeholder.search(step["description"]),
                    f"{lang}/{step_name} description contains a translation placeholder",
                )
                for key, text in step["data_description"].items():
                    if not key.startswith("notification_"):
                        continue
                    self.assertIsNone(
                        placeholder.search(text),
                        f"{lang}/{step_name}/{key} contains a translation placeholder",
                    )
                for name in placeholder_names:
                    self.assertIn(
                        f"`{name}`",
                        step["description"],
                        f"{lang}/{step_name} no longer documents variable {name}",
                    )

    def test_all_in_one_frontend_is_bundled(self):
        manifest = json.loads((COMPONENT / "manifest.json").read_text())
        self.assertIn("frontend", manifest["dependencies"])
        self.assertIn("http", manifest["dependencies"])
        self.assertIn("lovelace", manifest["dependencies"])

        asset = COMPONENT / "www" / "smart-entity-timer-card.js"
        self.assertTrue(asset.is_file())
        source = asset.read_text()

        self.assertIn(f'const CARD_VERSION = "{manifest["version"]}";', source)
        self.assertIn('customElements.get("smart-entity-timer-card")', source)
        self.assertIn("layout_mini", source)
        self.assertIn("layout_tile", source)
        self.assertIn("MIN_CARD_API_VERSION = 2", source)

    def test_frontend_registration_uses_home_assistant_frontend_api(self):
        frontend = (COMPONENT / "frontend.py").read_text()
        init = (COMPONENT / "__init__.py").read_text()
        const = (COMPONENT / "const.py").read_text()
        self.assertIn("async_register_static_paths", frontend)
        self.assertIn("StaticPathConfig", frontend)
        self.assertIn("async_get_info", frontend)
        self.assertIn("async_create_item", frontend)
        self.assertIn("async_update_item", frontend)
        self.assertIn("res_type", frontend)
        self.assertIn("add_extra_js_url", frontend)
        self.assertIn("await async_register_frontend(hass)", init)
        self.assertIn("FRONTEND_CARD_PATH", const)
        self.assertIn("FRONTEND_CARD_URL", const)


if __name__ == "__main__":
    unittest.main()
