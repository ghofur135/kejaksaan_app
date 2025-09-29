# PowerShell script to start the Flask application
Write-Host "Starting PIDUM & PIDSUS Application..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv" -ForegroundColor Yellow
    Write-Host "Then install requirements: .venv\Scripts\pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Using virtual environment Python..." -ForegroundColor Yellow
& .venv\Scripts\python.exe --version

Write-Host "Starting Flask application..." -ForegroundColor Yellow
Write-Host "Application will be available at: http://127.0.0.1:5001" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the application using virtual environment Python
& .venv\Scripts\python.exe app_with_db.py

Read-Host "Press Enter to continue"