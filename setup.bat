@echo off
title Setup Aplikasi Kejaksaan
cls

echo.
echo ============================================
echo    SETUP APLIKASI KEJAKSAAN
echo ============================================
echo.

REM Cek Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python tidak ditemukan!
    echo.
    echo Silakan download dan install Python dari:
    echo https://www.python.org/downloads/
    echo.
    echo Pastikan centang "Add Python to PATH" saat install
    pause
    exit /b 1
)

echo [INFO] Python ditemukan...
python --version

REM Pindah ke direktori aplikasi
cd /d "%~dp0"

echo.
echo [INFO] Membuat virtual environment...
python -m venv venv

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Gagal membuat virtual environment!
    pause
    exit /b 1
)

echo [INFO] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

echo [INFO] Mengupdate pip...
python -m pip install --upgrade pip

echo [INFO] Menginstall dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo [INFO] Installing basic dependencies...
    pip install Flask==2.3.3 pandas==2.0.3 openpyxl==3.1.2 matplotlib==3.7.2 numpy==1.24.3
)

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Gagal menginstall dependencies!
    pause
    exit /b 1
)

REM Buat direktori yang diperlukan
if not exist "db" mkdir db
if not exist "csv" mkdir csv

echo.
echo ============================================
echo [SUCCESS] Setup berhasil!
echo.
echo Untuk menjalankan aplikasi:
echo 1. Double-click 'start_app.bat'
echo 2. Atau jalankan: python app_with_db.py
echo ============================================
echo.
pause