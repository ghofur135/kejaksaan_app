# Debugging Steps untuk Issue Tanggal Import

## Status Saat Ini
- Kode sudah di-fix untuk parse tanggal dengan benar
- Testing menunjukkan tanggal sudah benar di import_helper.py
- **TAPI:** Preview page mungkin masih menunjukkan 01

## Penyebab Kemungkinan
1. Flask belum benar-benar di-restart (module cache)
2. Ada file lama yang masih ter-load
3. Browser cache

## Fix yang Diperlukan

### Step 1: Bersihkan Python Cache
```bash
cd D:\my-project\kejaksaan_app
# Remove Python cache files
del /s __pycache__
del *.pyc
```

### Step 2: Restart Flask Sepenuhnya
- **Hentikan Flask app** (Ctrl+C di terminal)
- **Tunggu 3 detik** 
- **Jalankan Flask lagi**

### Step 3: Clear Browser Cache
- Buka http://127.0.0.1:5002 
- Tekan Ctrl+Shift+Delete (Clear Browsing Data)
- Atau buka console: F12 → Network → Disable cache (checkbox)

### Step 4: Test Import Ulang
1. Pergi ke: http://127.0.0.1:5002/import_tahapan/penuntutan
2. Upload file: `Penuntutan Juli - Oktober_extracted_20251025_122735.csv`
3. **LIHAT PREVIEW** - apakah tanggal berbeda-beda?
4. **LIHAT CONSOLE Flask** - harus muncul tanggal yang berbeda

### Step 5: Cek Console Output
Saat upload file, di terminal Flask harus muncul output seperti:
```
[DEBUG] First 3 rows tanggal from import_helper:
  Row 0: 2025-07-02
  Row 1: 2025-07-07
  Row 2: 2025-07-08
  
[DEBUG] Processing NO_TANGGAL_REGISTER_PERKARA row 0
[DEBUG] Raw register_value: 'PDM- 10/PRBAL/Eoh.2/07/2025 2025-07-02'
[DEBUG] Regex matched: 2025-07-02
[DEBUG] Final TANGGAL set to: 2025-07-02
[DEBUG] Row 0 final: NO=1, TANGGAL=2025-07-02
...
```

### PENTING: Apa yang Dicari
- Di console: TANGGAL harus BERBEDA-BEDA (02, 07, 08, 10, 22, 23, dll)
- Di preview page: Input date harus menampilkan hari yang berbeda
- Jika MASIH semua 01 → ada issue lain

## Jika Masih Bermasalah
Report dengan screenshot/log yang menunjukkan:
1. Console output dari Flask
2. Screenshot preview page
3. Apakah sudah clear cache browser?
4. Apakah sudah restart Flask dengan Ctrl+C + run ulang?
