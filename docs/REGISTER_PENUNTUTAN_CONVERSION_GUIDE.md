# 📋 Panduan Konversi dan Import Register Penuntutan

## 🎯 **Overview**
Fitur ini memungkinkan konversi file CSV register penuntutan ke format yang sesuai untuk import ke sistem PIDUM. File yang sudah dikonversi dapat langsung diimport dengan tahapan "Penuntutan".

## 📂 **File yang Telah Diproses**

### **File Original:**
- **Nama:** `05 SEPTEMBER - 19 SEPTEMBER (penuntutan)_output.csv`
- **Lokasi:** `/csv/05 SEPTEMBER - 19 SEPTEMBER (penuntutan)_output.csv`
- **Format:** 
  ```csv
  Tanggal Register,Tindak Pidana yang Didakwakan
  2025-09-01,"UU NO. 36 TAHUN 2009,Pasal 196"
  2025-09-04,"UU NO.35 TAHUN 2009,Pasal 119 ayat (2)#Pasal 117 ayat (2)..."
  ```

### **File Hasil Konversi:**
- **Nama:** `05 SEPTEMBER - 19 SEPTEMBER (penuntutan)_output_converted_for_import.csv`
- **Lokasi:** `/csv/05 SEPTEMBER - 19 SEPTEMBER (penuntutan)_output_converted_for_import.csv`
- **Format PIDUM:**
  ```csv
  NO,PERIODE,TANGGAL,JENIS PERKARA,KETERANGAN
  1,2025-10,2025-09-01,PIDUM,"UU NO. 36 TAHUN 2009,Pasal 196"
  2,2025-10,2025-09-01,PIDUM,"UU NO. 36 TAHUN 2009,Pasal 196"
  ```

## 🔧 **Cara Konversi Manual**

### **Menggunakan Script Python:**
```bash
cd /home/dhimas/project/kejaksaan
python3 convert_penuntutan_csv.py
```

### **Menggunakan Fitur Web:**
1. Buka aplikasi web: `http://127.0.0.1:5001`
2. Pilih menu "Konversi PDF" → "Register Penuntutan"
3. Upload file CSV original
4. Download hasil konversi

## 📥 **Cara Import ke Sistem**

### **Langkah 1: Akses Halaman Import**
1. Buka: `http://127.0.0.1:5001/input_pidum`
2. Pilih "Import Penuntutan"
3. Atau langsung ke: `http://127.0.0.1:5001/import_tahapan/penuntutan`

### **Langkah 2: Upload File**
1. Pilih file yang sudah dikonversi: `*_converted_for_import.csv`
2. Klik "Upload dan Preview"

### **Langkah 3: Review Data**
1. Periksa mapping kolom:
   - **Tanggal** → Kolom tanggal register
   - **Keterangan** → Kolom tindak pidana/dakwaan
2. Pilih jenis perkara jika diperlukan
3. Hapus baris yang tidak diinginkan

### **Langkah 4: Konfirmasi Import**
1. Klik "Simpan ke Database"
2. Data akan masuk dengan tahapan "Penuntutan"

## 🎛️ **Fitur Konversi Otomatis**

### **Mapping Kolom Otomatis:**
- `Tanggal Register` → `TANGGAL`
- `Tindak Pidana yang Didakwakan` → `KETERANGAN`
- Otomatis menambah: `NO`, `PERIODE`, `JENIS PERKARA`

### **Format Output:**
- **NO:** Nomor urut otomatis (1, 2, 3, ...)
- **PERIODE:** Format `YYYY-MM` (default: bulan sekarang)
- **TANGGAL:** Format `YYYY-MM-DD` dari kolom tanggal register
- **JENIS PERKARA:** Default "PIDUM"
- **KETERANGAN:** Berisi referensi hukum/pasal

## 📊 **Statistik File**

### **Data yang Diproses:**
- **Total Record:** 12 baris data
- **Rentang Tanggal:** 1 September - 25 September 2025
- **Jenis Kasus:**
  - UU No. 36 Tahun 2009 (Narkoba)
  - UU No. 35 Tahun 2009 (Narkoba)
  - KUHP (Pencurian, Penipuan, Penganiayaan)
  - UU No. 17 Tahun 2016
  - UU No. 23 Tahun 2002

## 🔍 **Validasi Data**

### **Format Tanggal:**
- ✅ Format valid: `YYYY-MM-DD` (2025-09-01)
- ✅ Dapat dibaca oleh sistem import

### **Format Keterangan:**
- ✅ Berisi referensi hukum yang lengkap
- ✅ Pasal dan undang-undang tercantum jelas
- ✅ Format sesuai untuk laporan PIDUM

## 🚀 **Akses Cepat**

### **URL Langsung:**
- **Import Penuntutan:** `http://127.0.0.1:5001/import_tahapan/penuntutan`
- **Konversi Register:** `http://127.0.0.1:5001/convert_register_penuntutan`
- **Beranda:** `http://127.0.0.1:5001`

### **File Ready to Import:**
```
/home/dhimas/project/kejaksaan/csv/05 SEPTEMBER - 19 SEPTEMBER (penuntutan)_output_converted_for_import.csv
```

## ✅ **Status**
- ✅ File CSV telah dikonversi ke format PIDUM
- ✅ Mapping kolom berhasil (Tanggal → TANGGAL, Tindak Pidana → KETERANGAN)
- ✅ Format siap untuk import dengan tahapan "Penuntutan"
- ✅ Data dapat diakses melalui sistem web

---

## 📝 **Notes**
- File original tetap tersimpan sebagai backup
- File hasil konversi menggunakan periode default (2025-10)
- Semua data dikategorikan sebagai "PIDUM"
- Tahapan penanganan akan diset sebagai "Penuntutan" saat import