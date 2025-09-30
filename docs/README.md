# Aplikasi Data PIDUM & PIDSUS

Aplikasi web berbasis Flask untuk mengelola data perkara PIDUM (Pidana Umum) dan PIDSUS (Pidana Khusus) dengan fitur input data, menampilkan tabel, export ke Excel, dan visualisasi grafik.

## Fitur

### Data PIDUM (Pidana Umum)
- Input data perkara pidana umum
- Menampilkan data dalam tabel yang interaktif
- Export data ke format Excel
- Grafik analisis data (berdasarkan jenis perkara dan upaya hukum)

### Data PIDSUS (Pidana Khusus)
- Input data perkara pidana khusus
- Menampilkan data dalam tabel yang interaktif
- Export data ke format Excel
- Grafik analisis data (berdasarkan jenis perkara dan status penyidikan)

## Struktur Aplikasi

```
my-project/
├── app.py                 # File utama aplikasi Flask
├── requirements.txt       # Dependencies Python
├── templates/            # Folder template HTML
│   ├── base.html        # Template base
│   ├── index.html       # Halaman beranda
│   ├── input_pidum.html # Form input PIDUM
│   ├── input_pidsus.html # Form input PIDSUS
│   ├── view_pidum.html  # Tampilan tabel PIDUM
│   ├── view_pidsus.html # Tampilan tabel PIDSUS
│   ├── pidum_charts.html # Grafik PIDUM
│   └── pidsus_charts.html # Grafik PIDSUS
└── README.md            # Dokumentasi
```

## Instalasi

1. Pastikan Python sudah terinstall di sistem Anda (minimal Python 3.7)

2. Clone atau download repository ini

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Aktifkan virtual environment (jika menggunakan):
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

5. Jalankan aplikasi:
```bash
python app.py
```

6. Buka browser dan akses: `http://127.0.0.1:5001`

5. Buka browser dan akses:
```
http://localhost:5000
```

## Cara Penggunaan

### 1. Input Data PIDUM
- Klik menu PIDUM > Input Data
- Isi form dengan data perkara pidana umum
- Klik "Simpan Data" untuk menyimpan

### 2. Input Data PIDSUS
- Klik menu PIDSUS > Input Data
- Isi form dengan data perkara pidana khusus
- Klik "Simpan Data" untuk menyimpan

### 3. Melihat Data
- Untuk melihat data PIDUM: menu PIDUM > Lihat Data
- Untuk melihat data PIDSUS: menu PIDSUS > Lihat Data
- Data ditampilkan dalam tabel dengan fitur pencarian dan pagination

### 4. Export ke Excel
- Di halaman lihat data, klik tombol "Export Excel"
- File Excel akan otomatis di-download dengan format yang sudah diformat

### 5. Melihat Grafik
- Untuk grafik PIDUM: menu PIDUM > Grafik
- Untuk grafik PIDSUS: menu PIDSUS > Grafik
- Grafik dapat diklik untuk diperbesar

## Struktur Data

### PIDUM
- **NO**: Nomor urut
- **PERIODE**: Periode waktu
- **TANGGAL**: Tanggal perkara (format: 21 DES - 10 JAN)
- **JENIS PERKARA**: Jenis perkara (NARKOBA, PERKARA ANAK, dll)
- **PRA PENUTUTAN**: Jumlah pra penututan
- **PENUNTUTAN**: Jumlah penuntutan
- **UPAYA HUKUM**: Jumlah upaya hukum

### PIDSUS
- **NO**: Nomor urut
- **PERIODE**: Periode waktu
- **TANGGAL**: Tanggal perkara (format: 21 DES - 10 JAN)
- **JENIS PERKARA**: Jenis perkara (TIPIKOR, KEPABEANAN, dll)
- **PENYIDIKAN**: Status penyidikan (0 atau 1)
- **PENUNTUTAN**: Status penuntutan (0 atau 1)
- **KETERANGAN**: Keterangan tambahan

## Teknologi yang Digunakan

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Processing**: Pandas
- **Excel Export**: OpenPyXL
- **Charts**: Matplotlib
- **Icons**: Font Awesome
- **Tables**: DataTables

## Catatan

- Aplikasi ini menggunakan in-memory storage, data akan hilang saat aplikasi di-restart
- Untuk production use, disarankan untuk menggunakan database yang proper (SQLite, PostgreSQL, dll)
- Grafik di-generate menggunakan Matplotlib dan ditampilkan sebagai base64 image

## Pengembangan Selanjutnya

- Integrasi dengan database
- Fitur login dan authentication
- Export ke format lain (PDF, CSV)
- Filter dan search yang lebih advanced
- Dashboard yang lebih interaktif
- Mobile responsive design enhancement

## Troubleshooting

### ❌ Error: No module named 'matplotlib' (atau module lainnya)
**Penyebab:** Menggunakan Python global, bukan virtual environment

**Solusi:**
```bash
# SALAH - jangan gunakan ini:
python app_with_db.py

# BENAR - gunakan virtual environment:
.venv\Scripts\python.exe app_with_db.py

# Atau gunakan script launcher:
start.bat
# atau
.\start.ps1
```

### ❌ Error: Script execution disabled (PowerShell)
**Solusi:**
```bash
# Gunakan batch file instead:
start.bat

# Atau izinkan PowerShell script:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❌ Error: Virtual environment not found
**Solusi:**
```bash
# Jalankan setup otomatis:
setup.bat

# Atau manual:
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

### ❌ Error: Port 5001 already in use
**Solusi:** Edit `app_with_db.py` dan ubah port:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Ganti ke port lain
```

### ✅ Quick Setup & Run
```bash
# 1. Setup (hanya sekali):
setup.bat

# 2. Run aplikasi:
start.bat
# atau
.venv\Scripts\python.exe app_with_db.py

# 3. Buka browser:
http://127.0.0.1:5001
```