#!/bin/bash

# Script untuk menjalankan aplikasi Kejaksaan
echo "Starting Kejaksaan Flask Application..."
echo "============================================="

# Pindah ke direktori proyek
cd /home/dhimas/project/kejaksaan

# Aktifkan virtual environment jika ada
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Jalankan aplikasi
echo "Starting Flask application on http://127.0.0.1:5001"
echo "Press Ctrl+C to stop the application"
echo "============================================="

python3 app_with_db.py