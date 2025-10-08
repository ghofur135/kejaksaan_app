# 📦 Windows Deployment Guide

## Aplikasi Kejaksaan - Data PIDUM & PIDSUS

### 🎯 Tentang Script Deployment

Repository ini telah dilengkapi dengan batch scripts untuk memudahkan deployment dan running aplikasi di sistem Windows. Scripts ini dirancang untuk user yang sudah memiliki Python terinstall di PC mereka.

---

## 📋 Prasyarat

### Sistem Requirements
- **OS**: Windows 7/8/10/11 (32-bit atau 64-bit)
- **Python**: 3.7 atau lebih baru
- **RAM**: Minimum 2GB (Recommended 4GB)
- **Storage**: 500MB free space
- **Browser**: Chrome, Firefox, Edge, atau Safari

### Cek Instalasi Python
```cmd
python --version
```

Jika Python belum terinstall:
1. Download dari [python.org](https://www.python.org/downloads/)
2. ✅ **PENTING**: Centang "Add Python to PATH" saat install
3. Restart Command Prompt setelah instalasi

---

## 🚀 Quick Start (3 Langkah)

### Langkah 1: Download Repository
```bash
git clone https://github.com/ghofur135/kejaksaan_app.git
cd kejaksaan_app
```

### Langkah 2: Setup Aplikasi
Double-click: `setup.bat`

### Langkah 3: Jalankan Aplikasi
Double-click: `start_app.bat`

🎉 **Selesai!** Browser akan terbuka otomatis ke `http://127.0.0.1:5001`

---

## 📁 Daftar Script Tersedia

### 🏃‍♂️ Script Utama

| Script | Fungsi | Kapan Digunakan |
|--------|--------|------------------|
| `start_app.bat` | **Jalankan aplikasi** | Penggunaan sehari-hari |
| `setup.bat` | **Setup awal** | Pertama kali install |

### 🔧 Script Development

| Script | Fungsi | Target User |
|--------|--------|-------------|
| `dev_start.bat` | Mode development + debug | Developer |
| `production_start.bat` | Mode production + Gunicorn | Server deployment |

### 🛠️ Script Utility

| Script | Fungsi | Peringatan |
|--------|--------|-----------|
| `reset_database.bat` | Reset semua data | ⚠️ **DESTRUCTIVE** |
| `quick_install.bat` | Install tanpa venv | Advanced user |

---

## 📖 Panduan Detail Script

### 🎯 `start_app.bat` - Script Utama

**Fungsi Utama:**
- Auto-detect Python installation
- Activate virtual environment (jika ada)
- Install/update dependencies otomatis
- Buka browser ke aplikasi
- Handle error dengan pesan jelas

**Cara Penggunaan:**
1. Double-click `start_app.bat`
2. Tunggu loading (~30 detik pertama kali)
3. Browser terbuka otomatis
4. Tekan `Ctrl+C` di Command Prompt untuk stop

**Output yang Normal:**
```
============================================
   APLIKASI KEJAKSAAN - DATA PIDUM & PIDSUS
============================================

[INFO] Python ditemukan...
[INFO] Checking dependencies...
[INFO] Mengaktifkan virtual environment...

============================================
[INFO] Memulai aplikasi...
[INFO] URL: http://127.0.0.1:5001
[INFO] Tekan Ctrl+C untuk menghentikan
============================================
```

### 🔧 `setup.bat` - Setup Awal

**Kapan Digunakan:**
- Pertama kali install aplikasi
- Setelah update dependencies
- Jika virtual environment corrupted

**Proses Setup:**
1. Validasi Python installation
2. Buat virtual environment baru
3. Upgrade pip ke versi terbaru
4. Install semua dependencies dari `requirements.txt`
5. Buat direktori yang diperlukan (`db`, `csv`)

**Durasi**: ~2-5 menit (tergantung koneksi internet)

### 🐛 `dev_start.bat` - Development Mode

**Untuk Developer:**
- Flask debug mode enabled
- Auto-reload saat file berubah
- Error messages lebih detail
- Hot-reload templates

**Environment Variables:**
```batch
set FLASK_ENV=development
set FLASK_DEBUG=1
```

### 🚀 `production_start.bat` - Production Mode

**Untuk Server Deployment:**
- Menggunakan Gunicorn WSGI server
- Multi-worker support (2 workers default)
- Timeout handling (120s)
- Error logging
- Better performance untuk multiple users

**Gunicorn Configuration:**
```bash
gunicorn --bind 127.0.0.1:5001 --workers 2 --timeout 120 app_with_db:app
```

### ⚠️ `reset_database.bat` - Database Reset

**⚠️ PERINGATAN: Script ini akan menghapus SEMUA data!**

**Proses Reset:**
1. Konfirmasi user (y/N)
2. Hapus file `db/kejaksaan.db`
3. Jalankan `init_database()` untuk buat database kosong
4. Konfirmasi berhasil

**Kapan Digunakan:**
- Development testing
- Corrupted database
- Fresh start dengan data kosong

### ⚡ `quick_install.bat` - Quick Install

**Untuk Advanced User:**
- Install dependencies ke Python global (tanpa virtual environment)
- Setup cepat tanpa isolation
- Cocok untuk testing atau demo

**⚠️ Catatan**: Tidak recommended untuk production

---

## 🔍 Troubleshooting

### ❌ Error: "Python tidak ditemukan"

**Solusi:**
1. Reinstall Python dengan centang "Add to PATH"
2. Atau tambah manual Python ke PATH:
   ```
   C:\Python39\
   C:\Python39\Scripts\
   ```
3. Restart Command Prompt
4. Test: `python --version`

### ❌ Error: "Gagal menginstall dependencies"

**Kemungkinan Penyebab:**
- Koneksi internet bermasalah
- Firewall/antivirus blocking
- Disk space tidak cukup
- Permission issues

**Solusi:**
1. Cek koneksi internet
2. Run Command Prompt as Administrator
3. Disable antivirus sementara
4. Gunakan `quick_install.bat`

### ❌ Error: "Port 5001 already in use"

**Solusi:**
1. Kill process yang menggunakan port 5001:
   ```cmd
   netstat -ano | findstr :5001
   taskkill /PID <PID_NUMBER> /F
   ```
2. Atau ubah port di `app_with_db.py`:
   ```python
   app.run(debug=True, port=5002)
   ```

### ❌ Browser tidak terbuka otomatis

**Solusi Manual:**
1. Buka browser manual
2. Navigate ke: `http://127.0.0.1:5001`
3. Atau: `http://localhost:5001`

### ❌ Virtual Environment issues

**Fix Virtual Environment:**
1. Hapus folder `venv`
2. Jalankan `setup.bat` lagi
3. Atau gunakan `quick_install.bat`

---

## 🎛️ Advanced Configuration

### Custom Port
Edit `app_with_db.py` baris terakhir:
```python
app.run(debug=True, port=5002)  # Ganti ke port lain
```

### Custom Database Path
Edit `database.py`:
```python
DATABASE_PATH = 'custom/path/kejaksaan.db'
```

### Production Server
Untuk server production dengan akses eksternal:
```python
app.run(host='0.0.0.0', port=5001)  # Akses dari IP manapun
```

**⚠️ Security**: Pastikan firewall configured dengan benar!

---

## 📊 Performance Tips

### Untuk PC dengan RAM Terbatas (<4GB)
1. Tutup aplikasi lain saat running
2. Gunakan `quick_install.bat` (lebih ringan)
3. Avoid bulk import data (>1000 records)

### Untuk Multiple Users
1. Gunakan `production_start.bat`
2. Increase Gunicorn workers:
   ```bash
   gunicorn --workers 4 app_with_db:app
   ```
3. Consider database optimization

---

## 🔒 Security Considerations

### Development vs Production

| Environment | Security Level | Akses |
|-------------|----------------|-------|
| Development | ⚠️ Low | localhost only |
| Production | ✅ Higher | Network access |

### Production Deployment
- Ganti `SECRET_KEY` di `app_with_db.py`
- Setup proper firewall rules
- Use HTTPS dengan reverse proxy (nginx/Apache)
- Regular database backups

---

## 📞 Support & Troubleshooting

### Log Files Location
- Error logs: Console output (Command Prompt)
- Database: `db/kejaksaan.db`
- Uploaded files: `csv/`

### Common Issues & Solutions

| Issue | Quick Fix | Advanced Fix |
|-------|-----------|-------------|
| App won't start | Restart, run `setup.bat` | Check Python PATH |
| Slow performance | Close other apps | Increase system RAM |
| Database corrupted | `reset_database.bat` | Restore from backup |
| Import fails | Check file format | Validate CSV structure |

### Get Help
1. 📖 Check README.md
2. 🐛 Open GitHub Issue
3. 📧 Contact: [Repository Owner]

---

## 📝 Development Notes

### Script Architecture
```
Batch Scripts/
├── start_app.bat          # Main application launcher
├── setup.bat             # Initial environment setup
├── dev_start.bat         # Development mode
├── production_start.bat  # Production deployment
├── reset_database.bat    # Database utilities
└── quick_install.bat     # Quick setup alternative
```

### Maintenance
- Scripts auto-update dependencies
- Virtual environment isolation
- Error handling and user feedback
- Cross-Windows version compatibility

### Future Enhancements
- [ ] GUI launcher
- [ ] Auto-updater
- [ ] Service installer
- [ ] Docker container option

---

## 📄 License & Credits

**Aplikasi**: Kejaksaan Data Management System  
**Scripts**: Windows Deployment Automation  
**License**: [Check main README.md]  
**Contributors**: [Repository Contributors]

---

*Last Updated: Oktober 2025*  
*Script Version: 1.0*  
*Compatibility: Windows 7+ with Python 3.7+*