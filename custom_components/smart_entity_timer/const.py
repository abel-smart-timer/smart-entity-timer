"""Constants for Smart Entity Timer."""

from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "smart_entity_timer"
NAME = "Smart Entity Timer"
VERSION = "0.1.2"
MIN_HA_VERSION = "2026.7.0"
CARD_API_VERSION = 1

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.BUTTON,
]

CONF_TARGET_ENTITY = "target_entity"
CONF_DEFAULT_ACTION = "default_action"
CONF_DEFAULT_DURATION_MINUTES = "default_duration_minutes"
CONF_MAX_DURATION_MINUTES = "max_duration_minutes"
CONF_NOTIFICATION_TARGET = "notification_target"
CONF_NOTIFY_MANUAL_CANCEL = "notify_manual_cancel"
CONF_NOTIFY_AUTO_CANCEL = "notify_auto_cancel"
CONF_EXECUTE_EXPIRED_TURN_OFF = "execute_expired_turn_off"
CONF_EXECUTE_EXPIRED_TURN_ON = "execute_expired_turn_on"
CONF_CONFIRMATION_TIMEOUT = "confirmation_timeout"

DEFAULT_ACTION = "turn_off"
DEFAULT_DURATION_MINUTES = 60
DEFAULT_MAX_DURATION_MINUTES = 24 * 60
DEFAULT_CONFIRMATION_TIMEOUT = 10
WATCHDOG_INTERVAL_SECONDS = 1
RESTORE_TARGET_WAIT_SECONDS = 120
DEFAULT_NOTIFY_MANUAL_CANCEL = False
DEFAULT_NOTIFY_AUTO_CANCEL = False
DEFAULT_EXECUTE_EXPIRED_TURN_OFF = True
DEFAULT_EXECUTE_EXPIRED_TURN_ON = False

ACTION_TURN_ON = "turn_on"
ACTION_TURN_OFF = "turn_off"
ACTIONS: tuple[str, str] = (ACTION_TURN_ON, ACTION_TURN_OFF)

STATUS_IDLE = "idle"
STATUS_ACTIVE = "active"
STATUS_EXECUTING = "executing"
STATUS_ERROR = "error"

RESULT_COMPLETED = "completed"
RESULT_CANCELLED = "cancelled"
RESULT_AUTO_CANCELLED = "auto_cancelled"
RESULT_SKIPPED = "skipped"
RESULT_ERROR = "error"

REASON_MANUAL_CANCEL = "manual_cancel"
REASON_TARGET_REACHED = "target_reached_early"
REASON_ALREADY_TARGET = "already_in_target_state"
REASON_EXPIRED_DURING_RESTART = "expired_during_restart"
REASON_TARGET_UNAVAILABLE = "target_unavailable"
REASON_RESTORE_TARGET_UNAVAILABLE = "restore_target_unavailable"
REASON_ACTION_FAILED = "action_failed"
REASON_CONFIRMATION_TIMEOUT = "confirmation_timeout"

SERVICE_START = "start"
SERVICE_CANCEL = "cancel"
ATTR_DURATION_MINUTES = "duration_minutes"
ATTR_END_ACTION = "end_action"

STORAGE_VERSION = 1
STORAGE_KEY = f"{DOMAIN}.{{entry_id}}"

# Domains with reliable Home Assistant turn_on/turn_off semantics for v0.1.2.
SUPPORTED_DOMAINS: tuple[str, ...] = (
    "climate",
    "fan",
    "humidifier",
    "input_boolean",
    "light",
    "media_player",
    "remote",
    "switch",
    "water_heater",
)

STRICT_ON_OFF_DOMAINS: frozenset[str] = frozenset(
    {
        "fan",
        "humidifier",
        "input_boolean",
        "light",
        "remote",
        "switch",
    }
)

MODE_DOMAINS: frozenset[str] = frozenset({"climate", "water_heater"})
MEDIA_PLAYER_OFF_STATES: frozenset[str] = frozenset({"off", "standby"})
UNAVAILABLE_STATES: frozenset[str] = frozenset({"unknown", "unavailable"})
