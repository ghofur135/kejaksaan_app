# Dummy Data PIDUM Generator - Documentation

## ✅ Berhasil Generate 150 Dummy Data PIDUM!

Script `generate_dummy_pidum.py` telah berhasil membuat 150 data dummy untuk periode **Agustus - Oktober 2025**.

## 📊 Detail Data yang Di-generate

### Periode Data:
- **Agustus 2025**: ~50 data
- **September 2025**: ~50 data  
- **Oktober 2025**: ~50 data
- **Total**: 150 data baru

### Jenis Perkara (9 kategori):
1. **NARKOTIKA** - kasus narkoba, sabu-sabu, ganja
2. **KORUPSI** - korupsi dana, gratifikasi, penyuapan
3. **PENCURIAN** - pencurian kendaraan, rumah, tempat umum
4. **PENIPUAN** - penipuan online, investasi bodong, arisan
5. **PENGANIAYAAN** - kekerasan, KDRT, perkelahian
6. **PEMBUNUHAN** - pembunuhan berencana, perampokan
7. **PERKOSAAN** - perkosaan, pencabulan anak
8. **PENGELAPAN** - pengelapan dana, barang inventaris
9. **PERKARA LAINNYA** - pelanggaran hukum lainnya

### Tahapan Penanganan (3 kategori):
1. **PRA PENUNTUTAN** - tahap awal penanganan
2. **PENUNTUTAN** - tahap penuntutan
3. **UPAYA HUKUM** - tahap upaya hukum

## 🎯 Fitur Dummy Data

### Keterangan Realistis:
- **NARKOTIKA**: "Kepemilikan sabu-sabu seberat 1.2 gram"
- **KORUPSI**: "Korupsi dana bantuan sosial sebesar Rp 250 juta"
- **PENCURIAN**: "Pencurian sepeda motor di mall"
- **PENIPUAN**: "Penipuan online sebesar Rp 100 juta"
- **PENGANIAYAAN**: "Penganiayaan berat menggunakan pisau"

### Variasi Data:
- **Berat narkotika**: 0.5g - 25.0g
- **Nominal uang**: Rp 50 juta - Rp 2.5 miliar
- **Lokasi**: Jakarta Utara, Selatan, Timur, Barat, Pusat
- **Jenis barang**: sepeda motor, handphone, laptop, perhiasan
- **Instansi**: dinas pendidikan, puskesmas, kelurahan

## 📈 Statistik Database

### Sebelum Generate:
- PIDUM records: **16**
- PIDSUS records: **0**

### Setelah Generate:
- PIDUM records: **166** (+150)
- PIDSUS records: **0**

## 🚀 Cara Menggunakan Script

### Running Script:
```bash
cd /home/dhimas/project/kejaksaan
python3 generate_dummy_pidum.py
```

### Interactive Mode:
1. Script menampilkan statistik database saat ini
2. Konfirmasi untuk melanjutkan (y/N)
3. Generate 150 dummy data
4. Insert ke database dengan progress indicator
5. Tampilkan hasil akhir

## 🔧 Struktur Data yang Di-generate

```python
{
    'NO': '1',
    'PERIODE': 'Agustus 2025',
    'TANGGAL': '2025-08-15',
    'JENIS PERKARA': 'NARKOTIKA',
    'TAHAPAN_PENANGANAN': 'UPAYA HUKUM',
    'KETERANGAN': 'Kepemilikan sabu-sabu seberat 1.2 gram'
}
```

## 📍 Viewing Results

Data dummy dapat dilihat di:
- **URL**: `http://localhost:5001/view_pidum`
- **Features**: Pagination, search, filter, delete
- **Export**: Excel export tersedia
- **Total data**: 166 records (16 original + 150 dummy)

## 🎨 Sample Keterangan

### NARKOTIKA:
- "Kepemilikan sabu-sabu seberat 2.5 gram"
- "Penyalahgunaan narkotika jenis ganja"
- "Pengedar narkoba di wilayah Jakarta Utara"

### KORUPSI:
- "Korupsi dana APBD sebesar Rp 500 juta"
- "Gratifikasi dalam proyek pembangunan jalan"
- "Penyuapan untuk tender pengadaan komputer"

### PENCURIAN:
- "Pencurian handphone di stasiun"
- "Pencurian kendaraan bermotor sepeda motor"
- "Pencurian dengan kekerasan"

## 🛡️ Safety Features

### Data Validation:
- Tanggal random dalam range yang valid
- Keterangan realistis per jenis perkara
- Progress indicator saat insert
- Error handling per record

### Database Integration:
- Menggunakan fungsi insert_pidum_data() existing
- Compatible dengan struktur database
- Auto-increment ID
- Timestamp creation

## 🔄 Rerun Script

Script dapat dijalankan berulang kali untuk menambah data lebih banyak. Setiap run akan:
- Generate 150 data baru dengan nomor urut berbeda
- Tanggal random baru dalam periode yang sama
- Variasi keterangan yang berbeda

---

## 📝 Summary

✅ **150 dummy data PIDUM berhasil di-generate!**
- 📅 Periode: Agustus - Oktober 2025
- 🏷️ 9 jenis perkara berbeda
- 📊 3 tahapan penanganan
- 💾 Database: 16 → 166 records
- 🌐 View: http://localhost:5001/view_pidum

Data siap digunakan untuk testing fitur aplikasi!