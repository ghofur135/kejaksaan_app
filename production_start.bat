@echo off
title Aplikasi Kejaksaan - Production Mode
cls

echo.
echo ============================================
echo    PRODUCTION MODE - APLIKASI KEJAKSAAN
echo ============================================
echo.

cd /d "%~dp0"

REM Aktifkan virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo [INFO] Starting in PRODUCTION mode...
echo [INFO] Using Gunicorn server
echo [INFO] URL: http://127.0.0.1:5001
echo.

REM Cek apakah gunicorn terinstall
pip show gunicorn >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Installing Gunicorn...
    pip install gunicorn
)

REM Set environment variables untuk production
set FLASK_ENV=production
set FLASK_DEBUG=0

REM Jalankan dengan gunicorn
gunicorn --bind 127.0.0.1:5001 --workers 2 --timeout 120 app_with_db:app

pause