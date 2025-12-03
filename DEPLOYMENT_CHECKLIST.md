# ✅ Deployment Checklist - PC Baru

Checklist cepat untuk deploy aplikasi Kejaksaan ke PC baru.

## 📋 Quick Start (5 Menit)

### 1️⃣ Clone & Setup (1 menit)
```bash
git clone <repository-url>
cd kejaksaan_app
pip install -r requirements.txt
```

### 2️⃣ Konfigurasi Database (1 menit)
```bash
# Copy dan edit .env
cp .env.example .env
# Edit DB_HOST, DB_USER, DB_PASSWORD sesuai PC baru
```

### 3️⃣ Cek Schema Database (1 menit)
```bash
python scripts/check_schema_sync.py
```

**Output yang diharapkan:**
- ✅ Semua tabel synchronized → Lanjut ke step 5
- ❌ Ada missing columns → Lanjut ke step 4

### 4️⃣ Auto Migration (1 menit)
```bash
python scripts/auto_migrate.py
```

**Output yang diharapkan:**
- ✅ Migration applied successfully
- ✅ Database schema is now up to date

### 5️⃣ Jalankan Aplikasi (1 menit)
```bash
python src/app_with_db.py
```

**Akses:** http://localhost:5000

---

## 🔍 Pengecekan Detail

### Cek Koneksi Database
```bash
python scripts/test_mysql_connection.py
```

### Cek Struktur Tabel
```bash
python scripts/check_schema_sync.py
```

### Lihat Data di Database
```bash
mysql -u root -p
USE db_kejaksaan_app;
SHOW TABLES;
DESCRIBE pidum_data;
DESCRIBE pidsus_data;
DESCRIBE upaya_hukum_data;
```

---

## 📊 Perubahan Schema Terbaru

### Tabel `pidum_data` - Tambahan 2 Kolom:
- ✅ `pasal` (TEXT) - Pasal yang dilanggar
- ✅ `identitas_tersangka` (TEXT) - Nama tersangka

### Tabel `pidsus_data` - Tambahan 2 Kolom:
- ✅ `pasal` (TEXT) - Pasal yang dilanggar
- ✅ `nama_tersangka` (TEXT) - Nama tersangka

### Tabel `upaya_hukum_data` - Tabel Baru:
- ✅ 31 kolom untuk data upaya hukum lengkap
- ✅ Support Perlawanan, Banding, Kasasi, PK, Grasi

---

## 🚨 Troubleshooting Cepat

### ❌ Error: "Can't connect to MySQL"
```bash
# Cek MySQL running
net start MySQL80  # Windows
sudo systemctl start mysql  # Linux

# Cek kredensial di .env
```

### ❌ Error: "Table doesn't exist"
```bash
# Setup schema dari awal
python scripts/setup_schema_only.py
```

### ❌ Error: "Column doesn't exist"
```bash
# Jalankan auto migration
python scripts/auto_migrate.py
```

### ❌ Error: "Access denied"
```bash
# Cek user privileges
mysql -u root -p
GRANT ALL PRIVILEGES ON db_kejaksaan_app.* TO 'kejaksaan'@'localhost';
FLUSH PRIVILEGES;
```

---

## 📝 Catatan Penting

### ⚠️ Sebelum Migration
1. **Backup database** terlebih dahulu:
   ```bash
   mysqldump -u root -p db_kejaksaan_app > backup.sql
   ```

2. **Cek versi MySQL** (minimal 5.7):
   ```bash
   mysql --version
   ```

### ✅ Setelah Migration
1. **Test fitur utama:**
   - Login ke aplikasi
   - Input data PIDUM
   - Input data PIDSUS
   - Import CSV
   - Generate laporan

2. **Cek log error:**
   - Lihat console output
   - Cek file log di folder `logs/`

---

## 🔄 Update dari Git

Jika ada update code dari repository:

```bash
# 1. Pull latest code
git pull origin main

# 2. Update dependencies
pip install -r requirements.txt

# 3. Cek schema
python scripts/check_schema_sync.py

# 4. Auto migrate jika perlu
python scripts/auto_migrate.py

# 5. Restart aplikasi
python src/app_with_db.py
```

---

## 📞 Bantuan

Jika masih ada masalah:

1. **Baca dokumentasi lengkap:**
   - `docs/SCHEMA_SYNC_GUIDE.md` - Panduan sinkronisasi schema
   - `docs/MYSQL_MIGRATION_GUIDE.md` - Panduan migrasi MySQL
   - `docs/DEPLOYMENT_GUIDE.md` - Panduan deployment

2. **Cek CHANGELOG.md** untuk perubahan terbaru

3. **Hubungi tim development**

---

## ✨ Tips Pro

1. **Gunakan virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux
   ```

2. **Simpan backup rutin:**
   ```bash
   # Buat script backup otomatis
   mysqldump -u root -p db_kejaksaan_app > backup_$(date +%Y%m%d).sql
   ```

3. **Monitor log aplikasi:**
   ```bash
   tail -f logs/app.log  # Linux
   Get-Content logs/app.log -Wait  # Windows PowerShell
   ```

4. **Test di development dulu** sebelum deploy ke production

---

**Last Updated:** 2025-12-03  
**Version:** 1.3.0
