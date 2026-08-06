# Publicación en GitHub desde el navegador

Este paquete está preparado para la organización:

```text
https://github.com/abel-smart-timer
```

El repositorio de la integración debe llamarse exactamente:

```text
smart-entity-timer
```

La dirección final será:

```text
https://github.com/abel-smart-timer/smart-entity-timer
```

## 1. Crear el repositorio

1. Inicia sesión en GitHub.
2. Abre la organización `abel-smart-timer`.
3. En la pestaña **Repositories**, selecciona **New repository**.
4. En **Owner**, confirma que aparezca `abel-smart-timer`.
5. En **Repository name**, escribe `smart-entity-timer`.
6. En **Description**, escribe:

   ```text
   Persistent turn-on and turn-off timers for Home Assistant entities
   ```

7. Selecciona **Public**.
8. No actives **Add a README file**.
9. No agregues `.gitignore`.
10. No elijas una licencia, porque el paquete ya contiene `LICENSE`.
11. Selecciona **Create repository**.

## 2. Descomprimir este ZIP

1. En Windows, haz clic derecho en el ZIP.
2. Selecciona **Extraer todo**.
3. Abre la carpeta extraída.
4. Confirma que dentro se vean directamente estas carpetas y archivos:

   ```text
   .github/
   custom_components/
   docs/
   images/
   .gitignore
   CHANGELOG.md
   hacs.json
   INSTALL.txt
   LICENSE
   README.md
   UPLOAD_TO_GITHUB_ES.txt
   ```

No subas el archivo ZIP como un solo archivo. Debes subir el contenido descomprimido.

## 3. Subir los archivos

1. Abre el repositorio vacío `abel-smart-timer/smart-entity-timer`.
2. Selecciona **uploading an existing file**. Si no aparece, usa **Add file → Upload files**.
3. En el Explorador de Windows, entra en la carpeta extraída.
4. Selecciona todo su contenido.
5. Arrastra las carpetas y archivos a la ventana de GitHub.
6. Espera a que todos los archivos terminen de cargarse.
7. En **Commit message**, escribe:

   ```text
   Add Smart Entity Timer 0.1.2
   ```

8. Selecciona **Commit directly to the main branch**.
9. Presiona **Commit changes**.

## 4. Verificar la estructura

En la página principal del repositorio deben verse, como mínimo:

```text
.github
custom_components
docs
images
CHANGELOG.md
hacs.json
INSTALL.txt
LICENSE
README.md
```

Entra a esta ruta y confirma que existe `manifest.json`:

```text
custom_components/smart_entity_timer/manifest.json
```

El archivo debe apuntar a:

```text
https://github.com/abel-smart-timer/smart-entity-timer
```

## 5. Revisar GitHub Actions

1. Abre la pestaña **Actions** del repositorio.
2. Si GitHub pregunta si deseas habilitar workflows, selecciónalo.
3. Abre la ejecución llamada **Validate**.
4. Revisa los trabajos **Hassfest** y **HACS validation**.
5. En esta primera etapa, guarda el texto completo de cualquier error para corregirlo antes de crear el lanzamiento.

## 6. Configurar la información del repositorio

En la página principal, en el panel **About**, selecciona el icono de engrane y agrega:

Descripción:

```text
Persistent turn-on and turn-off timers for Home Assistant entities
```

Topics:

```text
home-assistant
homeassistant
hacs
custom-integration
timer
smart-home
```

Activa **Issues** en **Settings → General → Features** si no aparece habilitado.

## 7. No crear todavía el Release 0.1.2

Primero deben completarse las pruebas funcionales en Home Assistant. El lanzamiento público `v0.1.2` se creará después de corregir cualquier falla encontrada durante esas pruebas.

## Nota sobre codeowners

El repositorio pertenece a la organización `abel-smart-timer`, pero el campo `codeowners` del manifiesto debe señalar una cuenta personal de GitHub o un equipo concreto de la organización. En este paquete queda vacío hasta definir ese responsable. Esto no impide probar la integración ni alojar el código.
