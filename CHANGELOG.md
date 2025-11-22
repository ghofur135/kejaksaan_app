# Changelog

Semua perubahan penting pada proyek ini akan didokumentasikan di file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
