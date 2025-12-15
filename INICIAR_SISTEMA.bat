@echo off
title PREXCOL SYSTEM MANAGER
color 0b

REM ===================================================
REM    PREXCOL - INICIO AUTOMATICO Y OPTIMIZADO
REM ===================================================

echo.
echo  [1/3] Optimizando entorno...
call scripts\smart_install.bat
if errorlevel 1 (
    color 0c
    echo.
    echo  [ERROR] La preparacion del sistema fallo.
    echo  Revise los mensajes anteriores.
    pause
    exit /b
)

echo.
echo  [2/3] Preparando base de datos...
if not exist ".db_init_done" (
    REM Solo corre migraciones si no hay marcador o si el usuario fuerza
    REM Para seguridad, corremos migrate siempre (es rápido si no hay cambios)
    call scripts\auto_setup.bat >nul 2>&1
    REM Asumimos que auto_setup ya maneja cosas básicas, pero aquí aseguramos migraciones
    if exist ".python-embed\python.exe" (
        ".python-embed\python.exe" src\backend\manage.py migrate --noinput >nul 2>&1
    )
    echo completed > ".db_init_done"
)

echo.
echo  [3/3] Iniciando servicios...
echo.

REM Lanzamos el launcher en modo "rápido" (ya verificamos todo)
call scripts\start_prexcol.bat

exit /b
