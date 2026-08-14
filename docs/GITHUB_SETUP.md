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

## Publicación de 1.0.0

1. Sube el paquete final 1.0.0 a `main`.
2. Confirma que Python checks, Bundled frontend checks, Hassfest y HACS validation estén verdes.
3. Confirma `manifest.json`, `const.py` y `CARD_VERSION` en 1.0.0.
4. Crea el Release `v1.0.0` apuntando exactamente al commit validado de `main`.
5. Márcalo como Latest y no como Pre-release.
6. Revisa cuidadosamente tag, commit y notas antes de publicar porque Immutable Releases está activado.
7. Después de publicar, actualiza una instalación RC2 a 1.0.0 desde HACS.
8. Reinicia Home Assistant y confirma el recurso `/smart_entity_timer_static/smart-entity-timer-card.js?v=1.0.0`.
9. Confirma que las tarjetas existentes y una tarjeta nueva funcionan.
10. Solicita a HACS retirar `abel-smart-timer/smart-entity-timer-card` del catálogo default usando **Request for repository removal**.
11. No elimines ni archives el repositorio de la Card: seguirá siendo el repositorio de desarrollo del frontend.

## Versionado posterior

```text
1.0.x  bug fixes compatibles
1.x.0  nuevas funciones compatibles
2.0.0  cambios deliberadamente incompatibles
```

## Compatibilidad

```text
Smart Entity Timer  1.0.0
Bundled Card         1.0.0
Card API             2
```
