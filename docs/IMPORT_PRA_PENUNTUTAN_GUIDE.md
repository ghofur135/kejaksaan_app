# Panduan Import Data Tahapan Pra Penuntutan

## Deskripsi
Panduan ini menjelaskan cara menggunakan fitur import data tahapan Pra Penuntutan dengan format CSV yang berasal dari data penuntutan kejaksaan.

## URL Access
```
http://localhost:5001/import_tahapan/pra_penuntutan
```

## Format File CSV yang Didukung

### Struktur Kolom yang Diperlukan
File CSV harus memiliki kolom-kolom berikut:

| Kolom | Deskripsi | Contoh |
|-------|-----------|--------|
| `No` | Nomor urut | 1, 2, 3, ... |
| `No_Tanggal_Register_Perkara` | Nomor register dan tanggal | PDM-\n22/PRBAL/Enz.2/09/2025\n2025-09-01 |
| `Identitas_Tersangka` | Nama dan identitas tersangka | IMRAN Bin IDRIS |
| `Tindak_Pidana_Didakwakan` | Pasal dan UU yang dilanggar | UU NO. 36 TAHUN 2009,Pasal 196 |
| `Jaksa_Penuntut_Umum` | Nama jaksa penuntut umum | SATENO, S.H.M.H. \| PANJI BANGUN INDRIYANTO, S.H. |

### Contoh Data CSV
```csv
No,No_Tanggal_Register_Perkara,Identitas_Tersangka,Tindak_Pidana_Didakwakan,Jaksa_Penuntut_Umum
1,"PDM-
22/PRBAL/Enz.2/09/2025
2025-09-01",IMRAN Bin IDRIS,"UU NO. 36 TAHUN 2009,Pasal 196","SATENO, S.H.M.H. | PANJI BANGUN INDRIYANTO, S.H."
```

## Proses Import

### 1. Upload File
1. Buka halaman import: `http://localhost:5001/import_tahapan/pra_penuntutan`
2. Pilih file CSV dengan format yang sesuai
3. Klik tombol "Upload dan Preview"

### 2. Preview dan Validasi
Setelah upload, sistem akan:
- **Parsing Data**: Menganalisis struktur CSV dan mengekstrak informasi
- **Ekstraksi Tanggal**: Mengambil tanggal dari kolom `No_Tanggal_Register_Perkara`
- **Analisis Jenis Perkara**: Memberikan saran kategori berdasarkan `Tindak_Pidana_Didakwakan`
- **Kompilasi Keterangan**: Menggabungkan informasi pasal, tersangka, dan JPU

### 3. Kategori Jenis Perkara yang Terdeteksi
Sistem dapat mendeteksi dan menyarankan kategori berikut:

| Kategori | Keywords Deteksi |
|----------|------------------|
| **NARKOBA** | UU NO.35 TAHUN 2009, Pasal 112, 114, 119, 117, 120, 127 |
| **KESUSILAAN** | Pasal 289, Pasal 81, UU NO.23 TAHUN 2002 |
| **OHARDA** | KUHP Pasal 362, 363, 372, 378 |
| **PERKARA ANAK** | UU NO.23 TAHUN 2002 |
| **PERKARA LAINNYA** | UU NO.36 TAHUN 2009, UU NO.17 TAHUN 2016, KUHP Pasal 351 |

### 4. Pilih Jenis Perkara
Pada halaman preview:
1. **Review Saran**: Sistem memberikan saran kategori untuk setiap baris
2. **Manual Override**: User dapat mengubah kategori sesuai kebutuhan
3. **Edit Data**: Dapat menyesuaikan periode, tanggal, dan keterangan
4. **Remove Data**: Dapat menghapus baris yang tidak diperlukan

### 5. Konfirmasi Import
1. Setelah semua data sudah sesuai, klik "Konfirmasi Import"
2. Data akan disimpan ke database dengan:
   - **Tahapan Penanganan**: PRA PENUNTUTAN
   - **Jenis Perkara**: Sesuai pilihan user
   - **Keterangan**: Informasi lengkap pasal, tersangka, dan JPU

## Hasil Import

### Data yang Tersimpan
Setiap record akan memiliki struktur:
```
NO: [nomor urut]
PERIODE: [periode yang dipilih]
TANGGAL: [tanggal dari register atau yang diedit]
JENIS PERKARA: [kategori yang dipilih]
TAHAPAN_PENANGANAN: PRA PENUNTUTAN
KETERANGAN: Pasal: [tindak pidana] | Tersangka: [identitas] | JPU: [nama jaksa]
```

### Contoh Hasil
```
NO: 1
PERIODE: 1
TANGGAL: 2025-09-01
JENIS PERKARA: PERKARA LAINNYA
TAHAPAN_PENANGANAN: PRA PENUNTUTAN
KETERANGAN: Pasal: UU NO. 36 TAHUN 2009,Pasal 196 | Tersangka: IMRAN Bin IDRIS | JPU: SATENO, S.H.M.H. | PANJI BANGUN INDRIYANTO, S.H.
```

## Fitur Khusus

### 1. Ekstraksi Tanggal Otomatis
- Sistem mengekstrak tanggal dari format register yang kompleks
- Format: `PDM-\n22/PRBAL/Enz.2/09/2025\n2025-09-01`
- Mengambil bagian tanggal: `2025-09-01`

### 2. Analisis Jenis Perkara Cerdas
- Menganalisis kolom `Tindak_Pidana_Didakwakan`
- Mencocokkan dengan database pasal dan UU
- Memberikan saran kategori yang akurat

### 3. Kompilasi Informasi Lengkap
- Menggabungkan semua informasi relevan dalam satu keterangan
- Format terstruktur: Pasal | Tersangka | JPU
- Memudahkan pencarian dan analisis data

## Validasi dan Error Handling

### File Format
- ✅ Mendukung: `.csv`, `.xlsx`, `.xls`
- ✅ Maksimal ukuran: 10MB
- ✅ Encoding: UTF-8

### Data Validation
- ✅ Otomatis generate nomor jika kosong
- ✅ Default periode = 1 jika kosong
- ✅ Default tanggal = hari ini jika tidak dapat diekstrak
- ✅ Wajib pilih jenis perkara sebelum import

## Troubleshooting

### Error: "Tidak ada file yang dipilih"
- **Solusi**: Pastikan file sudah dipilih sebelum upload

### Error: "Unsupported file format"
- **Solusi**: Gunakan file .csv, .xlsx, atau .xls

### Error: "Error memproses file"
- **Solusi**: Periksa format kolom CSV sesuai panduan

### Data tanggal tidak sesuai
- **Solusi**: Edit manual di halaman preview sebelum import

### Kategori jenis perkara salah
- **Solusi**: Ubah pilihan kategori di halaman preview

## Akses dan Navigasi

### Menu Navigation
- **Home** → **Input PIDUM** → **Import Tahapan Pra Penuntutan**
- **Direct URL**: `http://localhost:5001/import_tahapan/pra_penuntutan`

### Setelah Import
- Data dapat dilihat di: **View PIDUM Data**
- Laporan tersedia di: **Laporan PIDUM**
- Export Excel tersedia di halaman view data

---

**Catatan**: Fitur ini khusus dirancang untuk menangani format data penuntutan kejaksaan dengan struktur register yang kompleks. Sistem akan otomatis menganalisis dan mengkonversi data sesuai kebutuhan aplikasi.