# Import Upaya Hukum API - User Guide

## ✅ API Berhasil Dibuat!

API baru untuk import CSV Upaya Hukum telah berhasil dibuat dengan mekanisme yang sama persis seperti API import pra penuntutan.

## 🚀 Cara Menggunakan

### 1. Akses API
- **URL**: `http://127.0.0.1:5001/import_upaya_hukum_api`
- **URL Redirect**: `http://127.0.0.1:5001/import_tahapan/upaya_hukum` (akan redirect ke API)

### 2. Format File CSV yang Dibutuhkan
File CSV harus memiliki kolom-kolom berikut:
```csv
No,Terdakwa_Terpidana,No_Tanggal_RP9
1,FADELA TRI ANGGRAENI Alias DELA Binti PAIJO,PDM- 08/PRBAL/Eoh.2/06/2025
2,RENO ALI MUKHTAMAR Alias RENO Bin AHMAD SUBARNO,PDM- 11/PRBAL/Eoh.2/07/2025
3,ADITYA SETIAWAN bin WAHIDIN,PDM- 19/PRBAL/Enz.2/06/2025
```

### 3. Proses Import
1. **Upload File**: Pilih file CSV/Excel dan upload
2. **Preview Data**: Sistem akan menampilkan preview data yang telah diproses
3. **Pilih Jenis Perkara**: User dapat memilih jenis perkara untuk setiap data
4. **Konfirmasi**: Submit untuk menyimpan data ke database

## 🎯 Fitur Utama

### ✅ Analisis Otomatis Jenis Perkara
Sistem akan menganalisis nama terdakwa dan memberikan saran jenis perkara:
- **NARKOTIKA** - jika nama mengandung kata terkait narkoba
- **KORUPSI** - jika mengandung kata terkait korupsi
- **PENCURIAN** - jika mengandung kata terkait pencurian
- **PENIPUAN** - jika mengandung kata terkait penipuan
- **PENGANIAYAAN** - jika mengandung kata terkait kekerasan
- **PEMBUNUHAN** - jika mengandung kata terkait pembunuhan
- **PERKOSAAN** - jika mengandung kata terkait perkosaan
- **PENGELAPAN** - jika mengandung kata terkait pengelapan
- **PERKARA LAINNYA** - default untuk kasus lainnya

### ✅ Ekstraksi Tanggal Otomatis
Sistem akan mengekstrak tanggal dari format RP9:
- Input: `PDM- 08/PRBAL/Eoh.2/06/2025`
- Output: `2025-06-01` (tahun-bulan-01)

### ✅ Validasi Data
- Validasi format file (CSV, XLS, XLSX)
- Validasi kolom yang diperlukan
- Filter baris header otomatis
- Validasi data kosong

### ✅ Preview dan Edit
- Preview data sebelum import
- Edit periode, tanggal, jenis perkara, keterangan
- Hapus baris yang tidak diperlukan
- Checkbox untuk inclusion/exclusion

## 📝 Data yang Disimpan

Setiap baris akan disimpan dengan struktur:
- **NO**: Nomor urut
- **PERIODE**: Periode data (default: 1)
- **TANGGAL**: Tanggal yang diekstrak dari RP9
- **JENIS PERKARA**: Pilihan user dari dropdown
- **TAHAPAN_PENANGANAN**: "UPAYA HUKUM" (otomatis)
- **KETERANGAN**: Informasi gabungan terdakwa dan RP9

## 🔧 File Helper yang Dibuat

1. **`import_upaya_hukum_helper.py`** - Logic processing import
2. **`templates/import_upaya_hukum.html`** - Form upload
3. **`templates/import_upaya_hukum_preview.html`** - Preview dan konfirmasi
4. **Route `/import_upaya_hukum_api`** - API endpoint utama
5. **Route `/confirm_import_upaya_hukum`** - Konfirmasi import

## 🎉 Hasil

API ini memberikan user kemampuan untuk:
1. ✅ Upload file CSV dengan format RP9
2. ✅ Otomatis menganalisis dan menyarankan jenis perkara
3. ✅ Preview dan edit data sebelum import
4. ✅ Memilih data mana yang akan disimpan
5. ✅ Import data ke database dengan tahapan "UPAYA HUKUM"

File contoh yang sudah tersedia (`05 SEPTEMBER - 19 SEPTEMBER (upaya hukum)_extracted_20251002_105906.csv`) dapat langsung digunakan untuk testing API ini.

---

**Mekanisme ini persis sama dengan API import pra penuntutan, namun disesuaikan dengan format data Upaya Hukum yang memiliki struktur RP9.**