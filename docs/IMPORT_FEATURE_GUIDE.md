# Fitur Import Data PIDUM - Kejaksaan App

## 🚀 **Fitur Baru: Import Data dari Excel/CSV**

### 📋 **Overview**
Fitur import memungkinkan pengguna untuk mengupload data PIDUM dalam format Excel atau CSV, dengan kemampuan untuk memilih jenis perkara yang sesuai sebelum data disimpan ke database.

### 📁 **Files yang Ditambahkan:**
- `import_helper.py` - Helper functions untuk memproses file import
- `templates/import_pidum.html` - Halaman upload file
- `templates/import_preview.html` - Halaman preview dan mapping jenis perkara
- `sample_pidum_data.csv` - File contoh untuk testing

### 🔧 **Files yang Dimodifikasi:**
- `app_with_db.py` - Menambahkan routes import dan konfigurasi upload
- `templates/input_pidum.html` - Menambahkan link ke fitur import

## 🎯 **Cara Penggunaan**

### 1. **Akses Fitur Import**
- Buka halaman "Input Data PIDUM"
- Klik tombol "Import dari Excel/CSV" di header

### 2. **Upload File**
- Pilih file Excel (.xlsx, .xls) atau CSV (.csv)
- Maksimal ukuran file: 10MB
- File harus memiliki kolom yang sesuai

### 3. **Preview dan Mapping**
- Sistem akan menganalisis data dan memberikan saran jenis perkara
- User dapat memilih jenis perkara yang sesuai untuk setiap baris data
- Tombol "Gunakan Semua Saran" untuk menggunakan semua saran sistem
- User dapat menghapus baris yang tidak diinginkan

### 4. **Konfirmasi Import**
- Review data yang akan diimport
- Klik "Simpan ke Database" untuk menyimpan

## 📊 **Format File yang Didukung**

### **Kolom yang Diharapkan:**
| Kolom | Deskripsi | Required |
|-------|-----------|----------|
| NO | Nomor urut | Ya |
| PERIODE | Periode data | Ya |
| TANGGAL | Tanggal (YYYY-MM-DD, DD/MM/YYYY, dll) | Ya |
| JENIS PERKARA | Jenis perkara original | Opsional* |
| PRA PENUTUTAN | Jumlah pra penututan | Ya |
| PENUNTUTAN | Jumlah penuntutan | Ya |
| UPAYA HUKUM | Jumlah upaya hukum | Ya |

*Jika tidak ada, user harus memilih manual

### **Contoh Format CSV:**
```csv
NO,PERIODE,TANGGAL,JENIS PERKARA,PRA PENUTUTAN,PENUNTUTAN,UPAYA HUKUM
1,1,2025-09-01,Kasus Narkotika,5,3,2
2,1,2025-09-02,Perkara Anak Dibawah Umur,2,1,1
```

## 🤖 **Smart Mapping Jenis Perkara**

Sistem menganalisis teks jenis perkara original dan memberikan saran:

### **Mapping Rules:**
- **NARKOBA**: Narkoba, Narkotika, Drugs, Sabu, Ganja
- **PERKARA ANAK**: Anak, Juvenile, Minor, Remaja
- **KESUSILAAN**: Kesusilaan, Susila, Moral, Cabul, Perkosaan
- **JUDI**: Judi, Gambling, Togel, Taruhan
- **KDRT**: KDRT, Kekerasan Dalam Rumah Tangga, Domestic Violence
- **OHARDA**: OHARDA, Orang Hilang, Harta Benda
- **PERKARA LAINNYA**: Default untuk yang tidak cocok

## 🛠 **Teknical Details**

### **Routes Baru:**
- `GET/POST /import_pidum` - Upload dan preview file
- `POST /confirm_import_pidum` - Konfirmasi dan simpan data

### **Session Storage:**
- Data import disimpan sementara di session
- Dibersihkan setelah konfirmasi atau cancel

### **Error Handling:**
- Validasi format file
- Validasi ukuran file (max 10MB)
- Error handling untuk parsing data
- Validasi kolom required

### **Security:**
- `secure_filename()` untuk sanitize nama file
- Validasi ekstensi file
- Session-based temporary storage

## 📝 **Testing**

### **File Sample:**
Gunakan `sample_pidum_data.csv` untuk testing:
```bash
# File sudah tersedia di:
/home/dhimas/project/kejaksaan/sample_pidum_data.csv
```

### **Test Cases:**
1. ✅ Upload file CSV valid
2. ✅ Upload file Excel valid
3. ✅ File dengan jenis perkara berbeda
4. ✅ Mapping otomatis jenis perkara
5. ✅ Manual selection jenis perkara
6. ✅ Remove baris yang tidak diinginkan
7. ✅ Validasi form sebelum submit

## 🔄 **Workflow Import**

```
1. User Upload File
   ↓
2. Parse & Validate File
   ↓
3. Analyze & Suggest Jenis Perkara
   ↓
4. Display Preview Table
   ↓
5. User Select/Modify Jenis Perkara
   ↓
6. User Confirm Import
   ↓
7. Insert to Database
   ↓
8. Show Success Message
```

## 🎨 **UI Features**

- **Progress Indication**: Clear steps dan feedback
- **Smart Suggestions**: Auto-select berdasarkan analisis
- **Bulk Actions**: "Gunakan Semua Saran" button
- **Inline Editing**: Edit jenis perkara per baris
- **Remove Rows**: Hapus baris yang tidak diinginkan
- **Validation**: Real-time form validation
- **Responsive Design**: Mobile-friendly interface

## 🚦 **Status & Next Steps**

### **Implemented ✅**
- File upload (CSV, Excel)
- Smart jenis perkara mapping
- Preview interface
- Bulk import to database
- Error handling
- Session management

### **Future Enhancements 🔄**
- Import untuk PIDSUS data
- Batch validation rules
- Import history tracking
- Data conflict resolution
- Advanced mapping rules
- File template download

**Fitur Import PIDUM siap digunakan!** 🎉