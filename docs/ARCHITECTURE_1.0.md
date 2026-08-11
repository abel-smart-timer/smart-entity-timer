# Smart Entity Timer 1.0.0 architecture

## Distribution

Smart Entity Timer 1.0.0 is distributed as one HACS **integration** repository. All runtime files, including the compiled dashboard card, live below `custom_components/smart_entity_timer/`, matching HACS integration packaging requirements.

```text
custom_components/smart_entity_timer/
├── backend Python modules
├── manifest.json
├── brand/
├── translations/
├── frontend.py
└── www/
    └── smart-entity-timer-card.js
```

## Frontend loading

`frontend.py` registers the bundled file with `hass.http.async_register_static_paths()` and calls Home Assistant frontend `add_extra_js_url()` with a versioned URL. The version query acts as a cache buster.

The bundled card still registers the custom element `smart-entity-timer-card`, so existing dashboards do not change their `type:` value.

## Development source

The card source remains in `abel-smart-timer/smart-entity-timer-card`. Stable compiled output is copied into the integration package for user distribution. After the 1.0.0 transition, the card repository is development-only and should be removed from the default HACS catalog, not deleted from GitHub.

## Compatibility

- Backend topology remains parent ConfigEntry + timer Config Subentries.
- Card API remains v2.
- Existing timer entity IDs and persistent storage are not intentionally changed.
- Existing card YAML continues to use `custom:smart-entity-timer-card`.
