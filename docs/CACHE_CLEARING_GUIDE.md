# PANDUAN MEMBERSIHKAN CACHE UNTUK FIX TANGGAL IMPORT

Tanggal pada import preview masih menunjukkan 01 semua? **Ini adalah masalah CACHE**, bukan kode!

## ✅ LANGKAH-LANGKAH PEMBERSIHAN CACHE (IKUTI SEMUA):

### STEP 1: BERSIHKAN PYTHON CACHE (Windows)

Buka Terminal/PowerShell dan jalankan:

```bash
cd D:\my-project\kejaksaan_app

# Hapus semua Python cache files
rmdir /s /q __pycache__
del *.pyc
for /r . %d in (__pycache__) do @rmdir /s /q "%d" 2>nul
```

Atau cara mudah - buka file explorer, sorting by type, cari "__pycache__" folders dan delete semua!

### STEP 2: STOPKAN FLASK APP

- **Tekan `Ctrl+C`** di terminal tempat Flask berjalan
- Tunggu sampai terminal menunjukkan "[Exited]" atau "[Done]"
- Tunggu 5 detik (penting! jangan langsung restart)

### STEP 3: JALANKAN FLASK ULANG

```bash
python app_with_db.py
```

Tunggu sampai muncul:
```
 * Running on http://127.0.0.1:5002
 * Press CTRL+C to quit
```

### STEP 4: CLEAR BROWSER CACHE

**OPTION A: Hard Refresh**
- Tekan `Ctrl+Shift+R` (hard refresh tanpa cache)

**OPTION B: Clear Browsing Data**
- Tekan `Ctrl+Shift+Delete`
- Pilih "Cached images and files"
- Klik "Clear data"

**OPTION C: Disable Cache Completely**
- Buka DevTools: `F12`
- Klik tab "Network"
- Centang checkbox "Disable cache"
- Refresh page: `Ctrl+R`

### STEP 5: TEST IMPORT ULANG

1. Buka: http://127.0.0.1:5002/import_tahapan/penuntutan
2. Upload file: `Penuntutan Juli - Oktober_extracted_20251025_122735.csv`
3. **LIHAT PREVIEW TANGGAL** - seharusnya berbeda-beda BUKAN semua 01!

## ✓ HASIL YANG DIHARAPKAN:

Kolom "Tanggal" pada preview seharusnya menampilkan:
- Row 1: 02/07/2025 (hari 02, bukan 01)
- Row 2: 07/07/2025 (hari 07)
- Row 3: 08/07/2025 (hari 08)
- dst... (semua berbeda)

Bukan:
- Row 1: 01/07/2025 ✗
- Row 2: 01/07/2025 ✗
- Row 3: 01/07/2025 ✗

## JIKA MASIH TIDAK BERHASIL:

1. Pastikan sudah follow SEMUA 5 steps di atas
2. Coba gunakan browser BARU (Incognito mode)
3. Coba matikan antivirus sementara (jika ada cache blocking)
4. Report dengan screenshot showing:
   - Terminal Flask output
   - Preview page tanggal values yang muncul
