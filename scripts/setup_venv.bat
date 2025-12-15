@echo off
REM ============================================
REM PREXCOL - Smart Python Detector + Venv Setup
REM Finds Python installation and creates venv
REM ============================================

echo [*] Buscando instalacion de Python...

REM Try common Python locations
set "PYTHON_FOUND="

REM 1. Try standard 'python' command
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
    set "PYTHON_FOUND=1"
    echo [OK] Python encontrado en PATH
    goto :FOUND_PYTHON
)

REM 2. Try 'py' launcher (Windows Python Launcher)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py"
    set "PYTHON_FOUND=1"
    echo [OK] Python Launcher encontrado
    goto :FOUND_PYTHON
)

REM 3. Try AppData locations
set "PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
if exist "%PYTHON_PATH%" (
    set "PYTHON_CMD=%PYTHON_PATH%"
    set "PYTHON_FOUND=1"
    echo [OK] Python encontrado en: %PYTHON_PATH%
    goto :FOUND_PYTHON
)

set "PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if exist "%PYTHON_PATH%" (
    set "PYTHON_CMD=%PYTHON_PATH%"
    set "PYTHON_FOUND=1"
    echo [OK] Python encontrado en: %PYTHON_PATH%
    goto :FOUND_PYTHON
)

set "PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if exist "%PYTHON_PATH%" (
    set "PYTHON_CMD=%PYTHON_PATH%"
    set "PYTHON_FOUND=1"
    echo [OK] Python encontrado en: %PYTHON_PATH%
    goto :FOUND_PYTHON
)

REM 4. Try Program Files
set "PYTHON_PATH=C:\Python39\python.exe"
if exist "%PYTHON_PATH%" (
    set "PYTHON_CMD=%PYTHON_PATH%"
    set "PYTHON_FOUND=1"
    echo [OK] Python encontrado en: %PYTHON_PATH%
    goto :FOUND_PYTHON
)

set "PYTHON_PATH=C:\Python310\python.exe"
if exist "%PYTHON_PATH%" (
    set "PYTHON_CMD=%PYTHON_PATH%"
    set "PYTHON_FOUND=1"
    echo [OK] Python encontrado en: %PYTHON_PATH%
    goto :FOUND_PYTHON
)

REM Not found
if not defined PYTHON_FOUND (
    echo [ERROR] Python no encontrado en el sistema
    echo.
    echo Por favor:
    echo 1. Instala Python desde https://www.python.org/downloads/
    echo 2. Durante la instalacion, marca "Add Python to PATH"
    echo 3. Reinicia esta terminal
    echo.
    pause
    exit /b 1
)

:FOUND_PYTHON
echo.
echo [*] Usando Python: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

SET ROOT_DIR=%~dp0..
SET VENV_DIR=%ROOT_DIR%\.venv

REM Remove existing venv if corrupt
if exist "%VENV_DIR%" (
    echo [*] Removiendo entorno virtual existente...
    rmdir /s /q "%VENV_DIR%"
)

REM Create new venv
echo [*] Creando nuevo entorno virtual...
%PYTHON_CMD% -m venv "%VENV_DIR%"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate and upgrade pip
echo [*] Activando entorno y actualizando pip...
call "%VENV_DIR%\Scripts\activate.bat"
python -m pip install --upgrade pip --quiet

REM Install requirements
echo [*] Instalando dependencias...
pip install -r "%ROOT_DIR%\requirements.txt" --quiet --no-warn-script-location

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [OK] Entorno virtual creado exitosamente
echo.
echo Ahora puedes ejecutar: scripts\start_prexcol.bat
echo.
pause
exit /b 0
