@echo off
REM ============================================
REM PREXCOL - Auto Python Installer
REM Downloads and extracts embedded Python
REM Installs dependencies directly into embed env (no separate venv)
REM ============================================

SET ROOT_DIR=%~dp0..
SET PYTHON_EMBED_DIR=%ROOT_DIR%\.python-embed
SET PYTHON_EXE=%PYTHON_EMBED_DIR%\python.exe
SET PYTHON_VERSION=3.11.7
SET PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip

echo ==========================================
echo PREXCOL - Auto Python Setup
echo ==========================================
echo.

REM Check if embedded Python already exists
if exist "%PYTHON_EXE%" (
    echo [OK] Python embebido encontrado en: %PYTHON_EMBED_DIR%
    "%PYTHON_EXE%" --version
    goto :INSTALL_DEPS
)

echo [*] Python no encontrado. Descargando version embebida...
echo.

REM Create directory
if not exist "%PYTHON_EMBED_DIR%" mkdir "%PYTHON_EMBED_DIR%"

REM Download embedded Python
echo [*] Descargando Python %PYTHON_VERSION% (esto puede tomar unos minutos)...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%ROOT_DIR%\python-embed.zip'}"

if %errorlevel% neq 0 (
    echo [ERROR] Fallo al descargar Python embebido
    echo.
    echo Por favor, descarga manualmente desde:
    echo %PYTHON_URL%
    echo.
    echo Y extrae el contenido en: %PYTHON_EMBED_DIR%
    pause
    exit /b 1
)

REM Extract
echo [*] Extrayendo Python...
powershell -Command "Expand-Archive -Path '%ROOT_DIR%\python-embed.zip' -DestinationPath '%PYTHON_EMBED_DIR%' -Force"

REM Cleanup
del "%ROOT_DIR%\python-embed.zip"
if exist "%PYTHON_EMBED_DIR%\python311._pth" (
    echo [*] Habilitando pip...
    powershell -Command "(Get-Content '%PYTHON_EMBED_DIR%\python311._pth') -replace '#import site', 'import site' | Set-Content '%PYTHON_EMBED_DIR%\python311._pth'"
)

:INSTALL_DEPS
echo.
echo [*] Configurando dependencias en entorno embebido...

REM Ensure pip is installed
if not exist "%PYTHON_EMBED_DIR%\Scripts\pip.exe" (
    echo [*] Instalando Pip...
    powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%PYTHON_EMBED_DIR%\get-pip.py'"
    "%PYTHON_EXE%" "%PYTHON_EMBED_DIR%\get-pip.py" --no-warn-script-location
    del "%PYTHON_EMBED_DIR%\get-pip.py"
)

REM Install project requirements
echo [*] Instalando librerias del proyecto...
"%PYTHON_EXE%" -m pip install --upgrade pip --quiet --no-warn-script-location
"%PYTHON_EXE%" -m pip install -r "%ROOT_DIR%\requirements.txt" --quiet --no-warn-script-location

if %errorlevel% neq 0 (
    echo [ERROR] Fallo al instalar dependencias del proyecto.
    echo Verifica tu conexion a internet.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo [OK] Configuracion Exitosa
echo ==========================================
echo.
echo Python instalado en: %PYTHON_EMBED_DIR%
echo Dependencias instaladas en: %PYTHON_EMBED_DIR%\Lib\site-packages
echo.
exit /b 0
