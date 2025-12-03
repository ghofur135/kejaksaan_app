# 🔄 Panduan Sinkronisasi Schema Database

Panduan ini menjelaskan cara mengecek dan menyinkronkan schema database MySQL dengan model di source code.

## 📋 Daftar Isi

1. [Pengecekan Schema](#pengecekan-schema)
2. [Auto Migration](#auto-migration)
3. [Troubleshooting](#troubleshooting)

---

## 🔍 Pengecekan Schema

### Script: `check_schema_sync.py`

Script ini akan mengecek apakah schema database MySQL Anda sudah sesuai dengan model di source code.

### Cara Menggunakan:

```bash
python scripts/check_schema_sync.py
```

### Output yang Ditampilkan:

1. **Tabel yang ada** vs **Tabel yang seharusnya ada**
2. **Kolom yang hilang** (perlu ditambahkan)
3. **Kolom yang berlebih** (tidak ada di model)
4. **Detail setiap kolom** (tipe data, nullable, key)
5. **SQL statement** untuk migrasi manual (jika diperlukan)

### Contoh Output:

```
================================================================================
                    Checking Table: pidum_data
================================================================================

Expected columns: 10
Actual columns:   8

✗ Missing columns (2):
  - pasal
  - identitas_tersangka

⚠ Migration SQL needed:
  ALTER TABLE pidum_data ADD COLUMN pasal TEXT;
  ALTER TABLE pidum_data ADD COLUMN identitas_tersangka TEXT AFTER pasal;

Column Details:
Column Name                         Type            Nullable   Key       
----------------------------------------------------------------------
id                                  int             NO         PRI       
no                                  varchar         NO                   
periode                             varchar         NO                   
tanggal                             date            NO                   
jenis_perkara                       varchar         NO                   
tahapan_penanganan                  varchar         NO                   
keterangan                          text            YES                  
created_at                          timestamp       YES                  
```

---

## 🚀 Auto Migration

### Script: `auto_migrate.py`

Script ini akan **otomatis menambahkan** kolom dan tabel yang hilang ke database Anda.

### Cara Menggunakan:

```bash
python scripts/auto_migrate.py
```

### Apa yang Dilakukan:

1. ✅ Menambahkan kolom `pasal` ke tabel `pidum_data`
2. ✅ Menambahkan kolom `identitas_tersangka` ke tabel `pidum_data`
3. ✅ Menambahkan kolom `pasal` ke tabel `pidsus_data`
4. ✅ Menambahkan kolom `nama_tersangka` ke tabel `pidsus_data`
5. ✅ Membuat tabel `upaya_hukum_data` (jika belum ada)

### Contoh Output:

```
================================================================================
                    AUTO MIGRATION - DATABASE SCHEMA
================================================================================

Connecting to database...
✓ Connected to: db_kejaksaan_app

Checking pidum_data.pasal...
  → Adding column 'pasal' to pidum_data...
  ✓ Column 'pasal' added successfully

Checking pidum_data.identitas_tersangka...
  → Adding column 'identitas_tersangka' to pidum_data...
  ✓ Column 'identitas_tersangka' added successfully

Checking pidsus_data.pasal...
  ✓ Column 'pasal' already exists

Checking pidsus_data.nama_tersangka...
  ✓ Column 'nama_tersangka' already exists

Checking upaya_hukum_data table...
  ✓ Table 'upaya_hukum_data' already exists

================================================================================
                           MIGRATION SUMMARY
================================================================================

✓ 2 migration(s) applied successfully:

  1. pidum_data.pasal
  2. pidum_data.identitas_tersangka

✓ Database schema is now up to date!

You can now run the application:
  python src/app_with_db.py
```

---

## 🔧 Workflow Deployment ke PC Baru

### Langkah 1: Clone Repository

```bash
git clone <repository-url>
cd kejaksaan_app
```

### Langkah 2: Setup Environment

```bash
# Copy file .env
cp .env.example .env

# Edit .env dengan konfigurasi database PC baru
# DB_HOST=localhost
# DB_NAME=db_kejaksaan_app
# DB_USER=root
# DB_PASSWORD=your_password
```

### Langkah 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Langkah 4: Cek Schema Database

```bash
python scripts/check_schema_sync.py
```

### Langkah 5: Jalankan Auto Migration

```bash
python scripts/auto_migrate.py
```

### Langkah 6: Verifikasi

```bash
# Cek lagi untuk memastikan semua sudah sync
python scripts/check_schema_sync.py
```

### Langkah 7: Jalankan Aplikasi

```bash
python src/app_with_db.py
```

---

## 🛠️ Troubleshooting

### Error: "Table doesn't exist"

**Solusi:**
```bash
# Buat schema database dari awal
python scripts/setup_schema_only.py

# Atau import schema SQL manual
mysql -u root -p db_kejaksaan_app < scripts/mysql_schema.sql
```

### Error: "Access denied for user"

**Solusi:**
1. Cek kredensial di file `.env`
2. Pastikan user MySQL memiliki privileges yang cukup:
   ```sql
   GRANT ALL PRIVILEGES ON db_kejaksaan_app.* TO 'kejaksaan'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Error: "Can't connect to MySQL server"

**Solusi:**
1. Pastikan MySQL server sudah running:
   ```bash
   # Windows
   net start MySQL80
   
   # Linux
   sudo systemctl start mysql
   ```
2. Cek host dan port di `.env`

### Migration Gagal di Tengah Jalan

**Solusi:**
```bash
# Jalankan lagi, script akan skip kolom yang sudah ada
python scripts/auto_migrate.py
```

### Ingin Rollback Migration

**Solusi:**
```sql
-- Hapus kolom yang baru ditambahkan
ALTER TABLE pidum_data DROP COLUMN pasal;
ALTER TABLE pidum_data DROP COLUMN identitas_tersangka;
ALTER TABLE pidsus_data DROP COLUMN pasal;
ALTER TABLE pidsus_data DROP COLUMN nama_tersangka;

-- Hapus tabel upaya_hukum_data
DROP TABLE upaya_hukum_data;
```

---

## 📊 Perbandingan Schema

### Tabel `pidum_data`

| Kolom                  | Tipe      | Keterangan                    | Status  |
|------------------------|-----------|-------------------------------|---------|
| id                     | INT       | Primary key                   | Lama    |
| no                     | VARCHAR   | Nomor urut                    | Lama    |
| periode                | VARCHAR   | Periode data                  | Lama    |
| tanggal                | DATE      | Tanggal perkara               | Lama    |
| jenis_perkara          | VARCHAR   | Jenis perkara                 | Lama    |
| tahapan_penanganan     | VARCHAR   | Tahapan (Pra/Penuntutan/UH)   | Lama    |
| **pasal**              | TEXT      | **Pasal yang dilanggar**      | **BARU** |
| **identitas_tersangka**| TEXT      | **Nama tersangka**            | **BARU** |
| keterangan             | TEXT      | Keterangan tambahan           | Lama    |
| created_at             | TIMESTAMP | Waktu dibuat                  | Lama    |

### Tabel `pidsus_data`

| Kolom                  | Tipe      | Keterangan                    | Status  |
|------------------------|-----------|-------------------------------|---------|
| id                     | INT       | Primary key                   | Lama    |
| no                     | VARCHAR   | Nomor urut                    | Lama    |
| periode                | VARCHAR   | Periode data                  | Lama    |
| tanggal                | DATE      | Tanggal perkara               | Lama    |
| jenis_perkara          | VARCHAR   | Jenis perkara                 | Lama    |
| **pasal**              | TEXT      | **Pasal yang dilanggar**      | **BARU** |
| **nama_tersangka**     | TEXT      | **Nama tersangka**            | **BARU** |
| penyidikan             | VARCHAR   | Status penyidikan (0/1)       | Lama    |
| penuntutan             | VARCHAR   | Status penuntutan (0/1)       | Lama    |
| keterangan             | TEXT      | Keterangan tambahan           | Lama    |
| created_at             | TIMESTAMP | Waktu dibuat                  | Lama    |

### Tabel `upaya_hukum_data` (BARU)

Tabel baru dengan 31 kolom untuk menyimpan data upaya hukum:
- 6 kolom Perlawanan
- 5 kolom Banding
- 5 kolom Kasasi
- 3 kolom Kasasi Demi Hukum
- 3 kolom PK
- 5 kolom Grasi
- 4 kolom metadata

---

## 💡 Tips

1. **Selalu backup database** sebelum menjalankan migration:
   ```bash
   mysqldump -u root -p db_kejaksaan_app > backup_$(date +%Y%m%d).sql
   ```

2. **Jalankan check_schema_sync.py** setelah pull code baru dari git

3. **Gunakan auto_migrate.py** untuk deployment otomatis

4. **Simpan output migration** untuk dokumentasi

5. **Test di development** sebelum deploy ke production

---

## 📞 Support

Jika mengalami masalah:
1. Cek error message dengan teliti
2. Lihat section Troubleshooting di atas
3. Cek log aplikasi di `logs/`
4. Hubungi tim development

---

**Last Updated:** 2025-12-03
**Version:** 1.3.0
