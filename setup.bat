@echo off
echo ========================================
echo   SETUP APLIKASI PIDUM & PIDSUS  
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python tidak terdeteksi di system!
    echo Silakan install Python terlebih dahulu dari python.org
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version

echo [2/4] Creating virtual environment...
if exist .venv (
    echo Virtual environment sudah ada, skip...
) else (
    python -m venv .venv
    echo Virtual environment berhasil dibuat!
)

echo [3/4] Installing dependencies...
.venv\Scripts\pip.exe install --upgrade pip
.venv\Scripts\pip.exe install -r requirements.txt

echo [4/4] Testing installation...
.venv\Scripts\python.exe -c "import flask, pandas, matplotlib, database; print('✅ Semua dependencies berhasil diinstall!')"

echo.
echo ========================================
echo   SETUP SELESAI!
echo ========================================
echo.
echo Untuk menjalankan aplikasi:
echo   1. Double-click start.bat
echo   2. Atau jalankan: .venv\Scripts\python.exe app_with_db.py
echo.
echo URL aplikasi: http://127.0.0.1:5001
echo.
pause