"""Bundled frontend registration for Smart Entity Timer."""

from __future__ import annotations

from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant

from .const import FRONTEND_CARD_PATH, FRONTEND_CARD_URL

_CARD_FILE = Path(__file__).parent / "www" / "smart-entity-timer-card.js"


async def async_register_frontend(hass: HomeAssistant) -> None:
    """Serve and register the Smart Entity Timer Card bundled with the integration."""
    await hass.http.async_register_static_paths(
        [StaticPathConfig(FRONTEND_CARD_PATH, str(_CARD_FILE), True)]
    )

    # Home Assistant's frontend API loads this ES module for every frontend session.
    # Using the integration version in the URL gives us deterministic cache busting.
    add_extra_js_url(hass, FRONTEND_CARD_URL)
