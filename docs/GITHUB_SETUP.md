# Mantenimiento del repositorio desde el navegador

Repositorio del producto distribuido:

```text
https://github.com/abel-smart-timer/smart-entity-timer
```

Repositorio de desarrollo del frontend:

```text
https://github.com/abel-smart-timer/smart-entity-timer-card
```

Desde 1.0.0, el usuario instala únicamente **Smart Entity Timer** desde HACS. El JavaScript compilado de la Card se incluye dentro de la integración.

## Antes de publicar 1.0.0

1. Detén/cancela todos los timers activos.
2. Crea un backup de Home Assistant.
3. Sube la candidata 1.0.0 a `main` sin crear todavía un Release.
4. Confirma Python checks, Bundled frontend checks, Hassfest y HACS validation en verde.
5. Prueba instalación limpia desde HACS seleccionando `main`.
6. Prueba actualización desde Smart Entity Timer 0.3.0 + Smart Entity Timer Card 0.3.0.
7. En la actualización, elimina la Card independiente de HACS antes de reiniciar Home Assistant.
8. Confirma que las entidades conservan sus `entity_id` y que las tarjetas existentes no requieren cambios de YAML.
9. Completa `docs/TEST_PLAN_1.0.0.md`.

## Publicación

Solo después de aprobar todas las pruebas:

1. Crea el Release `v1.0.0` apuntando al commit validado de `main`.
2. Márcalo como Latest y no como Pre-release.
3. Revisa cuidadosamente tag, commit y notas antes de publicar porque Immutable Releases está activado.
4. Después de publicar, confirma que HACS ofrece 1.0.0 como versión normal.
5. Solicita a HACS retirar `abel-smart-timer/smart-entity-timer-card` del catálogo default usando el issue template **Request for repository removal**.
6. No elimines ni archives el repositorio de la Card: seguirá siendo el repositorio de desarrollo del frontend.

## Compatibilidad

```text
Smart Entity Timer  1.0.0
Bundled Card         1.0.0
Card API             2
```
