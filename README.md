# Aplikasi Kejaksaan

Aplikasi manajemen data kejaksaan untuk PIDUM (Pidana Umum) dan PIDSUS (Pidana Khusus).

## 🆕 Update Terbaru - Import Upaya Hukum Extended

Fitur baru untuk import data Register Upaya Hukum dengan format extended yang mendukung semua jenis upaya hukum:

### Fitur Baru
- **Tabel Baru `upaya_hukum_data`** - Tabel khusus dengan 31 kolom untuk menyimpan data upaya hukum secara detail
- **Import CSV Extended** - Mendukung format CSV dengan kolom Perlawanan, Banding, Kasasi, PK, dan Grasi
- **Halaman View Upaya Hukum** - `/view_upaya_hukum` untuk melihat dan mengelola data upaya hukum
- **Laporan Terintegrasi** - Data upaya hukum dari tabel baru otomatis terhitung di laporan PIDUM

### Cara Menggunakan
1. Buka `/import_upaya_hukum_api`
2. Upload file CSV Register Upaya Hukum
3. Preview dan konfirmasi import
4. Lihat data di `/view_upaya_hukum`
5. Laporan di `/view_pidum` akan menampilkan total gabungan

### Format CSV yang Didukung
Kolom wajib: `No`, `Terdakwa_Terpidana`, `No_Tanggal_RP9`

Kolom opsional:
- Banding: `Banding_No_Tgl_Akte_Permohonan`, `Banding_No_Tgl_Amar_Putusan_PT`, dll.
- Kasasi: `Kasasi_No_Tgl_Akte_Permohonan`, `Kasasi_No_Tanggal_Amar_Putusan_MA`, dll.
- PK: `PK_Tgl_Diajukan_Terpidana`, `PK_No_Tgl_Amar_Putusan`, dll.
- Grasi: `Grasi_Tgl_Penerimaan_Berkas`, `Grasi_No_Tgl_KEPRES_Amar`, dll.

---

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
│   ├── config.py                # Konfigurasi database
│   ├── controllers/             # Controller aplikasi
│   ├── models/                  # Model database
│   │   └── mysql_database.py    # Koneksi dan model MySQL
│   ├── helpers/                 # Helper functions
│   │   ├── import_helper.py
│   │   ├── import_pra_penuntutan_helper.py
│   │   └── import_upaya_hukum_helper.py  # Import upaya hukum extended
│   └── utils/                   # Utility functions
│       └── CSV Tool/            # Tools untuk CSV
├── config/                      # File konfigurasi
├── scripts/                     # Script utility
├── data/                        # Data aplikasi
│   └── csv/                     # File CSV untuk import
├── docs/                        # Dokumentasi
├── static/                      # File statis (CSS, JS, images)
├── templates/                   # Template HTML
│   ├── view_pidum.html          # Lihat data PIDUM
│   ├── view_upaya_hukum.html    # Lihat data Upaya Hukum (NEW)
│   ├── import_upaya_hukum.html  # Form import upaya hukum
│   └── import_upaya_hukum_preview.html  # Preview import
├── logs/                        # Log files
├── tests/                       # Unit tests
├── requirements.txt             # Dependencies Python
├── CHANGELOG.md                 # Catatan perubahan
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