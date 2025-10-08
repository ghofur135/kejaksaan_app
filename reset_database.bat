@echo off
title Reset Database - Aplikasi Kejaksaan
cls

echo.
echo ============================================
echo    RESET DATABASE - APLIKASI KEJAKSAAN
echo ============================================
echo.
echo PERINGATAN: Ini akan menghapus SEMUA data!
echo.
set /p confirm=Apakah Anda yakin? (y/N): 

if /i "%confirm%" NEQ "y" (
    echo [INFO] Operasi dibatalkan
    pause
    exit /b 0
)

cd /d "%~dp0"

REM Aktifkan virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo.
echo [INFO] Menghapus database...

if exist "db\kejaksaan.db" (
    del "db\kejaksaan.db"
    echo [SUCCESS] Database berhasil dihapus
) else (
    echo [INFO] Database tidak ditemukan
)

echo [INFO] Menjalankan aplikasi untuk membuat database baru...
python -c "from database import init_database; init_database(); print('[SUCCESS] Database baru berhasil dibuat')"

echo.
echo ============================================
echo [SUCCESS] Reset database selesai!
echo ============================================
echo.
pause