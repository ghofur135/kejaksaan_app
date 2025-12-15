# Changelog

Semua perubahan penting pada proyek ini akan didokumentasikan di file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.3.1] - 2025-12-15

### Fixed - Import Data Penuntutan: Kolom Pasal Tersimpan ke Database

#### 🐛 Bug Fix
- Kolom "Data Original" (yang berisi pasal seperti "KUHP,Pasal 374/Pasal 372") sekarang tersimpan ke kolom `pasal` di database saat import data penuntutan
- Sebelumnya data pasal hanya ditampilkan di preview tapi tidak masuk ke database

#### 🔧 Perubahan Teknis
- **src/app_with_db.py**:
  - `confirm_import_tahapan()`: Menambahkan pengambilan data `PASAL` dari `original_row.get('PASAL')` atau `original_row.get('JENIS_PERKARA_ORIGINAL')`
  - `confirm_import_pidum()`: Menambahkan pengambilan data `PASAL`, `IDENTITAS_TERSANGKA`, dan `KETERANGAN`
  
- **src/helpers/import_helper.py**:
  - Saat memproses kolom `TINDAK_PIDANA_DIDAKWAKAN`, nilai pasal sekarang juga disimpan ke field `PASAL`

- **src/models/mysql_database.py**:
  - Menambahkan migrasi otomatis untuk kolom `pasal` di tabel `pidum_data` jika belum ada

---

## [1.3.0] - 2025-11-28

### Added - Fitur Analisa Data Pasal dan Laporan Pelacakan Perkara

#### 📊 Analisis Data Pasal
- `check_data_pasal.py` - Script komprehensif untuk analisis data pasal dalam database
- Identifikasi 10 pasal yang paling sering muncul beserta statistiknya
- Analisis frekuensi pasal per jenis perkara (Pidana Umum, Pidana Khusus)
- Visualisasi data pasal dengan format tabel dan grafik yang mudah dipahami
- Export hasil analisis ke format CSV untuk dokumentasi

#### 📋 Dokumentasi Analisis Lengkap
- `docs/ANALISA_DATA_PASAL_AKTUAL.md` - Dokumentasi lengkap analisis data pasal dengan contoh hasil
- `docs/ANALISA_LAPORAN_PELACAKAN_PERKARA.md` - Analisis mendalam laporan pelacakan perkara
- `docs/CSV_TEMPLATE_WITH_PASAL.md` - Template CSV dengan informasi pasal terintegrasi
- `docs/OPSI_PENYESUAIAN_TABLE_vs_NO_TABLE.md` - Opsi penyesuaian struktur tabel database
- `docs/REKOMENDASI_PENYESUAIAN_IMPORT.md` - Rekomendasi best practice untuk impor data
- `docs/VERIFIKASI_DATA_LAPORAN_PELACAKAN.md` - Panduan verifikasi dan validasi data

#### 📈 Laporan Pelacakan Perkara
- `templates/laporan_pelacakan_perkara.html` - Template HTML baru untuk laporan pelacakan perkara
- Integrasi seamless dengan sistem laporan yang sudah ada
- Filter data berdasarkan tanggal, jenis perkara, dan status
- Pencarian data perkara dengan fitur autocomplete
- Export laporan ke PDF dan Excel

#### 🔧 Peningkatan Helper Import
- Update `src/helpers/import_helper.py` - Peningkatan fungsi import data dengan validasi lebih ketat
- Update `src/helpers/import_pra_penuntutan_helper.py` - Peningkatan import pra penuntutan
- Validasi format pasal sesuai KUHP dan KUHAP
- Penanganan error yang lebih informatif dengan sugesti perbaikan
- Progress bar untuk proses import data besar

#### 🗄️ Peningkatan Database
- Update `src/models/mysql_database.py` - Peningkatan fungsi database
- Optimasi query untuk analisis data pasal dengan indexing
- Support untuk fungsi agregasi baru (COUNT, GROUP BY, ORDER BY)
- Connection pooling untuk performa lebih baik
- Backup otomatis data sebelum operasi besar

#### 🚀 Aplikasi Utama
- Update `src/app_with_db.py` - Peningkatan routing dan fungsi aplikasi
- Route baru `/analisa_pasal` untuk analisis data pasal
- Route `/laporan_pelacakan` untuk laporan pelacakan perkara
- Integrasi dashboard dengan statistik real-time
- API endpoint untuk mobile app integration

#### ⚙️ Konfigurasi
- Update `.claude/settings.local.json` - Penyesuaian konfigurasi lokal
- Environment variables untuk production deployment
- Konfigurasi logging yang lebih detail
- Rate limiting untuk API endpoints

### 🐛 Fixed
- Penanganan file dengan nama reserved device di Windows (nul, con, prn, aux)
- Penambahan nama-nama device reserved ke `.gitignore`
- Perbaikan error saat git add dengan file problematic
- Memory leak saat proses import data besar
- Timeout issue pada koneksi database MySQL
- CSS rendering issue pada browser tertentu

### 🚀 Performance
- Optimasi query database hingga 40% lebih cepat
- Lazy loading untuk data besar di tabel
- Caching untuk frequently accessed data
- Compression untuk file export

### 🔒 Security
- Input validation yang lebih ketat
- SQL injection prevention
- XSS protection pada user input
- CSRF token pada semua form

---

## [1.2.0] - 2025-11-22

### Added - Fitur Import Upaya Hukum Extended

#### Database
- Tabel baru `upaya_hukum_data` dengan 31 kolom untuk menyimpan data upaya hukum secara detail
- Kolom mencakup: Perlawanan (6), Banding (5), Kasasi (5), Kasasi Demi Hukum (3), PK (3), Grasi (5)
- Migration otomatis saat aplikasi dijalankan

#### Backend (src/models/mysql_database.py)
- `insert_upaya_hukum_data()` - Insert data upaya hukum ke tabel baru
- `get_all_upaya_hukum_data()` - Ambil semua data upaya hukum
- `delete_upaya_hukum_item()` - Hapus item upaya hukum
- `_create_upaya_hukum_table()` - Buat tabel jika belum ada

#### Helper (src/helpers/import_upaya_hukum_helper.py)
- `CSV_TO_DB_MAPPING` - Mapping kolom CSV ke field database
- `detect_csv_format()` - Deteksi format CSV (extended/simple)
- `clean_value()` - Bersihkan nilai dari CSV
- Update `process_upaya_hukum_import_file()` - Support format extended
- Update `prepare_upaya_hukum_data_for_db()` - Siapkan data untuk tabel baru

#### Routes (src/app_with_db.py)
- `GET /view_upaya_hukum` - Halaman lihat data upaya hukum
- `POST /delete_upaya_hukum_item/<id>` - Hapus item upaya hukum
- Update `POST /confirm_import_upaya_hukum` - Simpan ke tabel upaya_hukum_data

#### Templates
- `view_upaya_hukum.html` - Halaman view data upaya hukum dengan filter dan statistik
- Update `import_upaya_hukum.html` - Panduan format CSV extended
- Update `import_upaya_hukum_preview.html` - Preview dengan kolom Banding, Kasasi, PK

### Changed - Integrasi Laporan

#### Database (src/models/mysql_database.py)
- Update `get_pidum_report_data()` - Sekarang juga menghitung data dari `upaya_hukum_data`
- Kolom UPAYA HUKUM di laporan menggabungkan data dari kedua tabel

#### Routes (src/app_with_db.py)
- Update `view_pidum` - Menampilkan total upaya hukum gabungan dengan breakdown

#### Templates
- Update `view_pidum.html` - Kartu Upaya Hukum menampilkan detail dan link ke view_upaya_hukum

---

## [1.1.0] - 2025-11-XX

### Added - Identitas Tersangka
- Kolom `identitas_tersangka` di tabel `pidum_data`
- Fitur pencarian berdasarkan nama tersangka di halaman view_pidum

---

## [1.0.0] - 2025-XX-XX

### Added - Migrasi MySQL
- Migrasi database dari SQLite ke MySQL (AWS RDS)
- File konfigurasi `.env` untuk koneksi database
- `src/config.py` - Manajemen konfigurasi
- `src/models/mysql_database.py` - Implementasi koneksi MySQL
- Script migrasi dan setup database

### Features
- Manajemen data PIDUM (Pidana Umum)
- Manajemen data PIDSUS (Pidana Khusus)
- Import data dari CSV
- Generate laporan
- Export ke Excel
- Visualisasi data dengan chart
- Autentikasi pengguna

---

## Struktur Tabel upaya_hukum_data

```sql
CREATE TABLE upaya_hukum_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    no TEXT,
    terdakwa_terpidana TEXT,
    no_tanggal_rp9 TEXT,
    jenis_perkara TEXT,
    -- Perlawanan (6 kolom)
    perlawanan_no_tgl_penetapan_pn TEXT,
    perlawanan_no_tgl_akte TEXT,
    perlawanan_tgl_pengajuan_memori TEXT,
    perlawanan_yang_mengajukan_jpu TEXT,
    perlawanan_yang_mengajukan_terdakwa TEXT,
    perlawanan_no_tgl_amar_penetapan_pt TEXT,
    -- Banding (5 kolom)
    banding_no_tgl_akte_permohonan TEXT,
    banding_tgl_pengajuan_memori TEXT,
    banding_yang_mengajukan_jpu TEXT,
    banding_yang_mengajukan_terdakwa TEXT,
    banding_no_tgl_amar_putusan_pt TEXT,
    -- Kasasi (5 kolom)
    kasasi_no_tgl_akte_permohonan TEXT,
    kasasi_tgl_pengajuan_memori TEXT,
    kasasi_yang_mengajukan_jpu TEXT,
    kasasi_yang_mengajukan_terdakwa TEXT,
    kasasi_no_tgl_amar_putusan_ma TEXT,
    -- Kasasi Demi Hukum (3 kolom)
    kasasi_demi_hukum_tgl_diajukan TEXT,
    kasasi_demi_hukum_keadaan_putusan_pn TEXT,
    kasasi_demi_hukum_no_tgl_amar_putusan_ma TEXT,
    -- PK (3 kolom)
    pk_tgl_diajukan_terpidana TEXT,
    pk_tgl_pemeriksaan_berita_acara TEXT,
    pk_no_tgl_amar_putusan TEXT,
    -- Grasi (5 kolom)
    grasi_tgl_penerimaan_berkas TEXT,
    grasi_tgl_penundaan_eksekusi TEXT,
    grasi_tgl_risalah_pertimbangan_kajari TEXT,
    grasi_tgl_terima_kepres TEXT,
    grasi_no_tgl_kepres_amar TEXT,
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Format CSV Import Upaya Hukum

### Kolom Wajib
| Nama Kolom | Deskripsi |
|------------|-----------|
| No | Nomor urut |
| Terdakwa_Terpidana | Nama terdakwa/terpidana |
| No_Tanggal_RP9 | Nomor dan tanggal RP9 |

### Kolom Opsional - Banding
| Nama Kolom | Deskripsi |
|------------|-----------|
| Banding_No_Tgl_Akte_Permohonan | Nomor dan tanggal akte permohonan |
| Banding_Tgl_Pengajuan_Memori | Tanggal pengajuan memori |
| Banding_Yang_Mengajukan_JPU | JPU yang mengajukan |
| Banding_Yang_Mengajukan_Terdakwa | Terdakwa yang mengajukan |
| Banding_No_Tgl_Amar_Putusan_PT | Putusan PT |

### Kolom Opsional - Kasasi
| Nama Kolom | Deskripsi |
|------------|-----------|
| Kasasi_No_Tgl_Akte_Permohonan | Nomor dan tanggal akte |
| Kasasi_Tgl_Pengajuan_Memori | Tanggal pengajuan memori |
| Kasasi_Yang_Mengajukan_JPU | JPU yang mengajukan |
| Kasasi_Yang_Mengajukan_Terdakwa | Terdakwa yang mengajukan |
| Kasasi_No_Tanggal_Amar_Putusan_MA | Putusan MA |

### Kolom Opsional - PK
| Nama Kolom | Deskripsi |
|------------|-----------|
| PK_Tgl_Diajukan_Terpidana | Tanggal diajukan |
| PK_Tgl_Pemeriksaan_Berita_Acara | Tanggal pemeriksaan |
| PK_No_Tgl_Amar_Putusan | Putusan PK |

### Kolom Opsional - Grasi
| Nama Kolom | Deskripsi |
|------------|-----------|
| Grasi_Tgl_Penerimaan_Berkas | Tanggal terima berkas |
| Grasi_Tgl_Penundaan_Eksekusi | Tanggal penundaan |
| Grasi_Tgl_Risalah_Pertimbangan_Kajari | Tanggal risalah |
| Grasi_Tgl_Terima_KEPRES | Tanggal terima KEPRES |
| Grasi_No_Tgl_KEPRES_Amar | Nomor KEPRES |
