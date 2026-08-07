# Mantenimiento del repositorio desde el navegador

Repositorio existente para 0.3.0:

```text
https://github.com/abel-smart-timer/smart-entity-timer
```

No se crea un repositorio nuevo ni se cambia el dominio `smart_entity_timer`.

Versión estable anterior:

```text
v0.2.0
```

Nueva versión:

```text
v0.3.0
```

## Validación completada

La candidata 0.3.0 ya pasó en Home Assistant real:

- instalación limpia;
- creación de múltiples timers;
- reconfiguración centralizada;
- bloqueo de cambios con timers activos;
- eliminación individual de subentries;
- migración de uno y varios timers 0.2.0;
- conservación de entity IDs;
- Card 0.2.2;
- notificaciones personalizadas y eventos.

La prueba de actualizar mientras un timer está activo queda fuera del release gate. El procedimiento soportado exige que todos los timers estén detenidos antes de actualizar.

## Subir 0.3.0

1. Abre `abel-smart-timer/smart-entity-timer`.
2. Usa **Add file → Upload files**.
3. Sube el contenido completo del ZIP de repositorio 0.3.0.
4. Commit sugerido: `Centralize timer management with config subentries in 0.3.0`.
5. Revisa **Actions**.
6. Confirma Python checks, Hassfest y HACS validation en verde.
7. Crea el Release `v0.3.0` y márcalo como **Latest**, no como pre-release.

## Compatibilidad

```text
Smart Entity Timer       0.3.0
Smart Entity Timer Card  0.2.2
Card API                  2
```

La actualización 0.3.0 cambia la topología de configuración, no el contrato Card API.
