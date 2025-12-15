@echo off
REM ============================================
REM PREXCOL - Auto Python Installer
REM Downloads and extracts embedded Python if not found
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
    goto :SETUP_VENV
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

REM Enable pip in embedded Python
echo [*] Habilitando pip...
powershell -Command "(Get-Content '%PYTHON_EMBED_DIR%\python311._pth') -replace '#import site', 'import site' | Set-Content '%PYTHON_EMBED_DIR%\python311._pth'"

REM Download get-pip.py
echo [*] Instalando pip...
powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%PYTHON_EMBED_DIR%\get-pip.py'"
"%PYTHON_EXE%" "%PYTHON_EMBED_DIR%\get-pip.py" --quiet

REM Cleanup
del "%PYTHON_EMBED_DIR%\get-pip.py"

echo.
echo [OK] Python %PYTHON_VERSION% instalado exitosamente
echo.

:SETUP_VENV
echo [*] Creando entorno virtual con Python embebido...
echo.

SET VENV_DIR=%ROOT_DIR%\.venv

REM Remove existing venv if exists
if exist "%VENV_DIR%" (
    echo [*] Removiendo entorno virtual anterior...
    rmdir /s /q "%VENV_DIR%"
)

REM Create venv
"%PYTHON_EXE%" -m venv "%VENV_DIR%"
if %errorlevel% neq 0 (
    echo [ERROR] Fallo al crear entorno virtual
    pause
    exit /b 1
)

REM Activate and install dependencies
echo [*] Instalando dependencias del proyecto...
call "%VENV_DIR%\Scripts\activate.bat"
python -m pip install --upgrade pip --quiet
pip install -r "%ROOT_DIR%\requirements.txt" --quiet

if %errorlevel% neq 0 (
    echo [ERROR] Fallo al instalar dependencias
    pause
    exit /b 1
)

echo.
echo ==========================================
echo [OK] Configuracion completada
echo ==========================================
echo.
echo Python embebido instalado en: %PYTHON_EMBED_DIR%
echo Entorno virtual creado en: %VENV_DIR%
echo.
echo Ahora puedes ejecutar: scripts\start_prexcol.bat
echo.
pause
exit /b 0
