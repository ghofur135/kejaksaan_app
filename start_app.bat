@echo off
title Aplikasi Kejaksaan - Data PIDUM & PIDSUS
cls

echo.
echo ============================================
echo    APLIKASI KEJAKSAAN - DATA PIDUM & PIDSUS
echo ============================================
echo.

REM Cek apakah Python terinstall
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python tidak ditemukan!
    echo Pastikan Python sudah terinstall dan ada di PATH
    echo.
    pause
    exit /b 1
)

echo [INFO] Python ditemukan...
echo [INFO] Checking dependencies...

REM Pindah ke direktori aplikasi
cd /d "%~dp0"

REM Cek dan aktifkan virtual environment jika ada
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Mengaktifkan virtual environment...
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo [INFO] Mengaktifkan virtual environment (.venv)...
    call .venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment tidak ditemukan
    echo [INFO] Menggunakan Python global...
)

REM Install dependencies jika diperlukan
if exist "requirements.txt" (
    echo [INFO] Mengecek dependencies...
    pip install -q -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Gagal menginstall dependencies!
        pause
        exit /b 1
    )
)

REM Buat direktori database jika belum ada
if not exist "db" mkdir db

echo.
echo ============================================
echo [INFO] Memulai aplikasi...
echo [INFO] URL: http://127.0.0.1:5001
echo [INFO] Tekan Ctrl+C untuk menghentikan
echo ============================================
echo.

REM Buka browser secara otomatis (opsional)
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5001

REM Jalankan aplikasi
python app_with_db.py

REM Jika sampai sini berarti aplikasi sudah ditutup
echo.
echo [INFO] Aplikasi telah dihentikan.
pause