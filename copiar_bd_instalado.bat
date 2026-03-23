@echo off
echo ================================================
echo  SIGEDTA - Copiar base de datos al instalado
echo ================================================
echo.

set ORIGEN=C:\Program Files\SIGEDTA\data\sistecdatos_dictamenes.db
set DESTINO=C:\Program Files\SIGEDTA\_internal\data\sistecdatos_dictamenes.db

echo Copiando BD con los 37 dictamenes...
copy /Y "%ORIGEN%" "%DESTINO%"

if %ERRORLEVEL% == 0 (
    echo.
    echo ✓ EXITO: Base de datos copiada correctamente.
    echo   Ahora abre SIGEDTA 2025 y veras todos los dictamenes.
) else (
    echo.
    echo ✗ ERROR: No se pudo copiar. Asegurate de ejecutar como Administrador.
)

echo.
pause
