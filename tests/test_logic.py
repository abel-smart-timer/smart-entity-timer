"""Dependency-light regression tests for Smart Entity Timer pure state logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "smart_entity_timer"


class Platform(StrEnum):
    SENSOR = "sensor"
    NUMBER = "number"
    SELECT = "select"
    BUTTON = "button"


@dataclass
class FakeState:
    state: str
    attributes: dict = field(default_factory=dict)


def _load_logic():
    homeassistant = types.ModuleType("homeassistant")
    ha_const = types.ModuleType("homeassistant.const")
    ha_const.ATTR_RESTORED = "restored"
    ha_const.Platform = Platform
    ha_core = types.ModuleType("homeassistant.core")
    ha_core.State = FakeState
    sys.modules.setdefault("homeassistant", homeassistant)
    sys.modules["homeassistant.const"] = ha_const
    sys.modules["homeassistant.core"] = ha_core

    package = types.ModuleType("smart_entity_timer")
    package.__path__ = [str(COMPONENT)]
    sys.modules["smart_entity_timer"] = package

    const_spec = importlib.util.spec_from_file_location(
        "smart_entity_timer.const", COMPONENT / "const.py"
    )
    const_module = importlib.util.module_from_spec(const_spec)
    sys.modules["smart_entity_timer.const"] = const_module
    assert const_spec.loader is not None
    const_spec.loader.exec_module(const_module)

    logic_spec = importlib.util.spec_from_file_location(
        "smart_entity_timer.logic", COMPONENT / "logic.py"
    )
    logic_module = importlib.util.module_from_spec(logic_spec)
    sys.modules["smart_entity_timer.logic"] = logic_module
    assert logic_spec.loader is not None
    logic_spec.loader.exec_module(logic_module)
    return const_module, logic_module


CONST, LOGIC = _load_logic()


class StateLogicTests(unittest.TestCase):
    def test_strict_on_off_domains(self):
        self.assertTrue(LOGIC.target_state_reached("light.test", FakeState("off"), CONST.ACTION_TURN_OFF))
        self.assertTrue(LOGIC.target_state_reached("switch.test", FakeState("on"), CONST.ACTION_TURN_ON))
        self.assertFalse(LOGIC.target_state_reached("fan.test", FakeState("on"), CONST.ACTION_TURN_OFF))

    def test_mode_domains(self):
        self.assertTrue(LOGIC.target_state_reached("climate.test", FakeState("cool"), CONST.ACTION_TURN_ON))
        self.assertTrue(LOGIC.target_state_reached("climate.test", FakeState("off"), CONST.ACTION_TURN_OFF))
        self.assertTrue(LOGIC.target_state_reached("water_heater.test", FakeState("eco"), CONST.ACTION_TURN_ON))

    def test_media_player_standby_is_off(self):
        self.assertTrue(LOGIC.target_state_reached("media_player.test", FakeState("standby"), CONST.ACTION_TURN_OFF))
        self.assertTrue(LOGIC.target_state_reached("media_player.test", FakeState("playing"), CONST.ACTION_TURN_ON))

    def test_unavailable_and_restored_states_are_not_actionable(self):
        self.assertFalse(LOGIC.target_state_reached("light.test", FakeState("unavailable"), CONST.ACTION_TURN_OFF))
        self.assertFalse(LOGIC.target_state_reached("light.test", FakeState("off", {"restored": True}), CONST.ACTION_TURN_OFF))

    def test_format_duration(self):
        self.assertEqual(LOGIC.format_duration(1), "1 minute")
        self.assertEqual(LOGIC.format_duration(61), "1 hour 1 minute")
        self.assertEqual(LOGIC.format_duration(120, spanish=True), "2 horas")


class ApiContractTests(unittest.TestCase):
    def test_card_api_version_is_two(self):
        self.assertEqual(CONST.CARD_API_VERSION, 2)

    def test_new_set_values_service_is_declared(self):
        self.assertEqual(CONST.SERVICE_SET_VALUES, "set_values")

    def test_version(self):
        manifest = json.loads((COMPONENT / "manifest.json").read_text())
        self.assertEqual(CONST.VERSION, manifest["version"])

    def test_subentry_architecture_constants(self):
        self.assertEqual(CONST.CONFIG_ENTRY_VERSION, 2)
        self.assertEqual(CONST.SUBENTRY_TYPE_TIMER, "timer")
        self.assertEqual(CONST.ARCHITECTURE_SUBENTRIES_V1, "subentries_v1")

    def test_notification_and_event_contract(self):
        self.assertEqual(len(CONST.NOTIFICATION_TEMPLATE_KEYS), 5)
        self.assertEqual(CONST.EVENT_STARTED, "smart_entity_timer.started")
        self.assertEqual(CONST.EVENT_COMPLETED, "smart_entity_timer.completed")
        self.assertEqual(CONST.EVENT_CANCELLED, "smart_entity_timer.cancelled")
        self.assertEqual(CONST.EVENT_SKIPPED, "smart_entity_timer.skipped")
        self.assertEqual(CONST.EVENT_ERROR, "smart_entity_timer.error")


if __name__ == "__main__":
    unittest.main()
