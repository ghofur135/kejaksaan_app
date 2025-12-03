# 🚀 Quick Reference - Sinkronisasi Database

Referensi cepat untuk mengecek dan menyinkronkan schema database.

---

## 📌 Command Penting

### Cek Schema Database
```bash
python scripts/check_schema_sync.py
```
**Fungsi:** Mengecek apakah schema database sudah sesuai dengan model di source code

**Output:**
- ✅ Tabel yang synchronized
- ❌ Kolom yang hilang
- ⚠️ Kolom yang berlebih
- 📋 SQL statement untuk migrasi manual

---

### Auto Migration
```bash
python scripts/auto_migrate.py
```
**Fungsi:** Otomatis menambahkan kolom dan tabel yang hilang

**Yang dilakukan:**
- Tambah kolom `pasal` ke `pidum_data`
- Tambah kolom `identitas_tersangka` ke `pidum_data`
- Tambah kolom `pasal` ke `pidsus_data`
- Tambah kolom `nama_tersangka` ke `pidsus_data`
- Buat tabel `upaya_hukum_data` (jika belum ada)

---

### Test Koneksi Database
```bash
python scripts/test_mysql_connection.py
```
**Fungsi:** Test koneksi ke MySQL dan tampilkan info database

---

### Setup Schema dari Awal
```bash
python scripts/setup_schema_only.py
```
**Fungsi:** Buat semua tabel dari awal (untuk database baru)

---

## 📊 Perubahan Schema v1.3.0

### pidum_data
```sql
ALTER TABLE pidum_data ADD COLUMN pasal TEXT AFTER tahapan_penanganan;
ALTER TABLE pidum_data ADD COLUMN identitas_tersangka TEXT AFTER pasal;
```

### pidsus_data
```sql
ALTER TABLE pidsus_data ADD COLUMN pasal TEXT AFTER jenis_perkara;
ALTER TABLE pidsus_data ADD COLUMN nama_tersangka TEXT AFTER pasal;
```

### upaya_hukum_data (Tabel Baru)
```sql
CREATE TABLE upaya_hukum_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    no TEXT,
    terdakwa_terpidana TEXT,
    no_tanggal_rp9 TEXT,
    jenis_perkara TEXT,
    -- 31 kolom untuk Perlawanan, Banding, Kasasi, PK, Grasi
    -- ...
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔄 Workflow Deployment

```
1. Clone repo
   ↓
2. Setup .env
   ↓
3. pip install -r requirements.txt
   ↓
4. python scripts/check_schema_sync.py
   ↓
5. python scripts/auto_migrate.py (jika perlu)
   ↓
6. python src/app_with_db.py
```

---

## 🛠️ Troubleshooting

| Error | Solusi |
|-------|--------|
| Can't connect to MySQL | `net start MySQL80` atau cek `.env` |
| Table doesn't exist | `python scripts/setup_schema_only.py` |
| Column doesn't exist | `python scripts/auto_migrate.py` |
| Access denied | Cek user privileges di MySQL |

---

## 📚 Dokumentasi Lengkap

- **SCHEMA_SYNC_GUIDE.md** - Panduan lengkap sinkronisasi schema
- **DEPLOYMENT_CHECKLIST.md** - Checklist deployment ke PC baru
- **MYSQL_MIGRATION_GUIDE.md** - Panduan migrasi MySQL
- **CHANGELOG.md** - Catatan perubahan versi

---

## 💡 Tips

1. **Selalu backup** sebelum migration:
   ```bash
   mysqldump -u root -p db_kejaksaan_app > backup.sql
   ```

2. **Cek schema** setelah pull code baru:
   ```bash
   git pull && python scripts/check_schema_sync.py
   ```

3. **Test di development** sebelum production

4. **Simpan output migration** untuk dokumentasi

---

**Version:** 1.3.0  
**Last Updated:** 2025-12-03
