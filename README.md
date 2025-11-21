# Aplikasi Kejaksaan

Aplikasi manajemen data kejaksaan untuk PIDUM (Pidana Umum) dan PIDSUS (Pidana Khusus).

## 🔄 Update MySQL Migration

Aplikasi telah berhasil dimigrasi dari SQLite ke MySQL! Berikut adalah perubahan utama:

### 📋 Perubahan Database
- **Dari**: SQLite (file-based)
- **Ke**: MySQL (network-based dengan AWS RDS)

### 🗂️ File yang Ditambahkan/Dimodifikasi
- `.env` - Konfigurasi koneksi database MySQL
- `src/config.py` - Manajemen konfigurasi database
- `src/models/mysql_database.py` - Implementasi koneksi MySQL
- `scripts/mysql_schema.sql` - Schema database kompatibel MySQL
- `scripts/migrate_sqlite_to_mysql.py` - Script migrasi data
- `scripts/setup_mysql_database.py` - Setup dan testing database
- `scripts/test_mysql_connection.py` - Testing koneksi database

### 📄 Dokumentasi
- `docs/MYSQL_MIGRATION_GUIDE.md` - Panduan lengkap migrasi

### 🔄 Update Dependencies
- `requirements.txt` - Ditambahkan `mysql-connector-python` dan `python-dotenv`

### ⚙️ Konfigurasi
Database MySQL kini dikonfigurasi melalui environment variables:
- Host: AWS RDS
- Database: `db_kejaksaan_app`
- User: `kejaksaan`
- Port: `3306`

### 🚀 Cara Menjalankan
1. **Setup Database**:
   ```bash
   python scripts/setup_schema_only.py
   ```

2. **Testing Koneksi**:
   ```bash
   python scripts/test_mysql_connection.py
   ```

3. **Menjalankan Aplikasi**:
   ```bash
   python src/app_with_db.py
   ```

### 📊 Fitur yang Telah Diuji
- ✅ Koneksi database
- ✅ Operasi CRUD (Create, Read, Update, Delete)
- ✅ Input data manual
- ✅ Import data dari CSV
- ✅ Generate laporan
- ✅ Export data ke Excel
- ✅ Visualisasi data dengan chart

### 🔄 Rollback
Jika diperlukan kembali ke SQLite:
1. Backup database MySQL
2. Ubah import di `src/app_with_db.py` ke `models.database`
3. Install dependencies SQLite
4. Jalankan aplikasi dengan database SQLite

## Struktur Folder

```
kejaksaan_app/
├── src/                          # Source code aplikasi
│   ├── app_with_db.py           # File utama aplikasi Flask
│   ├── controllers/             # Controller aplikasi
│   ├── models/                  # Model database
│   │   └── database.py          # Koneksi dan model database
│   ├── helpers/                 # Helper functions
│   │   ├── import_helper.py
│   │   ├── import_pra_penuntutan_helper.py
│   │   └── import_upaya_hukum_helper.py
│   └── utils/                   # Utility functions
│       └── CSV Tool/            # Tools untuk CSV
├── config/                      # File konfigurasi
│   ├── ecosystem-direct.config.json
│   ├── ecosystem.config.json
│   └── kejaksaan.code-workspace
├── scripts/                     # Script utility
│   ├── generate_dummy_pidum.py
│   ├── generate_realistic_pidum_dummy.py
│   ├── insert_sample_data.py
│   ├── migrate_database.py
│   ├── pm2-manager.sh
│   ├── reset_pidum.sh
│   ├── reset_pidum_data.py
│   ├── run_app.sh
│   ├── run_production.sh
│   └── simple_reset_pidum.py
├── data/                        # Data aplikasi
│   └── csv/                     # File CSV untuk import
├── docs/                        # Dokumentasi
├── static/                      # File statis (CSS, JS, images)
├── templates/                   # Template HTML
├── logs/                        # Log files
├── tests/                       # Unit tests
├── requirements.txt             # Dependencies Python
└── .gitignore                   # Git ignore file
```

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Jalankan aplikasi:
```bash
python run.py
```

Atau jalankan langsung dari folder src:
```bash
python src/app_with_db.py
```

## Fitur

- Manajemen data PIDUM
- Manajemen data PIDSUS
- Import data dari CSV
- Generate laporan
- Visualisasi data dengan chart

## Dokumentasi

Lihat folder `docs/` untuk dokumentasi lengkap.