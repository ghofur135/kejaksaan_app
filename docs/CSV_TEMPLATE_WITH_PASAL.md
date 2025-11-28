# CSV Template Baru - Dengan Kolom Pasal Dedicated

**Last Updated:** 28 November 2025
**Version:** 2.0 (Opsi B - With Dedicated Pasal Column)

---

## ✅ IMPLEMENTASI SELESAI!

Database dan sistem import telah diupdate untuk support kolom **Pasal** dedicated.

### Perubahan yang Telah Dilakukan:

1. ✅ **Database Schema Updated**
   - Kolom `pasal` TEXT ditambahkan di `pidum_data`
   - Kolom `pasal` TEXT ditambahkan di `pidsus_data`

2. ✅ **Data Migration Completed**
   - 80 rows dengan format SPDP berhasil di-migrate
   - Pasal berhasil di-extract dari field keterangan

3. ✅ **Import System Updated**
   - `import_helper.py` - Support kolom Pasal dari CSV
   - `import_pra_penuntutan_helper.py` - Support kolom Pasal
   - `mysql_database.py` - Insert/update dengan field pasal

---

## 📋 CSV TEMPLATE BARU

### 1. Template untuk PENUNTUTAN & UPAYA HUKUM

**File:** `template_import_penuntutan_dengan_pasal.csv`

```csv
No,No_Tanggal_Register_Perkara,Pasal,Identitas_Tersangka,Jenis_Perkara
1,PDM- 02/PRBAL/Eku.2/01/2025,Pasal 303 KUHP,ALDI RAMADANI,JUDI
2,PDM- 03/PRBAL/Enz.2/02/2025,Pasal 362 KUHP,BUDI SANTOSO,OHARDA
3,PDM- 04/PRBAL/Eoh.2/03/2025,Pasal 114 UU RI No. 35/2009,CHANDRA,NARKOBA
```

**Kolom-kolom:**
| Kolom | Required | Format | Contoh | Keterangan |
|---|---|---|---|---|
| `No` | Optional | Integer | 1, 2, 3 | Nomor urut (auto jika kosong) |
| `No_Tanggal_Register_Perkara` | **Required** | Text | PDM- 02/PRBAL/... | Nomor register perkara |
| **`Pasal`** | **Required** | Text | Pasal 303 KUHP | **NEW: Pasal yang didakwakan** |
| `Identitas_Tersangka` | **Required** | Text | ALDI RAMADANI | Nama tersangka |
| `Jenis_Perkara` | Optional | Predefined | JUDI | Auto-suggest jika kosong |

---

### 2. Template untuk PRA PENUNTUTAN

**File:** `template_import_pra_penuntutan_dengan_pasal.csv`

```csv
No,Tgl_Nomor,Pasal_yang_Disangkakan,Identitas_Tersangka
1,2025-01-23 SPDP/63/VIII/...,Pasal 303 KUHP,JUROCHMAN
2,2025-02-14 SPDP/64/VIII/...,Pasal 362 KUHP,LUJENG WAHYONO
3,2025-03-12 SPDP/65/VIII/...,Pasal 114 UU RI No. 35/2009,HAMBO PAMUNGKAS
```

**Kolom-kolom:**
| Kolom | Required | Format | Contoh | Keterangan |
|---|---|---|---|---|
| `No` | Optional | Integer | 1, 2, 3 | Nomor urut |
| `Tgl_Nomor` | **Required** | Date + Text | 2025-01-23 SPDP/... | Tanggal + Nomor SPDP |
| **`Pasal_yang_Disangkakan`** | **Required** | Text | Pasal 303 KUHP | Pasal yang didakwakan |
| `Identitas_Tersangka` | **Required** | Text | JUROCHMAN | Nama tersangka |

**Catatan:** Format PRA PENUNTUTAN sudah support pasal sejak awal, tidak ada perubahan format CSV.

---

## 🔄 PERBEDAAN FORMAT LAMA vs BARU

### Format LAMA (Sebelum Update):

**PENUNTUTAN CSV:**
```csv
No,No_Tanggal_Register_Perkara,Identitas_Tersangka
1,PDM- 02/PRBAL/Eku.2/01/2025,ALDI RAMADANI
```

**Hasil di Database:**
```
pasal: NULL  ❌
keterangan: "PDM- 02/PRBAL/Eku.2/01/2025"
```

---

### Format BARU (Setelah Update):

**PENUNTUTAN CSV:**
```csv
No,No_Tanggal_Register_Perkara,Pasal,Identitas_Tersangka
1,PDM- 02/PRBAL/Eku.2/01/2025,Pasal 303 KUHP,ALDI RAMADANI
```

**Hasil di Database:**
```
pasal: "Pasal 303 KUHP"  ✅
keterangan: "PDM- 02/PRBAL/Eku.2/01/2025"
```

---

## 📊 STATUS DATA SETELAH IMPLEMENTASI

**Total Data PIDUM:** 140 rows

| Kategori | Jumlah | Status Pasal |
|---|---|---|
| Data PRA PENUNTUTAN (format SPDP) | 80 | ✅ **Ada Pasal** (migrated) |
| Data PENUNTUTAN (format PDM) | 47 | ⚠️ **Belum Ada Pasal** (perlu update) |
| Data UPAYA HUKUM (format PDM) | 13 | ⚠️ **Belum Ada Pasal** (perlu update) |

**Action Items untuk Data Lama:**
- 60 rows (PENUNTUTAN + UPAYA HUKUM) belum punya pasal
- **Opsi 1:** Input manual via form edit
- **Opsi 2:** Re-import dengan CSV baru yang include pasal
- **Opsi 3:** Biarkan NULL (laporan akan tampil dash `-`)

---

## 💡 PANDUAN PENGGUNAAN

### Untuk Import Data BARU (ke Depan):

**1. Buat CSV dengan format baru:**
- Pastikan kolom **Pasal** ada dan diisi
- Download template dari: `docs/templates/` (jika tersedia)

**2. Import via Web Interface:**
- Login ke aplikasi
- Pilih menu "Import Data"
- Pilih tahapan (PRA PENUNTUTAN / PENUNTUTAN / UPAYA HUKUM)
- Upload file CSV
- **Preview akan menampilkan kolom Pasal** ✅
- Confirm dan save

**3. Verifikasi:**
- Cek di menu "View Data"
- Kolom Pasal harus terisi

---

### Untuk Update Data LAMA (60 rows tanpa pasal):

**Opsi A: Edit Manual (Satu per satu)**

1. Login ke aplikasi
2. Menu "View PIDUM" atau "View PIDSUS"
3. Klik "Edit" pada row yang ingin diupdate
4. **Isi field "Pasal"** (field baru akan muncul di form)
5. Save

**Opsi B: Re-Import dengan CSV Baru**

1. Export data existing ke CSV
2. Tambahkan kolom "Pasal" di Excel/CSV
3. Isi kolom Pasal untuk setiap row
4. Delete data lama (optional)
5. Re-import dengan CSV baru

**Opsi C: Bulk Update via SQL** (Advanced)

```sql
-- Update manual via SQL query
UPDATE pidum_data
SET pasal = 'Pasal XXX KUHP'
WHERE id = YYY;
```

---

## 📝 CONTOH DATA LENGKAP

### Contoh 1: Data PENUNTUTAN dengan Pasal

**CSV Input:**
```csv
No,No_Tanggal_Register_Perkara,Pasal,Identitas_Tersangka,Jenis_Perkara
1,PDM- 02/PRBAL/Eku.2/01/2025,Pasal 303 KUHP,Aci,JUDI
```

**Hasil di Database:**
```
id: 1501
no: 1
periode: 1
tanggal: 2025-01-15
jenis_perkara: JUDI
tahapan_penanganan: PENUNTUTAN
pasal: "Pasal 303 KUHP"  ✅
identitas_tersangka: "Aci"
keterangan: "PDM- 02/PRBAL/Eku.2/01/2025"
```

**Tampil di Laporan Pelacakan Perkara:**
| No | Nama | Pasal | Jenis | Pra Penuntutan | Penuntutan | Upaya Hukum |
|---|---|---|---|---|---|---|
| 1 | Aci | **Pasal 303 KUHP** | JUDI | - | 15/01/2025 | - |

---

### Contoh 2: Data PRA PENUNTUTAN (Existing Format)

**CSV Input:**
```csv
No,Tgl_Nomor,Pasal_yang_Disangkakan,Identitas_Tersangka
1,2025-01-23 SPDP/63/VIII/RES.1.24/2025/Reskrim,Pasal 303 KUHP,JUROCHMAN
```

**Hasil di Database:**
```
pasal: "Pasal 303 KUHP"  ✅
keterangan: "SPDP: 2025-01-23 SPDP/63/VIII/RES.1.24/2025/Reskrim"
```

---

## ⚠️ CATATAN PENTING

### 1. **Pasal vs Keterangan**

**SEBELUM (Format Lama):**
- Pasal tercampur di field `keterangan`
- Format: `"SPDP: ... | Pasal: Pasal 303"`

**SEKARANG (Format Baru):**
- Pasal punya kolom dedicated: `pasal`
- Keterangan hanya isi info lain (nomor register, dll)
- **Clean separation** ✅

### 2. **Backward Compatibility**

- ✅ Data lama tetap bisa dibaca
- ✅ Import format lama (tanpa kolom Pasal) tetap work, tapi field pasal akan NULL
- ✅ Aplikasi tidak break dengan data existing

### 3. **Validation**

Saat ini **tidak ada validation** untuk field Pasal. User bisa isi format apa saja.

**Rekomendasi:**
- Gunakan format konsisten: "Pasal XXX KUHP" atau "Pasal XXX UU RI No. XX/YYYY"
- Hindari typo (Pasai, pASAL, dll)
- Case-insensitive untuk query (akan di-handle di backend)

---

## 🚀 NEXT STEPS

### Immediate (Hari Ini):
1. ✅ Database updated
2. ✅ Import system updated
3. ✅ Data migration completed
4. ⏳ **Test import dengan CSV baru** (recommended)

### Short Term (Minggu Ini):
1. ⏳ Update data lama (60 rows tanpa pasal) - optional
2. ⏳ Training user untuk format CSV baru
3. ⏳ Update form input manual untuk include field Pasal

### Long Term (Bulan Ini):
1. ⏳ Add validation untuk format pasal
2. ⏳ Auto-complete / suggestion untuk pasal umum
3. ⏳ Analytics per pasal (top 10 pasal, dll)

---

## 📞 SUPPORT

Jika ada pertanyaan atau issue:
1. Check dokumentasi ini terlebih dahulu
2. Test dengan sample CSV kecil (2-3 rows)
3. Report issue dengan detail:
   - CSV yang digunakan
   - Error message (jika ada)
   - Screenshot

---

**Document Version:** 2.0
**Effective Date:** 28 November 2025
**Status:** ✅ **IMPLEMENTED & READY TO USE**
