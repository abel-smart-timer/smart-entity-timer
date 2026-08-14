# Smart Entity Timer 1.0.0 architecture

## Distribution

Smart Entity Timer 1.0.0 is distributed as one HACS **integration** repository. All user-facing runtime files, including the compiled dashboard card, live below `custom_components/smart_entity_timer/`.

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

`frontend.py`:

1. serves the bundled card with `hass.http.async_register_static_paths()`;
2. loads the Lovelace resource collection;
3. creates the module resource when absent;
4. updates an existing Smart Entity Timer bundled-resource URL when the package version changes;
5. falls back to Home Assistant's frontend extra-module loader for unusual/non-storage Lovelace configurations.

The version query is a cache buster. For 1.0.0 the normal resource URL is:

```text
/smart_entity_timer_static/smart-entity-timer-card.js?v=1.0.0
```

The bundled card still registers the custom element `smart-entity-timer-card`, so existing dashboards keep the same `type:` value.

## Development source

The card source remains in `abel-smart-timer/smart-entity-timer-card`. Stable compiled output is copied into the integration package for user distribution. After the 1.0.0 transition, that repository is development-only and is intended to be removed from the default HACS catalog, not deleted from GitHub.

## Compatibility

- Backend topology remains parent ConfigEntry + Timer Config Subentries.
- Card API remains v2.
- Existing timer entity IDs and persistent storage are not intentionally changed.
- Existing card YAML continues to use `custom:smart-entity-timer-card`.
