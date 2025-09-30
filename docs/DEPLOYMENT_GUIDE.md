# Kejaksaan Application - Setup Guide

## Prerequisites
- Python 3.10 atau lebih tinggi
- pip3 package manager

## Installation

### 1. Install Dependencies
```bash
cd /home/dhimas/project/kejaksaan
pip3 install -r requirements.txt
```

### 2. Database Setup
Database SQLite akan otomatis dibuat pada saat aplikasi pertama kali dijalankan di:
- Path: `/home/dhimas/project/kejaksaan/db/kejaksaan.db`

## Running the Application

### Development Mode (Recommended for testing)
```bash
# Menggunakan script yang sudah disediakan
./run_app.sh

# Atau jalankan langsung
python3 app_with_db.py
```

Aplikasi akan berjalan di: http://127.0.0.1:5001

### Production Mode
```bash
# Menggunakan Gunicorn untuk production
./run_production.sh

# Atau jalankan langsung
gunicorn --bind 0.0.0.0:5001 --workers 4 app_with_db:app
```

Aplikasi akan berjalan di: http://0.0.0.0:5001 (accessible dari network)

## Features
- **Input PIDUM**: Form untuk memasukkan data PIDUM
- **Input PIDSUS**: Form untuk memasukkan data PIDSUS  
- **View Data**: Melihat data yang telah diinput
- **Charts**: Visualisasi data dalam bentuk grafik
- **Export Excel**: Export data ke file Excel dengan styling
- **Database Management**: Otomatis menggunakan SQLite database

## Application Structure
```
/home/dhimas/project/kejaksaan/
├── app_with_db.py          # Main Flask application
├── database.py             # Database functions
├── requirements.txt        # Python dependencies
├── run_app.sh             # Development server script
├── run_production.sh      # Production server script
├── templates/             # HTML templates
├── static/               # Static files (CSS, JS, images)
└── db/                  # SQLite database directory
    └── kejaksaan.db     # Main database file
```

## Troubleshooting

### Port Already in Use
Jika port 5001 sudah digunakan, edit file `app_with_db.py` pada baris terakhir:
```python
app.run(debug=True, port=5002)  # Ganti ke port lain
```

### Permission Denied
Jika script tidak bisa dijalankan:
```bash
chmod +x run_app.sh
chmod +x run_production.sh
```

### Database Issues
Jika ada masalah dengan database, hapus file database dan restart aplikasi:
```bash
rm db/kejaksaan.db
python3 app_with_db.py
```

## Security Notes
- Aplikasi menggunakan secret key default, ubah untuk production
- Development server tidak cocok untuk production
- Gunakan reverse proxy (nginx) untuk production deployment

## Version Compatibility
- Python: 3.10+
- Flask: 2.3.3
- Dependencies: Lihat requirements.txt untuk versi lengkap