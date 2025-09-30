#!/bin/bash

# Script untuk menjalankan aplikasi Kejaksaan dengan Gunicorn (Production)
echo "Starting Kejaksaan Flask Application with Gunicorn (Production Mode)..."
echo "======================================================================"

# Pindah ke direktori proyek
cd /home/dhimas/project/kejaksaan

# Aktifkan virtual environment jika ada
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Jalankan aplikasi dengan gunicorn
echo "Starting Flask application with Gunicorn on http://0.0.0.0:5001"
echo "Press Ctrl+C to stop the application"
echo "======================================================================"

gunicorn --bind 0.0.0.0:5001 --workers 4 app_with_db:app