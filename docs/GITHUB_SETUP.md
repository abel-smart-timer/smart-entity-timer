# Mantenimiento del repositorio desde el navegador

Repositorio:

```text
https://github.com/abel-smart-timer/smart-entity-timer
```

Versión estable actual:

```text
v0.1.3
```

La integración ya tiene Release publicado y validaciones de GitHub Actions/HACS funcionando. Este documento reemplaza las instrucciones iniciales de creación del repositorio.

## Actualizar archivos desde el navegador

1. Abre `abel-smart-timer/smart-entity-timer`.
2. Selecciona **Add file → Upload files**.
3. Arrastra únicamente los archivos/carpetas que deseas reemplazar o agregar.
4. Revisa la lista de cambios antes del commit.
5. Escribe un mensaje de commit descriptivo.
6. Guarda directamente en `main` cuando se trate de una actualización pequeña y revisada.
7. Abre **Actions** y confirma que las validaciones terminen en verde.

## Actualizaciones solo de documentación

Una corrección de README, INSTALL o archivos bajo `docs/` no requiere cambiar la versión del `manifest.json` si no cambia el código distribuido de la integración.

El Release `v0.1.3` continúa representando exactamente el código que fue probado y publicado. Los cambios documentales posteriores permanecen en `main` hasta el siguiente Release.

## Flujo para una nueva versión de código

1. Actualiza el código y la versión del manifiesto.
2. Actualiza `CHANGELOG.md` y documentación relevante.
3. Sube los cambios a `main`.
4. Espera a que GitHub Actions termine en verde.
5. Prueba la versión en Home Assistant real.
6. Crea un nuevo Release con un tag nuevo, por ejemplo `v0.1.4` o `v0.2.0`.
7. No reutilices un tag existente para código diferente.

## HACS

Smart Entity Timer se distribuye como integración HACS.

La estructura principal debe conservarse:

```text
custom_components/
└── smart_entity_timer/
    ├── manifest.json
    ├── __init__.py
    └── ...
```

Después de cualquier cambio relevante revisa en GitHub Actions:

- Python checks;
- Hassfest;
- HACS validation.

## Repositorio de la tarjeta

La tarjeta se mantiene separada en:

```text
https://github.com/abel-smart-timer/smart-entity-timer-card
```

Esto es intencional: HACS administra la integración y el plugin Dashboard como tipos de repositorio distintos.

## Versiones compatibles actuales

```text
Smart Entity Timer       0.1.3
Smart Entity Timer Card  0.2.2
Card API                  2
```

## Próximas funciones

Las ideas que todavía no forman parte de la versión estable deben documentarse en `docs/ROADMAP.md` y no presentarse en README como funciones existentes.
