# Realistic Dummy Data PIDUM Generator - Documentation

## ✅ Berhasil Generate 90 Dummy Data PIDUM Realistis!

Script `generate_realistic_pidum_dummy.py` telah berhasil membuat **90 data dummy realistis** berdasarkan format CSV nyata untuk periode **Agustus - Oktober 2025**.

## 📊 Detail Data yang Di-generate

### Distribusi Data:
- **Total**: 90 data (30 per bulan)
- **Agustus 2025**: 30 data
- **September 2025**: 30 data  
- **Oktober 2025**: 30 data

### Distribusi per Tahapan (setiap bulan):
- **PRA PENUNTUTAN**: 10 data (berdasarkan format SPDP)
- **PENUNTUTAN**: 10 data (berdasarkan format Register)
- **UPAYA HUKUM**: 10 data (berdasarkan format RP9)

## 🎯 Data Templates Realistis

### 1. **PRA PENUNTUTAN Templates** (dari CSV pra penuntutan):
```python
{
    "tgl_nomor": "2025-08-28 SPDP/63/VIII/RES.1.24/2025/Reskrim",
    "pasal": "Pasal 82 Undang-Undang Nomor 17 Tahun 2016...",
    "jenis": "PERKARA ANAK"
}
```

**Sample Keterangan PRA PENUNTUTAN**:
- `SPDP: 2025-08-18 SPDP/24/VIII/RES.4.2/2025/Resnarkoba | Pasal: Pasal 114 ayat (1) atau Pasal 112 ayat (1)...`
- `SPDP: 2025-09-05 B/SPDP/65/IX/RES.1.8/Reskrim | Pasal: Pasal 365 KUHP Jo Pasal 55 ayat (1)...`

### 2. **PENUNTUTAN Templates** (dari CSV penuntutan):
```python
{
    "register": "PDM-22/PRBAL/Enz.2/09/2025",
    "tersangka": "IMRAN Bin IDRIS",
    "tindak_pidana": "UU NO. 36 TAHUN 2009,Pasal 196",
    "jaksa": "SATENO, S.H.M.H. | PANJI BANGUN INDRIYANTO, S.H."
}
```

**Sample Keterangan PENUNTUTAN**:
- `Register: PDM-22/PRBAL/Enz.2/08/2025 | Tersangka: IMRAN Bin IDRIS | Tindak Pidana: UU NO. 36 TAHUN 2009,Pasal 196... | Jaksa: SATENO, S.H.M.H...`
- `Register: PDM-25/PRBAL/Eoh.2/09/2025 | Tersangka: SUWANDI Alias WANDI bin ENJANG SUTRISNA | Tindak Pidana: KUHP,Pasal 378#Pasal 372...`

### 3. **UPAYA HUKUM Templates** (dari CSV upaya hukum):
```python
{
    "terdakwa": "FADELA TRI ANGGRAENI Alias DELA Binti PAIJO",
    "rp9": "PDM- 08/PRBAL/Eoh.2/06/2025",
    "jenis_upaya": "Banding",
    "tanggal_transaksi": "Terdakwa: 2025-09-08 0"
}
```

**Sample Keterangan UPAYA HUKUM**:
- `Terdakwa: AHMAD BIN SULAIMAN | Jenis: Banding | RP9: PDM- 19/PRBAL/Enz.2/08/2025 | Tanggal Transaksi: 2025-08-18`
- `Terdakwa: NANA SUPRIATNA | Jenis: Banding | RP9: PDM- 11/PRBAL/Eoh.2/10/2025 | Tanggal Transaksi: 2025-10-09`

## 🏷️ Jenis Perkara Realistis

Data menggunakan **12 jenis perkara** yang sesuai dengan data CSV nyata:
1. **NARKOTIKA** - dari kasus narkoba UU 35/2009
2. **PERKARA ANAK** - dari UU 17/2016 perlindungan anak
3. **PENCURIAN** - dari KUHP pasal 362, 363, 365
4. **PENIPUAN** - dari KUHP pasal 378
5. **PENGANIAYAAN** - dari KUHP pasal 351
6. **PENGELAPAN** - dari KUHP pasal 372, 374
7. **KESUSILAAN** - untuk kasus kesusilaan
8. **JUDI** - untuk kasus perjudian
9. **KDRT** - untuk kekerasan dalam rumah tangga
10. **OHARDA** - untuk orang hilang dan mayat
11. **KORUPSI** - untuk kasus korupsi
12. **PERKARA LAINNYA** - untuk kasus lainnya

## 📈 Statistik Database

### Sebelum Generate:
- PIDUM records: **3**
- PIDSUS records: **0**

### Setelah Generate:
- PIDUM records: **93** (+90)
- PIDSUS records: **0**

## 🚀 Fitur Script

### 1. **Interactive Options**:
- **Option 1**: Generate new data (tambah ke existing)
- **Option 2**: Replace all data (hapus semua + generate baru)
- **Option 3**: Cancel operation

### 2. **Realistic Data Generation**:
- ✅ Format SPDP nyata untuk PRA PENUNTUTAN
- ✅ Format Register nyata untuk PENUNTUTAN  
- ✅ Format RP9 nyata untuk UPAYA HUKUM
- ✅ Tanggal random dalam periode yang tepat
- ✅ Pasal-pasal hukum yang sesuai kasus

### 3. **Smart Date Management**:
- Tanggal random dalam bulan yang sesuai
- Format tanggal konsisten (YYYY-MM-DD)
- Periode nama bulan yang benar

### 4. **Data Quality**:
- Template berdasarkan data CSV nyata
- Variasi nama dengan template realistis
- Keterangan detail dan informatif
- Jenis perkara sesuai dengan pasal

## 📊 Sample Data Results

### Agustus 2025 - PRA PENUNTUTAN:
```
NO: 1, Periode: Agustus 2025
Tanggal: 2025-08-18, Jenis: PENCURIAN
Tahapan: PRA PENUNTUTAN
Keterangan: SPDP: 2025-09-24 B/SPDP/75/IX/RES.1.8./2025/Reskrim | Pasal: Pasal 362 KUHP...
```

### September 2025 - PENUNTUTAN:
```
NO: 41, Periode: September 2025  
Tanggal: 2025-09-15, Jenis: NARKOTIKA
Tahapan: PENUNTUTAN
Keterangan: Register: PDM-25/PRBAL/Enz.2/09/2025 | Tersangka: AIFAN GUSTI KURNIAWAN...
```

### Oktober 2025 - UPAYA HUKUM:
```
NO: 81, Periode: Oktober 2025
Tanggal: 2025-10-09, Jenis: PERKARA LAINNYA  
Tahapan: UPAYA HUKUM
Keterangan: Terdakwa: NANA SUPRIATNA | Jenis: Banding | RP9: PDM- 19/PRBAL/Enz.2/10/2025...
```

## 🔧 Technical Implementation

### Data Structure:
```python
{
    'NO': '1',
    'PERIODE': 'Agustus 2025',
    'TANGGAL': '2025-08-18',
    'JENIS PERKARA': 'PENCURIAN',
    'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',
    'KETERANGAN': 'SPDP: 2025-08-18 B/SPDP/75/VIII/RES.1.8./2025/Reskrim | Pasal: Pasal 362 KUHP'
}
```

### Templates Used:
- **6 PRA PENUNTUTAN templates** dari CSV pra penuntutan
- **6 PENUNTUTAN templates** dari CSV penuntutan  
- **3 UPAYA HUKUM templates** dari CSV upaya hukum
- **26 variasi nama** untuk diversitas

## 🎯 Benefits

### 1. **Realistic Testing Data**:
- Data sesuai format CSV nyata
- Pattern yang konsisten dengan sistem sebenarnya
- Jenis perkara yang relevan

### 2. **Comprehensive Coverage**:
- Semua tahapan penanganan tercakup
- Distribusi merata per bulan dan tahapan
- Variasi pasal dan kasus yang beragam

### 3. **Import API Testing**:
- Data siap untuk test semua fitur import
- Format konsisten dengan API yang ada
- Pattern sesuai dengan expectation user

## 🚀 Usage

### View Generated Data:
```
http://localhost:5001/view_pidum
```

### Test Import APIs:
- **PRA PENUNTUTAN**: `http://127.0.0.1:5001/import_pra_penuntutan_api`
- **UPAYA HUKUM**: `http://127.0.0.1:5001/import_upaya_hukum_api`  
- **PENUNTUTAN**: `http://127.0.0.1:5001/import_tahapan/penuntutan`

### Re-run Script:
```bash
cd /home/dhimas/project/kejaksaan
python3 generate_realistic_pidum_dummy.py
```

---

## 📝 Summary

✅ **90 data dummy realistis berhasil dibuat!**

- 📅 **Periode**: Agustus - Oktober 2025 (30 data/bulan)
- 📊 **Distribusi**: 30 PRA PENUNTUTAN + 30 PENUNTUTAN + 30 UPAYA HUKUM  
- 🎯 **Quality**: Berdasarkan template CSV nyata
- 💾 **Database**: 3 → 93 records (+90)
- 🔧 **Ready**: Siap untuk testing semua fitur aplikasi

Data dummy sekarang realistis dan representatif terhadap data sebenarnya!