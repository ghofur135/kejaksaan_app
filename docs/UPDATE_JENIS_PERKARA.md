# Update Jenis Perkara - Kejaksaan App

## Perubahan yang Dilakukan

### PIDUM (Pidana Umum)
Jenis perkara telah diupdate menjadi:
1. NARKOBA
2. PERKARA ANAK
3. KESUSILAAN
4. JUDI
5. KDRT
6. OHARDA
7. PERKARA LAINNYA

**Sebelumnya:**
- NARKOBA
- PERKARA ANAK
- PENCURIAN
- PENGANIAYAAN
- PENIPUAN
- LAIN-LAIN

### PIDSUS (Pidana Khusus)
Jenis perkara telah diupdate menjadi:
1. TIPIKOR
2. KEPABEANAN
3. BEA CUKAI
4. TPPU
5. PERPAJAKAN
6. PERKARA LAINNYA

**Sebelumnya:**
- TIPIKOR
- KEPABEANAN
- CUKAI
- MIGAS
- KAYU
- LAIN-LAIN

## Files yang Dimodifikasi
- `templates/input_pidum.html` - Updated dropdown jenis perkara PIDUM
- `templates/input_pidsus.html` - Updated dropdown jenis perkara PIDSUS

## Status Aplikasi
✅ Aplikasi telah di-restart dengan PM2
✅ Perubahan sudah aktif dan dapat digunakan
✅ Database tetap kompatibel dengan perubahan ini

## Testing
Untuk memverifikasi perubahan:
1. Buka http://127.0.0.1:5001
2. Klik "Input Data PIDUM" - Cek dropdown jenis perkara
3. Klik "Input Data PIDSUS" - Cek dropdown jenis perkara

Data yang sudah ada di database tetap akan ditampilkan dengan benar.