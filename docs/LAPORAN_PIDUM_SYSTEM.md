# Laporan PIDUM System

## Overview
Sistem laporan PIDUM telah dibuat untuk menampilkan data dalam format tabel dan grafik sesuai dengan format yang diminta, dengan struktur yang sama persis seperti gambar reference.

## Fitur Laporan PIDUM

### 📊 **Tabel Laporan**
- **Format**: Sesuai dengan gambar reference
- **Kolom**:
  - NO (Nomor urut)
  - BULAN (Bulan laporan)
  - JENIS PERKARA (7 kategori)
  - JUMLAH (Total per jenis perkara)
  - PRA PENUNTUTAN (Jumlah di tahap pra penuntutan)
  - PENUNTUTAN (Jumlah di tahap penuntutan)
  - UPAYA HUKUM (Jumlah di tahap upaya hukum)
- **Total Row**: Menampilkan total keseluruhan di baris terakhir

### 📈 **Grafik PIDUM**
- **Jenis**: Bar chart (grafik batang)
- **Data**: Menampilkan jumlah total per jenis perkara
- **Label**: Nilai ditampilkan di atas setiap batang
- **Style**: Sesuai dengan format reference

### 🎯 **Jenis Perkara**
1. NARKOBA
2. PERKARA ANAK  
3. KESUSILAAN
4. JUDI
5. KDRT
6. OHARDA
7. PERKARA LAINNYA

### 🔍 **Filter Periode**
- **Dropdown filter** untuk memilih bulan dan tahun
- **Default**: Bulan dan tahun saat ini
- **Range tahun**: 2020-2030
- **Update otomatis**: Data dan grafik terupdate sesuai filter

## Route dan Endpoint

### `/laporan_pidum`
- **Method**: GET
- **Parameters**: 
  - `bulan` (optional): 1-12
  - `tahun` (optional): 2020-2030
- **Template**: `laporan_pidum.html`
- **Function**: `laporan_pidum()`

## Database Function

### `get_pidum_report_data(bulan=None, tahun=None)`
- **Purpose**: Mengambil data agregat untuk laporan
- **Logic**: 
  - GROUP BY jenis_perkara dan tahapan_penanganan
  - Filter berdasarkan bulan/tahun jika disediakan
  - Mengembalikan data terstruktur dengan zero values untuk jenis perkara yang tidak ada data

### `generate_pidum_chart(report_data)`
- **Purpose**: Generate grafik bar chart
- **Output**: Base64 encoded PNG image
- **Features**:
  - Responsive design
  - Value labels pada setiap bar
  - Grid untuk readability
  - Auto-scaling Y axis

## Template Features

### Layout
- **Responsive design** dengan Bootstrap
- **Print-friendly** CSS untuk cetak laporan
- **Filter dropdown** dengan form styling
- **Export buttons** (Excel dan Print)

### Styling
- **Table styling**: Bordered, striped dengan header yang sesuai reference
- **Chart container**: Centered dengan responsive image
- **Color scheme**: Professional dengan highlight pada total row

## Sample Data
Script `insert_sample_data.py` menyediakan data sample yang sesuai dengan struktur laporan:

```
NARKOBA: 4 total (1 Pra Penuntutan, 3 Penuntutan)
PERKARA ANAK: 2 total (2 Pra Penuntutan)  
OHARDA: 4 total (3 Pra Penuntutan, 1 Penuntutan)
PERKARA LAINNYA: 2 total (1 Pra Penuntutan, 1 Penuntutan)
```

## Integration

### Navigation
- Link ditambahkan di halaman index dengan icon dan styling yang konsisten
- Accessible dari menu utama dengan button "Laporan PIDUM"

### Export Features
- **Excel Export**: Filter berdasarkan periode yang sedang ditampilkan
- **Print Function**: CSS print-friendly dengan hidden elements

## Implementation Details

### Data Aggregation
```sql
SELECT 
    jenis_perkara,
    tahapan_penanganan,
    COUNT(*) as jumlah,
    strftime('%m', tanggal) as bulan,
    strftime('%Y', tanggal) as tahun
FROM pidum_data
WHERE strftime('%m', tanggal) = ? AND strftime('%Y', tanggal) = ?
GROUP BY jenis_perkara, tahapan_penanganan
```

### Chart Generation
- **Library**: Matplotlib dengan backend 'Agg'
- **Format**: PNG dengan DPI 150
- **Encoding**: Base64 untuk embedding di HTML
- **Styling**: Custom colors dan fonts untuk professional look

## Testing
1. **Insert sample data**: `python3 insert_sample_data.py`
2. **Start application**: Port 5003
3. **Access report**: `http://localhost:5003/laporan_pidum`
4. **Test filters**: Pilih September 2025 untuk melihat data sample

## Output Format
Laporan yang dihasilkan **persis sama** dengan format di gambar reference:
- ✅ Struktur tabel identik
- ✅ Kolom dan header sesuai
- ✅ Grafik bar chart dengan nilai
- ✅ Total row di bawah
- ✅ Data September dengan distribusi yang tepat