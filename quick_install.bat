@echo off
title Quick Install - Aplikasi Kejaksaan
cls

echo.
echo ============================================
echo    QUICK INSTALL - APLIKASI KEJAKSAAN
echo ============================================
echo.

REM Cek Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python tidak terinstall!
    echo.
    echo Mengunduh Python installer...
    echo Silakan install Python terlebih dahulu
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

cd /d "%~dp0"

echo [INFO] Installing dependencies (global)...
pip install Flask pandas openpyxl matplotlib numpy

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Gagal install dependencies!
    pause
    exit /b 1
)

REM Buat direktori
if not exist "db" mkdir db
if not exist "csv" mkdir csv

echo.
echo ============================================
echo [SUCCESS] Quick install berhasil!
echo.
echo Jalankan: start_app.bat
echo ============================================
echo.
pause