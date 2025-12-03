# 🔧 Troubleshooting - Laporan Pelacakan Perkara

Panduan untuk mengatasi masalah ketika fitur Laporan Pelacakan Perkara tidak muncul di PC lain.

---

## 🚨 Problem: URL `/laporan_pelacakan_perkara` Tidak Bisa Diakses

### Gejala:
- Di PC lokal bisa akses `http://localhost:5001/laporan_pelacakan_perkara`
- Di PC lain setelah `git pull` tidak bisa akses (404 Not Found)

---

## ✅ Solusi Lengkap

### Step 1: Cek Kelengkapan File

Jalankan script checker:

```bash
python scripts/check_laporan_pelacakan.py
```

**Output yang diharapkan:**
```
✓ Template exists: templates\laporan_pelacakan_perkara.html
✓ Route '/laporan_pelacakan_perkara' found in app_with_db.py
✓ Function 'get_pelacakan_perkara_report_data' found in mysql_database.py
✓ Column 'identitas_tersangka' exists in pidum_data table
✓ Column 'pasal' exists in pidum_data table
✓ Function executed successfully
```

---

### Step 2: Jika Ada File yang Kurang

#### ❌ Template NOT found
```bash
# Pull latest code
git pull origin main

# Cek apakah file ada
dir templates\laporan_pelacakan_perkara.html
```

#### ❌ Route NOT found in app_with_db.py
```bash
# Pull latest code
git pull origin main

# Cek versi file
git log --oneline src/app_with_db.py | head -5
```

#### ❌ Function NOT found in mysql_database.py
```bash
# Pull latest code
git pull origin main

# Cek versi file
git log --oneline src/models/mysql_database.py | head -5
```

---

### Step 3: Jika Kolom Database Kurang

#### ❌ Column 'identitas_tersangka' NOT found
#### ❌ Column 'pasal' NOT found

**Solusi:**
```bash
# Jalankan auto migration
python scripts/auto_migrate.py
```

**Atau manual:**
```sql
-- Connect to MySQL
mysql -u root -p

USE db_kejaksaan_app;

-- Add missing columns
ALTER TABLE pidum_data ADD COLUMN pasal TEXT AFTER tahapan_penanganan;
ALTER TABLE pidum_data ADD COLUMN identitas_tersangka TEXT AFTER pasal;

-- Verify
DESCRIBE pidum_data;
```

---

### Step 4: Restart Aplikasi

Setelah semua fix, restart aplikasi:

```bash
# Stop aplikasi (Ctrl+C)

# Start lagi
python src/app_with_db.py
```

---

## 🔍 Pengecekan Manual

### 1. Cek File Template
```bash
# Windows
dir templates\laporan_pelacakan_perkara.html

# Linux/Mac
ls -la templates/laporan_pelacakan_perkara.html
```

### 2. Cek Route di App
```bash
# Search route in app file
findstr /C:"laporan_pelacakan_perkara" src\app_with_db.py

# Atau buka file dan cari line 2635
```

### 3. Cek Function di Database Model
```bash
# Search function
findstr /C:"get_pelacakan_perkara_report_data" src\models\mysql_database.py
```

### 4. Cek Kolom Database
```sql
-- Connect to MySQL
mysql -u root -p

USE db_kejaksaan_app;

-- Check columns
DESCRIBE pidum_data;

-- Should show:
-- | identitas_tersangka | text | YES  |     | NULL    |       |
-- | pasal               | text | YES  |     | NULL    |       |
```

---

## 📋 Checklist Deployment ke PC Baru

Gunakan checklist ini untuk memastikan fitur berjalan:

- [ ] **Git Pull Latest Code**
  ```bash
  git pull origin main
  ```

- [ ] **Install Dependencies**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Check Schema**
  ```bash
  python scripts/check_schema_sync.py
  ```

- [ ] **Run Migration (jika perlu)**
  ```bash
  python scripts/auto_migrate.py
  ```

- [ ] **Check Laporan Pelacakan Feature**
  ```bash
  python scripts/check_laporan_pelacakan.py
  ```

- [ ] **Restart Application**
  ```bash
  python src/app_with_db.py
  ```

- [ ] **Test URL**
  - Buka browser: `http://localhost:5001/laporan_pelacakan_perkara`
  - Login dengan kredensial yang benar
  - Pastikan halaman muncul tanpa error

---

## 🐛 Common Errors

### Error 1: 404 Not Found
**Penyebab:** Route tidak terdaftar di app_with_db.py

**Solusi:**
```bash
git pull origin main
# Restart aplikasi
```

### Error 2: Template Not Found
**Penyebab:** File template tidak ada

**Solusi:**
```bash
git pull origin main
# Cek file: templates/laporan_pelacakan_perkara.html
```

### Error 3: Column doesn't exist
**Penyebab:** Database schema belum diupdate

**Solusi:**
```bash
python scripts/auto_migrate.py
```

### Error 4: Function not found
**Penyebab:** mysql_database.py versi lama

**Solusi:**
```bash
git pull origin main
# Restart aplikasi
```

### Error 5: No data shown
**Penyebab:** Tidak ada data dengan identitas_tersangka

**Solusi:**
- Ini normal jika data lama tidak punya identitas_tersangka
- Input data baru dengan identitas_tersangka
- Atau update data lama:
  ```sql
  UPDATE pidum_data 
  SET identitas_tersangka = 'Nama Tersangka' 
  WHERE id = 1;
  ```

---

## 🎯 Quick Fix Command

Jalankan semua command ini secara berurutan:

```bash
# 1. Pull latest code
git pull origin main

# 2. Install dependencies
pip install -r requirements.txt

# 3. Check and migrate schema
python scripts/check_schema_sync.py
python scripts/auto_migrate.py

# 4. Check laporan pelacakan feature
python scripts/check_laporan_pelacakan.py

# 5. Restart app
python src/app_with_db.py
```

---

## 📞 Masih Bermasalah?

Jika masih ada masalah setelah mengikuti panduan ini:

1. **Cek log error** di console saat aplikasi berjalan
2. **Cek versi Git** - pastikan sudah pull latest:
   ```bash
   git log --oneline -5
   ```
3. **Cek branch** - pastikan di branch yang benar:
   ```bash
   git branch
   ```
4. **Compare files** dengan PC yang berfungsi:
   ```bash
   # Cek hash file
   git hash-object src/app_with_db.py
   git hash-object templates/laporan_pelacakan_perkara.html
   ```

---

## 📚 File yang Diperlukan

Fitur Laporan Pelacakan Perkara memerlukan:

1. **Template:**
   - `templates/laporan_pelacakan_perkara.html`

2. **Route:**
   - `src/app_with_db.py` (line ~2635)
   - Function: `laporan_pelacakan_perkara()`
   - Function: `export_pelacakan_perkara_excel()`

3. **Database Function:**
   - `src/models/mysql_database.py`
   - Function: `get_pelacakan_perkara_report_data()`

4. **Database Schema:**
   - Table: `pidum_data`
   - Column: `identitas_tersangka` (TEXT)
   - Column: `pasal` (TEXT)

5. **Test Script:**
   - `test_laporan_pelacakan.py`
   - `scripts/check_laporan_pelacakan.py`

---

**Last Updated:** 2025-12-03  
**Version:** 1.3.0
