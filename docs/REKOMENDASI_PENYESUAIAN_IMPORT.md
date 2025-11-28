# Rekomendasi Penyesuaian Sistem Import
## Untuk Mendukung Laporan Pelacakan Perkara

**Tanggal Analisa:** 28 November 2025

---

## 1. HASIL ANALISA DATA vs IMPORT SYSTEM

### 📊 Distribusi Data Berdasarkan Tahapan & Format

| Tahapan Penanganan | Format Data | Jumlah | Status Pasal |
|---|---|---|---|
| **PRA PENUNTUTAN** | Format SPDP (Ada Pasal) | **80 rows** | ✅ **ADA PASAL** |
| **PENUNTUTAN** | Format PDM (Nomor Register) | **47 rows** | ❌ **TIDAK ADA PASAL** |
| **UPAYA HUKUM** | Format PDM (Nomor Register) | **13 rows** | ❌ **TIDAK ADA PASAL** |

**Kesimpulan:**
- Import **PRA PENUNTUTAN**: ✅ Sudah bagus, ada pasal
- Import **PENUNTUTAN & UPAYA HUKUM**: ❌ Tidak capture pasal

---

## 2. ANALISA SISTEM IMPORT SAAT INI

### ✅ Import PRA PENUNTUTAN - SUDAH BAGUS

**File:** `src/helpers/import_pra_penuntutan_helper.py`

**Format CSV yang Diharapkan:**
```csv
No,Tgl_Nomor,Pasal_yang_Disangkakan,Identitas_Tersangka
1,2025-01-23 SPDP/...,Pasal 303 KUHP,JUROCHMAN
```

**Hasil di Database:**
```sql
identitas_tersangka: JUROCHMAN
jenis_perkara: JUDI
tahapan_penanganan: PRA PENUNTUTAN
keterangan: SPDP: 2025-01-23 SPDP/... | Pasal: Pasal 303 KUHP
```

**Status:** ✅ **SEMPURNA** - Sudah capture pasal dengan baik!

---

### ❌ Import PENUNTUTAN - BERMASALAH

**File:** `src/helpers/import_helper.py`

**Format CSV yang Diharapkan:**
```csv
No,No_Tanggal_Register_Perkara,Jenis_Perkara,Identitas_Tersangka
1,PDM- 02/PRBAL/Eku.2/01/2025,PERKARA LAINNYA,ALDI RAMADANI
```

**Code di Line 80-134:**
```python
elif 'NO_TANGGAL_REGISTER_PERKARA' in clean_key:
    # Store original value for KETERANGAN
    no_tanggal_register = clean_value
    # ... extract date ...

# Line 132-134:
if no_tanggal_register:
    std_row['KETERANGAN'] = no_tanggal_register  # ❌ MASALAH: hanya isi nomor PDM
```

**Hasil di Database:**
```sql
identitas_tersangka: ALDI RAMADANI
jenis_perkara: PERKARA LAINNYA
tahapan_penanganan: PENUNTUTAN
keterangan: PDM- 02/PRBAL/Eku.2/01/2025  -- ❌ Bukan pasal!
```

**Masalah:**
1. ❌ Field `keterangan` diisi dengan nomor PDM, BUKAN pasal
2. ❌ Tidak ada kolom CSV untuk pasal di format PENUNTUTAN
3. ❌ Tidak ada field dedicated untuk pasal

---

### ❌ Import UPAYA HUKUM - BERMASALAH

**File:** `src/helpers/import_upaya_hukum_helper.py`

**Format CSV:**
```csv
No,Terdakwa_Terpidana,No_Tanggal_RP9,Perlawanan_...,Banding_...
1,ALDI RAMADANI,PDM- 02/PRBAL/Eku.2/01/2025,...,...
```

**Masalah:**
1. ❌ Data upaya hukum **tidak masuk ke tabel `pidum_data`** - masuk ke `upaya_hukum_data` terpisah
2. ❌ Tabel `upaya_hukum_data` punya field `jenis_perkara` tapi **TIDAK ada field pasal**
3. ❌ Untuk laporan pelacakan, perlu link antara `pidum_data` dan `upaya_hukum_data`

---

## 3. DAMPAK TERHADAP LAPORAN PELACAKAN PERKARA

### Skenario Kasus Lengkap (3 Tahapan):

Misalnya tersangka "Aci" dengan kasus judi Pasal 303:

**Tahap 1 - PRA PENUNTUTAN (dari import PRA PENUNTUTAN):**
```sql
Row 1:
- nama: Aci
- tahapan: PRA PENUNTUTAN
- keterangan: SPDP: 2025-05-02 | Pasal: Pasal 303  ✅ Ada pasal
```

**Tahap 2 - PENUNTUTAN (dari import PENUNTUTAN):**
```sql
Row 2:
- nama: Aci
- tahapan: PENUNTUTAN
- keterangan: PDM- 123/PRBAL/Enz.2/06/2025  ❌ Tidak ada pasal
```

**Tahap 3 - UPAYA HUKUM (dari import UPAYA HUKUM):**
```sql
-- Masuk ke tabel upaya_hukum_data (terpisah)
- nama: Aci
- no_tanggal_rp9: PDM- 456/PRBAL/...  ❌ Tidak ada pasal
```

### Hasil Laporan:

| No | Nama | Pasal | Jenis | Pra Penuntutan | Penuntutan | Upaya Hukum |
|---|---|---|---|---|---|---|
| 1 | Aci | **Pasal 303** ✅ | JUDI | 02/05/2025 | 10/06/2025 | 20/07/2025 |

**Catatan:**
- Pasal diambil dari tahap PRA PENUNTUTAN (karena hanya itu yang ada)
- Kalau tidak ada data PRA PENUNTUTAN → **Tidak ada pasal sama sekali** ❌

---

## 4. SOLUSI DAN REKOMENDASI

### 🎯 Solusi 1: Tambah Kolom Pasal di CSV Import PENUNTUTAN (RECOMMENDED)

**Langkah:**

#### A. Update Format CSV PENUNTUTAN

**Format Lama:**
```csv
No,No_Tanggal_Register_Perkara,Identitas_Tersangka,Jaksa_Penuntut_Umum
1,PDM- 02/PRBAL/Eku.2/01/2025,ALDI RAMADANI,Jaksa A
```

**Format Baru (Tambah Kolom):**
```csv
No,No_Tanggal_Register_Perkara,Pasal,Identitas_Tersangka,Jaksa_Penuntut_Umum
1,PDM- 02/PRBAL/Eku.2/01/2025,Pasal 303 KUHP,ALDI RAMADANI,Jaksa A
```

#### B. Update `import_helper.py`

**Tambahkan di line ~77 (setelah handle KETERANGAN):**

```python
# Line 77 - existing code untuk KETERANGAN
elif any(keyword in clean_key for keyword in ['KETERANGAN', 'DESCRIPTION', 'PASAL', 'NOTE', 'PELANGGARAN']):
    std_row['KETERANGAN'] = clean_value

# ⭐ TAMBAHKAN INI (setelah line 77):
elif 'PASAL' in clean_key and 'DISANGKAKAN' not in clean_key:
    # Field dedicated untuk pasal (bukan Pasal_yang_Disangkakan dari pra penuntutan)
    pasal_value = clean_value
    std_row['PASAL'] = pasal_value  # Store pasal terpisah
```

**Update line 132-134:**

```python
# BEFORE (line 132-134):
if no_tanggal_register:
    std_row['KETERANGAN'] = no_tanggal_register

# AFTER:
if no_tanggal_register:
    # Jika ada pasal, format seperti SPDP
    if std_row.get('PASAL'):
        std_row['KETERANGAN'] = f"{no_tanggal_register} | Pasal: {std_row['PASAL']}"
    else:
        # Fallback: hanya nomor register
        std_row['KETERANGAN'] = no_tanggal_register
```

#### C. Update Database Schema (Optional tapi Recommended)

**Tambah kolom dedicated untuk pasal:**

```sql
ALTER TABLE pidum_data
ADD COLUMN pasal VARCHAR(200) AFTER tahapan_penanganan;

ALTER TABLE pidsus_data
ADD COLUMN pasal VARCHAR(200) AFTER jenis_perkara;

ALTER TABLE upaya_hukum_data
ADD COLUMN pasal VARCHAR(200) AFTER jenis_perkara;
```

**Update insert di `mysql_database.py` line 212-218:**

```python
# BEFORE:
query = '''
    INSERT INTO pidum_data (no, periode, tanggal, jenis_perkara, tahapan_penanganan, identitas_tersangka, keterangan)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
'''
cursor.execute(query, (data['NO'], data['PERIODE'], data['TANGGAL'], data['JENIS PERKARA'],
                      data['TAHAPAN_PENANGANAN'], data.get('IDENTITAS_TERSANGKA', ''), data['KETERANGAN']))

# AFTER:
query = '''
    INSERT INTO pidum_data (no, periode, tanggal, jenis_perkara, tahapan_penanganan, pasal, identitas_tersangka, keterangan)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
'''
cursor.execute(query, (data['NO'], data['PERIODE'], data['TANGGAL'], data['JENIS PERKARA'],
                      data['TAHAPAN_PENANGANAN'], data.get('PASAL', ''), data.get('IDENTITAS_TERSANGKA', ''), data['KETERANGAN']))
```

---

### 🎯 Solusi 2: Extract Pasal dari Data PRA PENUNTUTAN (Workaround)

Jika tidak bisa update CSV:

**Strategi:**
- Untuk laporan, ambil pasal dari row PRA PENUNTUTAN yang sama tersangka + jenis perkara
- Asumsi: 1 tersangka + 1 jenis perkara = pasal yang sama di semua tahapan

**Query:**
```sql
SELECT
    identitas_tersangka,
    jenis_perkara,
    -- Ambil pasal dari tahapan PRA PENUNTUTAN
    MAX(CASE WHEN tahapan_penanganan = 'PRA PENUNTUTAN' AND keterangan LIKE 'SPDP:%'
        THEN TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(keterangan, 'Pasal: ', -1), '|', 1))
        ELSE NULL END) as pasal,
    -- Tanggal per tahapan
    MAX(CASE WHEN tahapan_penanganan = 'PRA PENUNTUTAN'
        THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as pra_penuntutan,
    MAX(CASE WHEN tahapan_penanganan = 'PENUNTUTAN'
        THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as penuntutan,
    MAX(CASE WHEN tahapan_penanganan = 'UPAYA HUKUM'
        THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as upaya_hukum
FROM pidum_data
GROUP BY identitas_tersangka, jenis_perkara
```

**Kelemahan:**
- ❌ Jika data langsung masuk PENUNTUTAN tanpa PRA PENUNTUTAN → tidak ada pasal
- ❌ Asumsi pasal sama di semua tahapan bisa salah

---

### 🎯 Solusi 3: Manual Input Pasal untuk Data Lama

**Untuk data yang sudah ada:**

```sql
-- Update manual pasal untuk data PDM yang sudah masuk
UPDATE pidum_data
SET pasal = 'Pasal XXX'  -- User input manual
WHERE id = YYY;
```

**Untuk data baru:**
- Gunakan Solusi 1 (update import system)

---

## 5. REKOMENDASI IMPLEMENTASI

### Fase 1: Quick Fix (1-2 jam) - Untuk Laporan Sekarang

**Action:**
1. ✅ Implementasi **Solusi 2** (extract dari PRA PENUNTUTAN)
2. ✅ Laporan akan show pasal jika ada data PRA PENUNTUTAN
3. ✅ Display dash (`-`) jika tidak ada

**Keuntungan:**
- Cepat, no schema changes
- No need to re-import data
- Laporan bisa jalan sekarang

**Kekurangan:**
- 47 rows PENUNTUTAN tanpa PRA PENUNTUTAN → tidak ada pasal
- 13 rows UPAYA HUKUM tanpa PRA PENUNTUTAN → tidak ada pasal

---

### Fase 2: Proper Solution (3-4 jam) - Untuk Long Term

**Action:**
1. ✅ Tambah kolom `pasal` di database (ALTER TABLE)
2. ✅ Update `import_helper.py` untuk support kolom Pasal di CSV
3. ✅ Update form input manual untuk tambah field pasal
4. ✅ Migrate data existing:
   - Extract pasal dari SPDP format (80 rows)
   - Manual input untuk 60 rows sisanya (optional)

**Keuntungan:**
- Data terstruktur dengan baik
- Semua tahapan bisa punya pasal
- Maintainable untuk long-term
- Bisa filter/sort by pasal

**Kekurangan:**
- Perlu update CSV template untuk user
- Perlu re-import data atau manual input untuk data lama

---

### Fase 3: Update CSV Template & Training (1 jam)

**Action:**
1. ✅ Buat CSV template baru dengan kolom Pasal
2. ✅ Update dokumentasi import
3. ✅ Training user untuk format baru

**Template CSV PENUNTUTAN Baru:**
```csv
No,No_Tanggal_Register_Perkara,Pasal,Identitas_Tersangka,Jenis_Perkara,Jaksa_Penuntut_Umum
1,PDM- 02/PRBAL/Eku.2/01/2025,Pasal 303 KUHP,ALDI RAMADANI,JUDI,Jaksa Ahmad
```

---

## 6. CHECKLIST PENYESUAIAN

### Untuk Mendukung Laporan Pelacakan Perkara:

#### Database Schema:
- [ ] Tambah kolom `pasal` di tabel `pidum_data`
- [ ] Tambah kolom `pasal` di tabel `pidsus_data`
- [ ] Tambah kolom `pasal` di tabel `upaya_hukum_data` (optional)

#### Import System:
- [ ] Update `import_helper.py` untuk capture kolom Pasal
- [ ] Update `import_helper.py` untuk format keterangan dengan pasal
- [ ] Update database insert query untuk include pasal
- [ ] Test import dengan data baru

#### CSV Template:
- [ ] Update template CSV PENUNTUTAN dengan kolom Pasal
- [ ] Update template CSV UPAYA HUKUM dengan kolom Pasal (optional)
- [ ] Dokumentasi format CSV baru

#### Data Migration:
- [ ] Extract pasal dari 80 rows format SPDP
- [ ] Update database dengan pasal yang di-extract
- [ ] Manual input pasal untuk 60 rows format PDM (optional)

#### Form Input Manual:
- [ ] Tambah field "Pasal" di form input PIDUM
- [ ] Tambah field "Pasal" di form input PIDSUS
- [ ] Validasi field pasal (optional/required)

---

## 7. ESTIMASI EFFORT

| Fase | Task | Estimasi Waktu | Priority |
|---|---|---|---|
| **Fase 1: Quick Fix** | Implementasi laporan dengan extract dari PRA PENUNTUTAN | 1-2 jam | P0 (Urgent) |
| **Fase 2: Proper Solution** | Database schema + import update | 3-4 jam | P1 (High) |
| | Data migration (extract dari SPDP) | 1 jam | P1 (High) |
| | Manual input pasal (60 rows) | 2-3 jam | P2 (Medium) |
| | Update form input | 1 jam | P1 (High) |
| **Fase 3: Documentation** | Update CSV template + docs | 1 jam | P1 (High) |
| | User training | 30 menit | P2 (Medium) |
| **TOTAL** | | **9.5 - 12.5 jam** | |

---

## 8. REKOMENDASI FINAL

### Untuk Implementasi Sekarang:

**Opsi A: Cepat Tapi Tidak Sempurna (2-3 jam)**
1. ✅ Implementasi laporan dengan **Solusi 2** (extract dari PRA PENUNTUTAN)
2. ✅ Accept bahwa tidak semua data punya pasal
3. ✅ Plan untuk Fase 2 nanti

**Opsi B: Sempurna Tapi Lebih Lama (6-8 jam)**
1. ✅ Langsung implementasi **Fase 1 + Fase 2**
2. ✅ Tambah kolom pasal di database
3. ✅ Update import system
4. ✅ Migrate data existing
5. ✅ Baru implementasi laporan

**Opsi C: Hybrid (Recommended) - 4-5 jam**
1. ✅ **Hari ini:** Implementasi laporan dengan Solusi 2 (2-3 jam)
2. ✅ **Paralel/Next:** Implementasi Fase 2 (schema + import) (3-4 jam)
3. ✅ **Gradually:** Migrate data dan manual input (ongoing)

### Rekomendasi Saya: **Opsi C (Hybrid)**

**Alasan:**
- User bisa lihat laporan hari ini (walau belum sempurna)
- Tidak blocking progress
- Proper solution tetap dikerjakan
- Fleksibel untuk manual input data lama secara bertahap

---

## 9. PERTANYAAN UNTUK USER

Sebelum lanjut implementasi:

1. **Apakah bisa update format CSV untuk import PENUNTUTAN ke depannya?**
   - Ya → Implementasi Solusi 1 (recommended)
   - Tidak → Tetap pakai Solusi 2 (workaround)

2. **Apakah perlu pasal untuk SEMUA data (termasuk 60 rows yang lama)?**
   - Ya → Perlu manual input atau cari data source asli
   - Tidak → Accept dash untuk data tanpa pasal

3. **Kapan target laporan harus jadi?**
   - Hari ini → Opsi A (Quick Fix)
   - Minggu ini → Opsi C (Hybrid) - recommended
   - Tidak urgent → Opsi B (Proper Solution)

---

**Document Created:** 28 November 2025
**Status:** Rekomendasi siap untuk review dan approval
**Next Step:** User decision → Implementasi sesuai pilihan
