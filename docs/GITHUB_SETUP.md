# Mantenimiento del repositorio desde el navegador

Repositorio:

```text
https://github.com/abel-smart-timer/smart-entity-timer
```

Versión estable publicada:

```text
v0.1.3
```

Candidata de desarrollo actual:

```text
0.2.0
```

La versión 0.1.3 debe permanecer como Release estable mientras 0.2.0 se prueba en HAOS real.

## Probar 0.2.0 sin reemplazar todavía el Release estable

1. Descarga el ZIP de instalación 0.2.0 generado para pruebas.
2. Haz respaldo de Home Assistant.
3. Reemplaza `/config/custom_components/smart_entity_timer/` con los archivos 0.2.0.
4. Reinicia Home Assistant.
5. Conserva los helpers existentes.
6. Ejecuta T30–T36 de `docs/TEST_PLAN.md`.
7. Si aparece un problema, vuelve a instalar el Release 0.1.3 desde HACS o restaura el respaldo.

## Subir código 0.2.0 a GitHub

No es necesario subirlo a `main` antes de terminar las pruebas locales. Cuando la candidata pase las pruebas:

1. Abre `abel-smart-timer/smart-entity-timer`.
2. Selecciona **Add file → Upload files**.
3. Arrastra el contenido del ZIP completo del repositorio 0.2.0.
4. Usa un commit descriptivo, por ejemplo `Add customizable notifications and lifecycle events in 0.2.0`.
5. Revisa **Actions** y confirma Python checks, Hassfest y HACS validation en verde.
6. Repite una prueba rápida desde HAOS con esos mismos archivos.
7. Solo entonces crea el Release `v0.2.0`.

## No reutilizar tags

El Release estable `v0.1.3` representa el código ya validado y no debe modificarse ni reemplazarse. Cada nueva versión usa un tag nuevo.

## HACS

Smart Entity Timer se distribuye como integración HACS. La estructura debe conservarse:

```text
custom_components/
└── smart_entity_timer/
    ├── manifest.json
    ├── __init__.py
    └── ...
```

## Tarjeta compatible

```text
Smart Entity Timer estable        0.1.3
Smart Entity Timer candidata      0.2.0
Smart Entity Timer Card           0.2.2
Card API                           2
```

0.2.0 no cambia Card API, por lo que la tarjeta 0.2.2 debe continuar funcionando sin modificaciones.
