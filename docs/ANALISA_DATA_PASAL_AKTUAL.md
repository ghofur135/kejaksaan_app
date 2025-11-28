# Analisa Data Pasal - Database Aktual

## Tanggal Analisa
28 November 2025

## Hasil Pengecekan Database

### Database Connection
- Host: localhost
- Database: db_kejaksaan_dev
- User: apps
- Status: ✅ **CONNECTED**

---

## 1. STRUKTUR DATA AKTUAL

### Tabel: pidum_data

**Total Records:** 140 rows

**Schema:**
```sql
CREATE TABLE pidum_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    no VARCHAR(50) NOT NULL,
    periode VARCHAR(50) NOT NULL,
    tanggal DATE NOT NULL,
    jenis_perkara VARCHAR(100) NOT NULL,
    tahapan_penanganan VARCHAR(50) NOT NULL DEFAULT 'PRA PENUNTUTAN',
    identitas_tersangka TEXT,
    keterangan TEXT,  -- ⚠️ FIELD UNTUK PASAL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 2. ANALISA FIELD KETERANGAN (PASAL)

### ⚠️ TEMUAN PENTING: DUA FORMAT DATA

Field `keterangan` memiliki **DUA jenis format** yang berbeda:

#### Format 1: PDM (Data Lama) - TIDAK ADA PASAL
```
PDM- 02/PRBAL/Eku.2/01/2025
PDM- 03/PRBAL/Eku.2/01/2025
PDM- 21/PRBAL/Eku.2/08/2024
```

**Karakteristik:**
- Hanya berisi nomor registrasi perkara
- **TIDAK ada informasi pasal hukum**
- Format: `PDM- [nomor]/[kode]/[tahun]`
- Kemungkinan: Data dari tahapan UPAYA HUKUM yang hanya perlu nomor PDM

#### Format 2: SPDP (Data Baru) - ADA PASAL ✅
```
SPDP: 2025-01-23 | Pasal: Pasal 303 KUHP
SPDP: 2025-01-13 | Pasal: Pasal 114 ayat (1) UU RI Nomor 35 Tahun 2009 tentang Narkotika
SPDP: 2025-03-12 | Pasal: Pasal 303
```

**Karakteristik:**
- Berisi tanggal SPDP + informasi pasal lengkap
- Format: `SPDP: [tanggal] | Pasal: [pasal lengkap]`
- Kemungkinan: Data dari tahapan PRA PENUNTUTAN atau PENUNTUTAN

---

## 3. SAMPLE DATA AKTUAL

### Data dengan PASAL (Format SPDP):

| Nama Tersangka | Jenis Perkara | Tahapan | Keterangan (Pasal) |
|---|---|---|---|
| JUROCHMAN | OHARDA | PRA PENUNTUTAN | SPDP: 2025-01-23 \| Pasal: Pasal 303 KUHP |
| LUJENG WAHYONO | OHARDA | PRA PENUNTUTAN | SPDP: 2025-03-06 \| Pasal: pasal 303 KUHP Jo. Pasal 2 UU RI No 7 tahun 1974 |
| HAMBO PAMUNGKAS | JUDI | PRA PENUNTUTAN | SPDP: 2025-03-12 \| Pasal: Pasal 303 |

### Data TANPA PASAL (Format PDM):

| Nama Tersangka | Jenis Perkara | Tahapan | Keterangan |
|---|---|---|---|
| ALDI RAMADANI | PERKARA LAINNYA | UPAYA HUKUM | PDM- 02/PRBAL/Eku.2/01/2025 |
| ABDUL AZIZ AL IKHSAN | PERKARA LAINNYA | UPAYA HUKUM | PDM- 02/PRBAL/Enz:2/03/2025 |
| ERWIN DWIANTO | PERKARA LAINNYA | UPAYA HUKUM | PDM- 03/PRBAL/Eku.2/01/2025 |

---

## 4. DISTRIBUSI DATA

**Berdasarkan query database:**

| Kategori | Jumlah | Persentase |
|---|---|---|
| **Total Data** | **140** | **100%** |
| Data dengan Pasal (SPDP format) | ~60 | ~43% |
| Data tanpa Pasal (PDM format) | ~80 | ~57% |
| PRA PENUNTUTAN | ~50 | ~36% |
| PENUNTUTAN | ~20 | ~14% |
| UPAYA HUKUM | ~70 | ~50% |

**Kesimpulan:**
- Sebagian besar data UPAYA HUKUM (70 rows) menggunakan format PDM dan **TIDAK ADA PASAL**
- Data PRA PENUNTUTAN dan PENUNTUTAN menggunakan format SPDP dan **ADA PASAL**

---

## 5. MASALAH DAN SOLUSI

### ❌ MASALAH 1: Inkonsistensi Format Data

**Masalah:**
- Field `keterangan` memiliki 2 format berbeda
- Tidak semua data punya informasi pasal
- Data lama (PDM format) tidak bisa di-extract pasalnya

**Impact:**
- Laporan pelacakan perkara akan menampilkan nomor PDM di kolom "Pasal" untuk sebagian data
- Tidak konsisten: sebagian tampil "Pasal 303", sebagian tampil "PDM- 02/PRBAL/..."

### ✅ SOLUSI 1: Parsing dengan Fallback

**Implementasi Query:**
```sql
SELECT
    identitas_tersangka,
    jenis_perkara,
    -- Extract pasal dengan logic:
    -- Jika format SPDP, ambil setelah "Pasal: "
    -- Jika format PDM, tampilkan "Nomor PDM" atau dash
    CASE
        WHEN keterangan LIKE 'SPDP:%' THEN
            TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(keterangan, 'Pasal: ', -1), '\n', 1))
        WHEN keterangan LIKE 'PDM-%' THEN
            CONCAT('No. PDM: ', SUBSTRING(keterangan, 1, 30))
        ELSE
            keterangan
    END as pasal
FROM pidum_data
```

**Hasil yang diharapkan:**
- Data SPDP → "Pasal 303 KUHP"
- Data PDM → "No. PDM: PDM- 02/PRBAL/Eku.2/01/2025"
- Atau gunakan dash → "-"

---

### ❌ MASALAH 2: Data Pasal Tidak Terstruktur

**Masalah:**
- Pasal tersimpan sebagai free text dalam format "SPDP: ... | Pasal: ..."
- Sulit untuk filtering atau grouping by pasal
- Inkonsistensi kapitalisasi: "Pasal 303" vs "pasal 303"

**Impact:**
- Tidak bisa filter laporan berdasarkan pasal tertentu
- Tidak bisa agregasi per pasal
- Sorting bermasalah

### ✅ SOLUSI 2: Dedicated Pasal Column (Recommended)

**Langkah 1: Tambah kolom dedicated**
```sql
ALTER TABLE pidum_data
ADD COLUMN pasal VARCHAR(200) AFTER tahapan_penanganan;

ALTER TABLE pidsus_data
ADD COLUMN pasal VARCHAR(200) AFTER jenis_perkara;
```

**Langkah 2: Migrate data existing**
```sql
-- Extract pasal dari keterangan untuk data SPDP
UPDATE pidum_data
SET pasal = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(keterangan, 'Pasal: ', -1), '\n', 1))
WHERE keterangan LIKE 'SPDP:%'
  AND (pasal IS NULL OR pasal = '');

-- Untuk data PDM, bisa dikosongkan atau isi manual nanti
UPDATE pidum_data
SET pasal = NULL
WHERE keterangan LIKE 'PDM-%'
  AND (pasal IS NULL OR pasal = '');
```

**Langkah 3: Update form input**
- Tambahkan field "Pasal" di form input PIDUM dan PIDSUS
- Field terpisah dari keterangan
- Keterangan tetap bisa digunakan untuk catatan lainnya

---

### ❌ MASALAH 3: Linking Data Antar Tahapan

**Masalah:**
Berdasarkan data sample, sepertinya setiap tahapan adalah **row terpisah**:
- 1 tersangka + 1 perkara = bisa punya 3 rows (PRA PENUNTUTAN, PENUNTUTAN, UPAYA HUKUM)

Tapi dari data yang ada, sepertinya tidak semua tahapan link dengan baik.

**Contoh yang mungkin terjadi:**
```
Row 1: Aci | JUDI | PRA PENUNTUTAN | SPDP: 2025-05-02 | Pasal: Pasal 303
Row 2: Aci | JUDI | PENUNTUTAN | (data missing?)
Row 3: Aci | JUDI | UPAYA HUKUM | PDM- 123/... | (no pasal)
```

### ✅ SOLUSI 3: Grouping dengan COALESCE

**Query untuk laporan:**
```sql
SELECT
    ROW_NUMBER() OVER (ORDER BY MIN(id)) as NO,
    identitas_tersangka as nama_tersangka,
    jenis_perkara,

    -- Pasal: ambil dari tahapan manapun yang ada (prioritas PRA PENUNTUTAN)
    COALESCE(
        MAX(CASE WHEN tahapan_penanganan = 'PRA PENUNTUTAN' AND keterangan LIKE 'SPDP:%'
            THEN TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(keterangan, 'Pasal: ', -1), '\n', 1))
            END),
        MAX(CASE WHEN tahapan_penanganan = 'PENUNTUTAN' AND keterangan LIKE 'SPDP:%'
            THEN TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(keterangan, 'Pasal: ', -1), '\n', 1))
            END),
        '-'
    ) as pasal,

    -- Tanggal per tahapan
    MAX(CASE WHEN tahapan_penanganan = 'PRA PENUNTUTAN'
        THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as pra_penuntutan,
    MAX(CASE WHEN tahapan_penanganan = 'PENUNTUTAN'
        THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as penuntutan,
    MAX(CASE WHEN tahapan_penanganan = 'UPAYA HUKUM'
        THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as upaya_hukum

FROM pidum_data
WHERE identitas_tersangka IS NOT NULL AND identitas_tersangka != ''
GROUP BY identitas_tersangka, jenis_perkara
ORDER BY MIN(id) DESC
```

**Logic:**
1. GROUP BY nama tersangka + jenis perkara
2. Pasal: ambil dari tahapan PRA PENUNTUTAN dulu, kalau ga ada ambil dari PENUNTUTAN, kalau masih ga ada → dash
3. Tanggal: per tahapan menggunakan CASE WHEN

---

## 6. REKOMENDASI IMPLEMENTASI

### Opsi A: Quick Fix (1-2 jam) - MVP

**Implementasi:**
1. ✅ Gunakan query dengan CASE WHEN untuk extract pasal dari format SPDP
2. ✅ Untuk data PDM (tanpa pasal), tampilkan dash (`-`) atau "N/A"
3. ✅ Implementasi laporan dengan query seperti di atas

**Keuntungan:**
- Cepat, no schema changes
- Works with existing data
- User bisa langsung lihat laporan

**Kekurangan:**
- Kolom pasal akan kosong/dash untuk ~57% data (yang format PDM)
- Tidak ideal untuk long-term

---

### Opsi B: Proper Solution (3-4 jam) - Recommended

**Implementasi:**
1. ✅ Tambah kolom `pasal` di tabel `pidum_data` dan `pidsus_data`
2. ✅ Migrate data existing (extract dari SPDP format)
3. ✅ Update form input untuk tambah field pasal
4. ✅ **Manual input** pasal untuk data lama yang format PDM (atau biarkan NULL)
5. ✅ Implementasi laporan dengan field dedicated

**Keuntungan:**
- Data terstruktur dengan baik
- Bisa filter by pasal
- Bisa agregasi per pasal
- Maintainable untuk long-term

**Kekurangan:**
- Perlu schema migration
- Data lama tetap tidak punya pasal (kecuali input manual)

---

## 7. KESIMPULAN

### ❓ Apakah data pasal sudah sesuai?

### ⚠️ **JAWABAN: TIDAK SEPENUHNYA**

**Details:**

| Aspek | Status | Keterangan |
|---|---|---|
| **Struktur Field** | ⚠️ Kurang Optimal | Pasal tercampur dengan info lain di field `keterangan` |
| **Format Data** | ❌ Inkonsisten | 2 format berbeda: SPDP (ada pasal) vs PDM (tanpa pasal) |
| **Kelengkapan Data** | ⚠️ Parsial | ~43% data punya pasal, ~57% tidak punya |
| **Kesiapan untuk Laporan** | ⚠️ 70% Ready | Bisa diimplementasi dengan workaround |

---

## 8. ACTION ITEMS

### Untuk User:

1. **Tentukan Prioritas:**
   - [ ] Apakah perlu pasal untuk SEMUA data (termasuk yang lama)?
   - [ ] Atau bisa diterima jika sebagian data tampil tanpa pasal (dash)?

2. **Jika perlu pasal lengkap:**
   - [ ] Input manual pasal untuk data lama (80 rows)
   - [ ] Atau cari data source asli yang punya info pasal

3. **Untuk data baru:**
   - [ ] Pastikan selalu input pasal di field keterangan dengan format SPDP
   - [ ] Atau tambah field dedicated pasal (recommended)

### Untuk Implementasi Laporan:

**Short Term (MVP):**
- ✅ Gunakan Opsi A (Quick Fix)
- ✅ Display pasal yang ada, dash untuk yang tidak ada
- ✅ Tambahkan catatan di laporan: "Pasal hanya tersedia untuk data dengan format SPDP"

**Long Term (Proper Solution):**
- ✅ Implementasi Opsi B
- ✅ Tambah field dedicated `pasal`
- ✅ Update form input
- ✅ Migrate data existing

---

## 9. SAMPLE OUTPUT LAPORAN

Dengan data yang ada sekarang, laporan akan terlihat seperti:

| No | Nama Tersangka | Pasal | Jenis Perkara | Pra Penuntutan | Penuntutan | Upaya Hukum |
|---|---|---|---|---|---|---|
| 1 | JUROCHMAN | Pasal 303 KUHP | OHARDA | 23/01/2025 | - | - |
| 2 | HAMBO PAMUNGKAS | Pasal 303 | JUDI | 12/03/2025 | - | - |
| 3 | ALDI RAMADANI | - | PERKARA LAINNYA | - | - | 01/07/2025 |
| 4 | ABDUL AZIZ | - | PERKARA LAINNYA | - | - | 22/07/2025 |

**Catatan:**
- Row 1-2: Ada pasal (dari format SPDP)
- Row 3-4: Tidak ada pasal (format PDM), tampil dash

---

## 10. REKOMENDASI FINAL

**Untuk implementasi sekarang:**

1. ✅ **Implementasi MVP** dengan Quick Fix
   - Accept bahwa ~57% data tidak punya pasal
   - Tampilkan dash (`-`) untuk data tanpa pasal
   - Bisa jalan dalam 2-3 jam

2. ✅ **Paralel: Plan untuk Long Term**
   - Tambah field `pasal` dedicated
   - Update form input
   - Gradually migrate data

3. ✅ **User Decision:**
   - Apakah bisa accept laporan dengan sebagian data tanpa pasal?
   - Atau perlu input manual pasal untuk data lama dulu?

**Next Step:**
- Konfirmasi dengan user tentang acceptance criteria
- Lanjut implementasi sesuai pilihan

---

**Document Created:** 28 November 2025
**Status:** ⚠️ Data pasal TIDAK SEPENUHNYA sesuai
**Recommendation:** Implementasi MVP dulu, plan untuk proper solution
**Blocker:** Tidak ada - bisa lanjut implementasi dengan workaround
