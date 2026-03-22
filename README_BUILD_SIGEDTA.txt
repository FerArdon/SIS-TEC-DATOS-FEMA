# SIGEDTA - Build y Empaque (Windows)

Este documento explica cómo construir el ejecutable `SIGEDTA_2025.exe` y crear el instalador `Setup_SIGEDTA_2025.exe`.

## 0) Estructura esperada del proyecto
```
SIGEDTA\
  sigedta_main.py
  sigedta_db_advanced.py
  sigedta_export_advanced.py
  sigedta_login.py
  sigedta_ui.py
  sigedta_i18n.py
  requirements.txt
  assets\
    icon_sigedta.ico
    logo_sigedta.png
    campana.wav
  data\
    sigedta_dictamenes.db
```
> Nota: `sigedta_dictamenes.db` incluirá el usuario `admin` con la clave hasheada correspondiente a `F19E12r1963`.

## 1) Instalar dependencias de Python
- Recomendado crear un venv (opcional):
  ```bat
  py -3 -m venv .venv
  .venv\Scripts\activate
  ```
- Instalar paquetes:
  ```bat
  pip install -r requirements.txt
  pip install pyinstaller
  ```

## 2) Construir el ejecutable con PyInstaller
- Coloca este repo como carpeta de trabajo (donde está `sigedta_main.py`).
- Ejecuta:
  ```bat
  build_exe.bat
  ```
- Resultado: `dist\SIGEDTA_2025\SIGEDTA_2025.exe`

## 3) Crear instalador con Inno Setup
- Instala Inno Setup 6.x (si no lo tienes).
- Abre `SIGEDTA_2025_installer.iss` en Inno Setup.
- Asegúrate de haber generado antes la carpeta `dist\SIGEDTA_2025\` (paso 2).
- Compila el script. Obtendrás `Output\Setup_SIGEDTA_2025.exe`.

## 4) Recomendaciones
- Ejecutar el instalador con permisos de admin si instalarás en `C:\Program Files\`.
- `data\backups` se excluirá del desinstalador (para no perder respaldos).

## 5) Solución de problemas comunes
- **Icono no aparece:** Verifica ruta `assets\icon_sigedta.ico` y vuelve a construir.
- **Faltan librerías al ejecutar:** Revisa `--hidden-import` de `build_exe.bat` o agrega la lib faltante al requirements.txt.
- **DB no se crea:** Asegura permisos de escritura en `{app}\data`. Ejecuta como administrador o mueve la DB a `%APPDATA%` si prefieres.

¡Listo! Con esto tendrás `SIGEDTA_2025.exe` y un instalador profesional.