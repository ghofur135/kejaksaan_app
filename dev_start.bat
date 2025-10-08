@echo off
title Aplikasi Kejaksaan - Development Mode
cls

echo.
echo ============================================
echo    DEVELOPMENT MODE - APLIKASI KEJAKSAAN
echo ============================================
echo.

cd /d "%~dp0"

REM Aktifkan virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo [INFO] Starting in DEBUG mode...
echo [INFO] Auto-reload enabled
echo [INFO] URL: http://127.0.0.1:5001
echo.

REM Set environment variables untuk development
set FLASK_ENV=development
set FLASK_DEBUG=1

python app_with_db.py

pause