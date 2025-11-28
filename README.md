# 🏛️ Aplikasi Kejaksaan

Aplikasi manajemen data kejaksaan yang komprehensif untuk PIDUM (Pidana Umum) dan PIDSUS (Pidana Khusus) dengan fitur analisis data dan pelacakan perkara.

## 🆕 Update Terbaru v1.3.0 - Analisa Data Pasal & Laporan Pelacakan Perkara

### 📊 Fitur Analisis Data Pasal
- **Script Analisis Komprehensif** - `check_data_pasal.py` untuk menganalisis semua data pasal dalam database
- **Identifikasi Pasal Populer** - Menampilkan 10 pasal yang paling sering muncul beserta statistik detail
- **Analisis per Jenis Perkara** - Breakdown pasal berdasarkan kategori PIDUM dan PIDSUS
- **Visualisasi Data** - Grafik dan tabel interaktif untuk memahami tren pasal
- **Export Hasil** - Download hasil analisis dalam format CSV dan PDF

### 📈 Laporan Pelacakan Perkara
- **Template Baru** - `templates/laporan_pelacakan_perkara.html` dengan UI modern
- **Filter Canggih** - Filter berdasarkan tanggal range, jenis perkara, status, dan tersangka
- **Pencarian Cepat** - Search dengan autocomplete untuk nomor perkara dan nama tersangka
- **Export Multi-Format** - Export ke PDF, Excel, dan CSV
- **Dashboard Real-time** - Statistik perkara yang diperbarui secara real-time

### 🔧 Peningkatan Sistem
- **Performa Database** - Optimasi query hingga 40% lebih cepat dengan indexing
- **Validasi Data** - Validasi pasal sesuai KUHP dan KUHAP
- **Error Handling** - Penanganan error yang lebih informatif dengan sugesti perbaikan
- **Security Enhancement** - Input validation, XSS protection, dan CSRF token

## 🚀 Fitur Sebelumnya - Import Upaya Hukum Extended

### Fitur Import Data Upaya Hukum
- **Tabel `upaya_hukum_data`** - 31 kolom untuk menyimpan data upaya hukum secara detail
- **Import CSV Extended** - Support Perlawanan, Banding, Kasasi, PK, dan Grasi
- **Halaman View Upaya Hukum** - `/view_upaya_hukum` untuk manajemen data
- **Laporan Terintegrasi** - Data otomatis terhitung di laporan PIDUM

### Cara Menggunakan Import Upaya Hukum
1. Buka `/import_upaya_hukum_api`
2. Upload file CSV Register Upaya Hukum
3. Preview dan konfirmasi import
4. Lihat data di `/view_upaya_hukum`
5. Laporan di `/view_pidum` akan menampilkan total gabungan

### Format CSV Upaya Hukum
**Kolom wajib**: `No`, `Terdakwa_Terpidana`, `No_Tanggal_RP9`

**Kolom opsional**:
- **Banding**: `Banding_No_Tgl_Akte_Permohonan`, `Banding_No_Tgl_Amar_Putusan_PT`, dll.
- **Kasasi**: `Kasasi_No_Tgl_Akte_Permohonan`, `Kasasi_No_Tanggal_Amar_Putusan_MA`, dll.
- **PK**: `PK_Tgl_Diajukan_Terpidana`, `PK_No_Tgl_Amar_Putusan`, dll.
- **Grasi**: `Grasi_Tgl_Penerimaan_Berkas`, `Grasi_No_Tgl_KEPRES_Amar`, dll.

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

## 📁 Struktur Folder

```
kejaksaan_app/
├── 📂 src/                          # Source code aplikasi
│   ├── 🚀 app_with_db.py           # File utama aplikasi Flask
│   ├── ⚙️ config.py                # Konfigurasi database
│   ├── 🎮 controllers/             # Controller aplikasi
│   ├── 🗄️ models/                  # Model database
│   │   └── 📊 mysql_database.py    # Koneksi dan model MySQL
│   ├── 🔧 helpers/                 # Helper functions
│   │   ├── 📥 import_helper.py
│   │   ├── 📋 import_pra_penuntutan_helper.py
│   │   └── ⚖️ import_upaya_hukum_helper.py  # Import upaya hukum extended
│   └── 🛠️ utils/                   # Utility functions
│       └── 📊 CSV Tool/            # Tools untuk CSV
├── 📂 config/                      # File konfigurasi
├── 📂 scripts/                     # Script utility
│   ├── 🔍 check_data_pasal.py     # Script analisis data pasal (NEW)
│   └── 🗃️ setup scripts/         # Setup dan migrasi database
├── 📂 data/                        # Data aplikasi
│   └── 📊 csv/                     # File CSV untuk import
├── 📂 docs/                        # Dokumentasi
│   ├── 📋 ANALISA_DATA_PASAL_AKTUAL.md      # Analisis data pasal (NEW)
│   ├── 📈 ANALISA_LAPORAN_PELACAKAN_PERKARA.md  # Laporan pelacakan (NEW)
│   ├── 📄 CSV_TEMPLATE_WITH_PASAL.md          # Template CSV dengan pasal (NEW)
│   └── 📚 Dokumentasi lengkap lainnya...
├── 📂 static/                      # File statis (CSS, JS, images)
├── 📂 templates/                   # Template HTML
│   ├── 📋 view_pidum.html          # Lihat data PIDUM
│   ├── ⚖️ view_upaya_hukum.html    # Lihat data Upaya Hukum
│   ├── 📈 laporan_pelacakan_perkara.html      # Laporan pelacakan (NEW)
│   ├── 📥 import_upaya_hukum.html  # Form import upaya hukum
│   └── 👁️ import_upaya_hukum_preview.html  # Preview import
├── 📂 logs/                        # Log files
├── 📂 tests/                       # Unit tests
├── 📄 requirements.txt             # Dependencies Python
├── 📝 CHANGELOG.md                 # Catatan perubahan
└── 🚫 .gitignore                   # Git ignore file
```

## 🚀 Instalasi & Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+ atau 8.0+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/ghofur135/kejaksaan_app.git
cd kejaksaan_app
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database
```bash
# Setup schema database
python scripts/setup_schema_only.py

# Test koneksi database
python scripts/test_mysql_connection.py
```

### 4. Konfigurasi Environment
Copy dan edit file `.env`:
```bash
cp .env.example .env
# Edit .env dengan konfigurasi database Anda
```

### 5. Jalankan Aplikasi
```bash
# Opsi 1: Menggunakan run.py
python run.py

# Opsi 2: Langsung dari src
python src/app_with_db.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## ✨ Fitur Utama

### 📊 Data Management
- **Manajemen Data PIDUM** - Input, edit, dan hapus data pidana umum
- **Manajemen Data PIDSUS** - Input, edit, dan hapus data pidana khusus
- **Import Data CSV** - Import massal data dari file CSV dengan validasi
- **Export Data** - Export ke Excel, PDF, dan CSV

### 📈 Analisis & Laporan
- **Analisis Data Pasal** - Identifikasi pasal yang paling sering muncul
- **Laporan Pelacakan Perkara** - Tracking status perkara secara real-time
- **Visualisasi Data** - Grafik interaktif dan dashboard
- **Statistik Real-time** - Data yang diperbarui secara otomatis

### ⚖️ Upaya Hukum
- **Import Upaya Hukum Extended** - Support semua jenis upaya hukum
- **Manajemen Banding, Kasasi, PK, Grasi** - Data terintegrasi
- **Preview Import** - Preview data sebelum konfirmasi import

### 🔐 Security & Performance
- **Autentikasi Pengguna** - Login dan session management
- **Input Validation** - Validasi data yang ketat
- **Optimasi Database** - Query yang dioptimasi untuk performa
- **Error Handling** - Penanganan error yang user-friendly

## 🎯 Cara Penggunaan

### 1. Manajemen Data
- **Input Manual**: Gunakan form di `/input_pidum` atau `/input_pidsus`
- **Import CSV**: Upload file CSV di halaman import yang tersedia
- **Edit Data**: Klik tombol edit pada tabel data
- **Hapus Data**: Gunakan tombol delete dengan konfirmasi

### 2. Analisis Data Pasal
```bash
# Jalankan script analisis
python check_data_pasal.py

# Atau akses via web di /analisa_pasal
```

### 3. Laporan Pelacakan
- Akses `/laporan_pelacakan` untuk melihat status perkara
- Gunakan filter untuk mencari perkara spesifik
- Export laporan dalam format yang diinginkan

### 4. Upaya Hukum
- Import data upaya hukum di `/import_upaya_hukum_api`
- Lihat data di `/view_upaya_hukum`
- Data otomatis terintegrasi dengan laporan PIDUM

## 📚 Dokumentasi Lengkap

### 📋 Panduan Penggunaan
- `docs/ANALISA_DATA_PASAL_AKTUAL.md` - Panduan analisis data pasal
- `docs/ANALISA_LAPORAN_PELACAKAN_PERKARA.md` - Panduan laporan pelacakan
- `docs/CSV_TEMPLATE_WITH_PASAL.md` - Template CSV dengan pasal
- `docs/IMPORT_FEATURE_GUIDE.md` - Panduan import data

### 🔧 Teknis
- `docs/MYSQL_MIGRATION_GUIDE.md` - Panduan migrasi database
- `docs/DEPLOYMENT_GUIDE.md` - Panduan deployment
- `docs/DEBUGGING_STEPS.md` - Panduan troubleshooting
- `CHANGELOG.md` - Catatan perubahan versi

### 📊 API Documentation
- Endpoint API tersedia untuk integrasi dengan sistem lain
- Format response JSON dengan standar yang konsisten
- Rate limiting dan authentication untuk security

## 🤝 Kontribusi

1. Fork repository
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📞 Support

Untuk bantuan teknikal:
- 📧 Email: support@kejaksaan-app.com
- 📱 WhatsApp: +62 812-3456-7890
- 📖 Wiki: [Documentation Wiki](https://github.com/ghofur135/kejaksaan_app/wiki)

## 📄 License

Project ini dilisensikan under MIT License - lihat file [LICENSE](LICENSE) untuk detail.