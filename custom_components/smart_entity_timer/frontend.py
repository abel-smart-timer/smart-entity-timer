"""Bundled frontend registration for Smart Entity Timer."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant

from .const import FRONTEND_CARD_PATH, FRONTEND_CARD_URL

_LOGGER = logging.getLogger(__name__)
_CARD_FILE = Path(__file__).parent / "www" / "smart-entity-timer-card.js"


async def async_register_frontend(hass: HomeAssistant) -> None:
    """Serve the bundled card and register it as a Lovelace module resource."""
    await hass.http.async_register_static_paths(
        [StaticPathConfig(FRONTEND_CARD_PATH, str(_CARD_FILE), True)]
    )

    lovelace = hass.data.get("lovelace")
    resources = getattr(lovelace, "resources", None) if lovelace is not None else None

    # Storage-mode Lovelace is the normal Home Assistant configuration.  Registering
    # the card here makes the module visible under Settings -> Dashboards -> Resources
    # and guarantees that custom:smart-entity-timer-card is loaded by the frontend.
    if resources is not None and hasattr(resources, "async_get_info"):
        try:
            # Ensure the resource collection is loaded before reading/mutating it.
            await resources.async_get_info()
            items = list(resources.async_items() or [])

            for item in items:
                current_url = str(item.get("url", ""))
                if not current_url.startswith(FRONTEND_CARD_PATH):
                    continue

                if current_url != FRONTEND_CARD_URL and item.get("id"):
                    await resources.async_update_item(
                        item["id"],
                        {"res_type": "module", "url": FRONTEND_CARD_URL},
                    )
                    _LOGGER.info(
                        "Updated Smart Entity Timer Card Lovelace resource to %s",
                        FRONTEND_CARD_URL,
                    )
                return

            if hasattr(resources, "async_create_item"):
                await resources.async_create_item(
                    {"res_type": "module", "url": FRONTEND_CARD_URL}
                )
                _LOGGER.info(
                    "Registered Smart Entity Timer Card Lovelace resource: %s",
                    FRONTEND_CARD_URL,
                )
                return
        except Exception:  # noqa: BLE001 - frontend fallback must not break integration setup
            _LOGGER.exception(
                "Could not register the Smart Entity Timer Card as a Lovelace resource; "
                "falling back to the frontend extra-module loader"
            )

    # Fallback for unusual/non-storage Lovelace configurations. This API does not
    # necessarily appear in the Resources UI, but it can still load an ES module.
    add_extra_js_url(hass, FRONTEND_CARD_URL)
