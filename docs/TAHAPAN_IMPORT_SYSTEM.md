# Sistem Import Tahapan Penanganan Perkara

## Overview
Sistem import telah diperbarui untuk mendukung 3 tahapan penanganan perkara yang berbeda:
1. **Pra Penuntutan**
2. **Penuntutan** 
3. **Upaya Hukum**

## Perubahan Database Schema
Database PIDUM telah diperbarui dengan:
- **Kolom Baru**: `tahapan_penanganan` dan `keterangan`
- **Kolom Dihapus**: `pra_penututan`, `penuntutan`, `upaya_hukum`

### Schema Baru:
```sql
CREATE TABLE pidum_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    no TEXT NOT NULL,
    periode TEXT NOT NULL,
    tanggal TEXT NOT NULL,
    jenis_perkara TEXT NOT NULL,
    tahapan_penanganan TEXT NOT NULL,
    keterangan TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Format Import File

### Kolom yang Diperlukan:
- **NO**: Nomor urut data
- **PERIODE**: Periode laporan
- **TANGGAL**: Tanggal kejadian (format: YYYY-MM-DD)
- **JENIS PERKARA**: Jenis perkara (akan dipilih saat preview)
- **KETERANGAN**: Detail pasal pelanggaran atau informasi tambahan

### Contoh Format CSV/Excel:
```csv
NO,PERIODE,TANGGAL,JENIS PERKARA,KETERANGAN
1,1,2025-09-30,NARKOBA,Pasal 112 UU No. 35 Tahun 2009
2,1,2025-09-30,KESUSILAAN,Pasal 289 KUHP
3,1,2025-10-01,KDRT,Pasal 44 ayat (1) UU No. 23 Tahun 2004
```

## Fitur Import Tahapan

### 1. Import Pra Penuntutan
- **URL**: `/import_tahapan/pra_penuntutan`
- **Tahapan**: Data disimpan dengan `tahapan_penanganan = 'PRA PENUNTUTAN'`
- **Template**: `import_pra_penuntutan.html`

### 2. Import Penuntutan
- **URL**: `/import_tahapan/penuntutan`
- **Tahapan**: Data disimpan dengan `tahapan_penanganan = 'PENUNTUTAN'`
- **Template**: `import_penuntutan.html`

### 3. Import Upaya Hukum
- **URL**: `/import_tahapan/upaya_hukum`
- **Tahapan**: Data disimpan dengan `tahapan_penanganan = 'UPAYA HUKUM'`
- **Template**: `import_upaya_hukum.html`

## Workflow Import

1. **Pilih Tahapan**: User memilih tahapan dari dropdown menu di halaman Input PIDUM
2. **Upload File**: User upload file CSV/Excel dengan format yang sesuai
3. **Preview Data**: Sistem menampilkan preview data dengan saran jenis perkara
4. **Validasi**: User dapat mengedit periode, tanggal, jenis perkara, dan keterangan
5. **Simpan**: Data disimpan ke database dengan tahapan yang sesuai

## Routes Baru

### 1. `import_tahapan/<tahapan>`
- **Method**: GET, POST
- **Fungsi**: Menampilkan form import dan memproses upload file
- **Parameter**: tahapan (pra_penuntutan, penuntutan, upaya_hukum)

### 2. `confirm_import_tahapan`
- **Method**: POST
- **Fungsi**: Memproses konfirmasi import dari preview
- **Data**: Form data dengan jenis perkara yang dipilih user

## Fungsi Database Baru

### `get_pidum_data_by_tahapan(tahapan_penanganan)`
- Mengambil data PIDUM berdasarkan tahapan tertentu
- Return: List dictionary data yang sudah difilter

### `insert_pidum_data(data)`
- Updated untuk menerima `tahapan_penanganan` dan `keterangan`
- Kolom wajib: NO, PERIODE, TANGGAL, JENIS PERKARA, TAHAPAN_PENANGANAN, KETERANGAN

## Migration Script

File `migrate_database.py` telah dibuat untuk:
- Backup database existing
- Menambah kolom baru
- Menghapus kolom lama
- Migrasi data existing

### Menjalankan Migration:
```bash
python3 migrate_database.py
```

## File Template Baru

1. **`import_pra_penuntutan.html`**: Form import untuk tahapan Pra Penuntutan
2. **`import_penuntutan.html`**: Form import untuk tahapan Penuntutan  
3. **`import_upaya_hukum.html`**: Form import untuk tahapan Upaya Hukum
4. **`import_tahapan_preview.html`**: Preview data sebelum import dengan tahapan

## Jenis Perkara Tersedia

- NARKOBA
- PERKARA ANAK
- KESUSILAAN
- JUDI
- KDRT
- OHARDA
- PERKARA LAINNYA

## Testing

File contoh: `sample_import_tahapan.csv` telah disediakan untuk testing import.

## Catatan Penting

1. **Backward Compatibility**: Route import lama (`/import_pidum`) masih tersedia untuk transisi
2. **Data Migration**: Data existing akan diset dengan `tahapan_penanganan = 'PRA PENUNTUTAN'` secara default
3. **Validation**: Semua field wajib diisi saat import
4. **Error Handling**: Sistem akan menampilkan error detail jika ada data yang gagal diimport