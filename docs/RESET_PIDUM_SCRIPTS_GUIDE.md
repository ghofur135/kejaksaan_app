# Dokumentasi Script Reset Data PIDUM

## Deskripsi
Repository ini menyediakan 3 script berbeda untuk reset data PIDUM dari database aplikasi kejaksaan, dengan berbagai tingkat fleksibilitas dan kemudahan penggunaan.

## 🔧 Script yang Tersedia

### 1. `reset_pidum_data.py` - Script Lengkap & Fleksibel

**Fitur:**
- Reset berdasarkan kriteria (semua, tahapan, periode)
- Backup otomatis database
- Statistik data sebelum dan sesudah reset
- Konfirmasi keamanan
- Logging lengkap

**Usage:**
```bash
# Melihat statistik data saja
python3 reset_pidum_data.py --stats

# Reset semua data dengan backup
python3 reset_pidum_data.py --all --backup

# Reset berdasarkan tahapan
python3 reset_pidum_data.py --tahapan="PRA PENUNTUTAN" --backup

# Reset berdasarkan periode
python3 reset_pidum_data.py --periode="1" --backup

# Reset tanpa konfirmasi (hati-hati!)
python3 reset_pidum_data.py --all --confirm --backup
```

**Opsi:**
- `--all`: Reset semua data PIDUM
- `--tahapan=X`: Reset berdasarkan tahapan (PRA PENUNTUTAN, PENUNTUTAN, UPAYA HUKUM)
- `--periode=X`: Reset berdasarkan periode
- `--backup`: Buat backup sebelum reset
- `--confirm`: Skip konfirmasi user
- `--stats`: Tampilkan statistik saja
- `--help`: Bantuan lengkap

### 2. `simple_reset_pidum.py` - Script Sederhana

**Fitur:**
- Reset semua data PIDUM dengan sekali jalan
- Backup otomatis
- Interface sederhana
- Konfirmasi keamanan

**Usage:**
```bash
python3 simple_reset_pidum.py
```

**Output Example:**
```
==================================================
🗃️  SIMPLE RESET DATA PIDUM
==================================================

📊 Data PIDUM saat ini: 31 records

⚠️  WARNING: Akan menghapus SEMUA 31 data PIDUM!

Lanjutkan? (y/N): y

🔄 Creating backup...
✅ Backup created: kejaksaan_backup_20251002_095051.db
🔄 Resetting data...
✅ Berhasil menghapus 31 data PIDUM
📊 Data PIDUM sekarang: 0 records
==================================================
```

### 3. `reset_pidum.sh` - Script Bash

**Fitur:**
- Script bash untuk environment Unix/Linux
- Reset semua data PIDUM
- Backup otomatis
- Cepat dan ringan

**Usage:**
```bash
chmod +x reset_pidum.sh
./reset_pidum.sh
```

## 📊 Statistik Data

### Informasi yang Ditampilkan:
- **Total Records**: Jumlah total data PIDUM
- **Per Tahapan**: Breakdown berdasarkan tahapan penanganan
  - PRA PENUNTUTAN
  - PENUNTUTAN  
  - UPAYA HUKUM
- **Per Periode**: Breakdown berdasarkan periode
- **Per Jenis Perkara**: Breakdown berdasarkan kategori
  - NARKOBA
  - KESUSILAAN
  - OHARDA
  - PERKARA ANAK
  - JUDI
  - KDRT
  - PERKARA LAINNYA

### Contoh Output Statistik:
```
📊 STATISTIK DATA PIDUM SAAT INI:
   Total Records: 31
   Per Tahapan:
     - PENUNTUTAN: 10 records
     - PRA PENUNTUTAN: 21 records
   Per Periode:
     - Periode 1: 29 records
     - Periode 2: 2 records
   Per Jenis Perkara:
     - NARKOBA: 10 records
     - OHARDA: 8 records
     - PERKARA ANAK: 6 records
     - PERKARA LAINNYA: 4 records
     - JUDI: 1 records
     - KDRT: 1 records
     - KESUSILAAN: 1 records
```

## 🔒 Keamanan & Backup

### Backup Otomatis
- Semua script membuat backup database sebelum reset
- Format nama: `kejaksaan_backup_YYYYMMDD_HHMMSS.db`
- Lokasi: `./db/backups/` (script lengkap) atau `./db/` (script sederhana)

### Konfirmasi Keamanan
- Semua script meminta konfirmasi sebelum menghapus data
- Menampilkan jumlah data yang akan dihapus
- Opsi `--confirm` untuk bypass konfirmasi (script lengkap)

### Validasi
- Cek keberadaan database sebelum operasi
- Validasi kriteria reset (tahapan, periode)
- Error handling untuk operasi database

## 💡 Skenario Penggunaan

### 1. Reset Harian/Berkala
```bash
# Reset semua data untuk periode baru
python3 reset_pidum_data.py --all --backup --confirm
```

### 2. Reset Data Testing
```bash
# Reset data tahapan tertentu setelah testing import
python3 reset_pidum_data.py --tahapan="PRA PENUNTUTAN" --backup
```

### 3. Maintenance Database
```bash
# Lihat statistik data terlebih dahulu
python3 reset_pidum_data.py --stats

# Reset berdasarkan analisis
python3 reset_pidum_data.py --periode="1" --backup
```

### 4. Reset Cepat
```bash
# Untuk reset cepat tanpa banyak opsi
python3 simple_reset_pidum.py
```

## ⚠️ Warning & Best Practices

### Peringatan Penting:
1. **Backup Selalu**: Gunakan opsi `--backup` sebelum reset
2. **Verifikasi Target**: Pastikan kriteria reset sudah benar
3. **Environment**: Jangan jalankan di production tanpa backup eksternal
4. **Permission**: Pastikan script memiliki akses write ke database

### Best Practices:
1. **Backup Manual**: Buat backup manual database sebelum operasi besar
2. **Test Environment**: Test script di environment development terlebih dahulu
3. **Verifikasi**: Cek statistik sebelum dan sesudah reset
4. **Documentation**: Catat kapan dan mengapa reset dilakukan

## 🛠️ Troubleshooting

### Error: "Database not found"
```bash
# Pastikan path database benar
ls -la db/kejaksaan.db

# Atau cek dari direktori yang benar
cd /path/to/kejaksaan/
python3 reset_pidum_data.py --stats
```

### Error: "Permission denied"
```bash
# Beri permission execute
chmod +x reset_pidum_data.py
chmod +x simple_reset_pidum.py
chmod +x reset_pidum.sh

# Atau jalankan dengan python
python3 reset_pidum_data.py --stats
```

### Error: "no such table: pidum_data"
```bash
# Cek struktur database
python3 -c "
import sqlite3
conn = sqlite3.connect('db/kejaksaan.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
print(cursor.fetchall())
"
```

### Backup Gagal
```bash
# Pastikan folder backup ada dan writable
mkdir -p db/backups
chmod 755 db/backups
```

## 📝 Log File

### Script Lengkap
- Output lengkap ke console
- Backup path ditampilkan
- Statistik sebelum dan sesudah

### Script Sederhana  
- Output minimal ke console
- Konfirmasi operasi

### Script Bash
- Output ke console dengan format Unix-style
- Exit code untuk automation

---

**Catatan**: Script ini dirancang khusus untuk aplikasi kejaksaan dengan database SQLite. Pastikan untuk melakukan backup sebelum operasi reset untuk mencegah kehilangan data.