# Update Import Upaya Hukum - Format CSV Baru

## ✅ API Import Upaya Hukum Berhasil Diperbarui!

API import upaya hukum telah diperbarui untuk mendukung format CSV yang baru dengan kolom tambahan.

## 🔄 Perubahan Format CSV

### Format Lama (Masih Didukung):
```csv
No,Terdakwa_Terpidana,No_Tanggal_RP9
1,FADELA TRI ANGGRAENI Alias DELA Binti PAIJO,PDM- 08/PRBAL/Eoh.2/06/2025
```

### Format Baru (Diprioritaskan):
```csv
No,Terdakwa_Terpidana,No_Tanggal_RP9,Jenis_Upaya_Hukum,Tanggal_Transaksi,Banding_Akte,Kasasi_Akte,PK_Tanggal
1,FADELA TRI ANGGRAENI Alias DELA Binti PAIJO,PDM- 08/PRBAL/Eoh.2/06/2025,Banding,Terdakwa: 2025-09-08 0,Terdakwa: 2025-09-08 0,,
```

## 🚀 Fitur Baru yang Ditambahkan

### 1. **Backward Compatibility**
- ✅ Mendukung format CSV lama (3 kolom)
- ✅ Mendukung format CSV baru (8 kolom)
- ✅ Otomatis deteksi format yang digunakan

### 2. **Kolom Tambahan yang Didukung**
- **Jenis_Upaya_Hukum**: Jenis upaya hukum (Banding, Kasasi, PK)
- **Tanggal_Transaksi**: Tanggal transaksi (contoh: "Terdakwa: 2025-09-08 0")
- **Banding_Akte**: Data akta banding
- **Kasasi_Akte**: Data akta kasasi  
- **PK_Tanggal**: Data tanggal PK

### 3. **Enhanced Date Extraction**
- ✅ Prioritas: Gunakan `Tanggal_Transaksi` jika tersedia
- ✅ Fallback: Ekstrak dari `No_Tanggal_RP9` 
- ✅ Pattern matching untuk berbagai format tanggal

### 4. **Improved Keterangan**
Keterangan sekarang lebih detail dan informatif:
```
Terdakwa: FADELA TRI ANGGRAENI | Jenis: Banding | RP9: PDM- 08/PRBAL/Eoh.2/06/2025 | Banding: Terdakwa: 2025-09-08 0
```

## 🔧 Perubahan Teknis

### 1. **Function Updates** (`import_upaya_hukum_helper.py`)

#### New Function:
```python
def extract_date_from_transaksi(tanggal_transaksi):
    """Extract date from Tanggal_Transaksi field"""
    # Patterns: "Terdakwa: 2025-09-08 0" atau "Jaksa: 2025- 09-01 0"
```

#### Enhanced Validation:
```python
# Support both old and new format
required_columns_old = ['No', 'Terdakwa_Terpidana', 'No_Tanggal_RP9']
required_columns_new = ['No', 'Terdakwa_Terpidana', 'No_Tanggal_RP9', 'Jenis_Upaya_Hukum']
```

#### Enhanced Data Processing:
```python
# Extract additional data if available (new format)
jenis_upaya_hukum = str(row.get('Jenis_Upaya_Hukum', '')).strip()
tanggal_transaksi = str(row.get('Tanggal_Transaksi', '')).strip()
banding_akte = str(row.get('Banding_Akte', '')).strip()
kasasi_akte = str(row.get('Kasasi_Akte', '')).strip()
pk_tanggal = str(row.get('PK_Tanggal', '')).strip()
```

### 2. **Template Updates**

#### Updated Panduan:
- Kolom wajib vs opsional dijelaskan
- Contoh format CSV baru
- Penjelasan prioritas tanggal

#### Enhanced Preview:
- Tampilkan jenis upaya hukum jika tersedia
- Keterangan lebih detail dengan informasi tambahan

## 📊 Sample Data Processing

### Input CSV:
```csv
No,Terdakwa_Terpidana,No_Tanggal_RP9,Jenis_Upaya_Hukum,Tanggal_Transaksi,Banding_Akte,Kasasi_Akte,PK_Tanggal
1,FADELA TRI ANGGRAENI Alias DELA Binti PAIJO,PDM- 08/PRBAL/Eoh.2/06/2025,Banding,Terdakwa: 2025-09-08 0,Terdakwa: 2025-09-08 0,,
```

### Processed Data:
```python
{
    'NO': '1',
    'PERIODE': '1',
    'TANGGAL': '2025-09-08',  # From Tanggal_Transaksi
    'JENIS PERKARA': 'PERKARA LAINNYA',  # User selectable
    'TAHAPAN_PENANGANAN': 'UPAYA HUKUM',
    'KETERANGAN': 'Terdakwa: FADELA TRI ANGGRAENI | Jenis: Banding | RP9: PDM- 08/PRBAL/Eoh.2/06/2025 | Banding: Terdakwa: 2025-09-08 0'
}
```

## 🎯 Testing dengan File Baru

### File Sample:
`05 SEPTEMBER - 19 SEPTEMBER (upaya hukum)_extracted_20251004_094150.csv`

### Expected Results:
1. ✅ Format detection: NEW FORMAT
2. ✅ Date extraction: From Tanggal_Transaksi
3. ✅ Enhanced keterangan with all available info
4. ✅ Jenis upaya hukum displayed in preview
5. ✅ All additional fields preserved

## 🚀 Cara Testing

### 1. Akses API:
```
http://127.0.0.1:5001/import_upaya_hukum_api
```

### 2. Upload File:
- Pilih file: `05 SEPTEMBER - 19 SEPTEMBER (upaya hukum)_extracted_20251004_094150.csv`
- Klik "Upload dan Preview"

### 3. Verify Results:
- ✅ Data ter-parse dengan benar
- ✅ Tanggal diambil dari Tanggal_Transaksi (2025-09-08, 2025-09-22, 2025-09-01)
- ✅ Keterangan berisi semua informasi
- ✅ Jenis upaya hukum "Banding" terdeteksi

### 4. Confirm Import:
- Pilih jenis perkara sesuai kebutuhan
- Submit untuk import ke database

## 📈 Compatibility Matrix

| Format | Columns | Status | Notes |
|--------|---------|--------|-------|
| Old Format | 3 cols | ✅ Supported | Basic functionality |
| New Format | 8 cols | ✅ Enhanced | Full features |
| Mixed Format | Variable | ✅ Adaptive | Auto-detection |

## 🛡️ Error Handling

### Invalid Format:
```
Format tidak sesuai. Kolom minimal yang diperlukan: No, Terdakwa_Terpidana, No_Tanggal_RP9 atau No, Terdakwa_Terpidana, No_Tanggal_RP9, Jenis_Upaya_Hukum
```

### Date Parsing Fallback:
1. Try extract from Tanggal_Transaksi
2. Fallback to No_Tanggal_RP9
3. Final fallback to current date

---

## 📝 Summary

✅ **API Import Upaya Hukum berhasil diperbarui untuk mendukung format CSV baru!**

- 🔄 **Backward Compatible**: Format lama tetap didukung
- 🆕 **Enhanced Features**: 5 kolom tambahan didukung
- 📅 **Smart Date Extraction**: Prioritas dari Tanggal_Transaksi
- 📝 **Detailed Keterangan**: Informasi lebih lengkap
- 🎯 **Ready for Testing**: Siap test dengan file CSV baru

**URL Testing**: `http://127.0.0.1:5001/import_upaya_hukum_api`