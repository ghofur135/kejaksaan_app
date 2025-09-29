@echo off
echo Starting PIDUM & PIDSUS Application...
echo =====================================

REM Check if virtual environment exists
if not exist .venv\Scripts\python.exe (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then install requirements: .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo Using virtual environment Python...
.venv\Scripts\python.exe --version

echo Starting Flask application...
echo Application will be available at: http://127.0.0.1:5001
echo Press Ctrl+C to stop the server
echo.
.venv\Scripts\python.exe app_with_db.py

pause