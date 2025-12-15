@echo off
REM ============================================
REM PREXCOL - Smart Optimizer Installer
REM Gestiona instalaciones con caché y verificaciones rápidas
REM ============================================

set "ROOT_DIR=%~dp0.."
set "EMBED_DIR=%ROOT_DIR%\.python-embed"
set "PYTHON_EXE=%EMBED_DIR%\python.exe"
set "REQ_FILE=%ROOT_DIR%\requirements.txt"
set "MARKER_FILE=%ROOT_DIR%\.install_marker"

echo [OPTIMIZER] Analizando estado del sistema...

REM 1. VERIFICAR PYTHON (Core)
if not exist "%PYTHON_EXE%" (
    echo [SETUP] Python no detectado. Iniciando auto-setup completo...
    call "%~dp0auto_setup.bat"
    if errorlevel 1 exit /b 1
    goto :UPDATE_MARKER
)

REM 2. VERIFICAR DEPENDENCIAS (Smart update)
REM Si el requirements.txt es más nuevo que nuestro marcador, actualizamos.
REM En Batch puro comparar fechas es doloroso, usaremos una estrategia siempre-check silenciosa.
REM Pip es rápido si ya está todo instalado.

echo [CHECK] Verificando librerias Python...
"%PYTHON_EXE%" -m pip install -r "%REQ_FILE%" --quiet --no-warn-script-location --disable-pip-version-check
if errorlevel 1 (
    echo [ERROR] Fallo al actualizar dependencias backend.
    exit /b 1
)

REM 3. VERIFICAR FRONTEND (Smart install)
set "FRONT_DIR=%ROOT_DIR%\src\frontend"
if not exist "%FRONT_DIR%\node_modules" (
    echo [SETUP] Instalando modulos Frontend - primera vez...
    cd /d "%FRONT_DIR%"
    
    REM Intento 1: Standard
    call npm install --no-audit --no-fund --quiet
    if errorlevel 1 (
        echo [WARN] Fallo instalacion estandar. Reintentando con legacy-peer-deps...
        call npm install --legacy-peer-deps --no-audit --no-fund --quiet
        if errorlevel 1 (
            echo [ERROR] Fallo critico en instalacion de Frontend. Revisa los logs.
            cd /d "%ROOT_DIR%"
            exit /b 1
        )
    )
    
    cd /d "%ROOT_DIR%"
) else (
    REM Check rapido opcional
    echo [CHECK] Frontend listo.
)

:UPDATE_MARKER
echo %date% %time% > "%MARKER_FILE%"
echo [OPTIMIZER] Sistema listo y optimizado.
exit /b 0
