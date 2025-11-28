# Analisa Permintaan: Laporan Pelacakan Perkara Baru

## Tanggal Analisa
28 November 2025

## Gambar Referensi
Gambar menunjukkan format tabel laporan baru dengan kolom-kolom:

| No. | Nama Tersangka | Pasal | Jenis Perkara | Pra Penuntutan | Penuntutan | Upaya Hukum |
|-----|---------------|-------|---------------|----------------|------------|-------------|
| 1   | Aci           | 303   | Judi          | 02/05/2025     | 10/06/2025 | -           |

**Catatan di atas tabel:** "Pada insan adhyaksa" (mengindikasikan laporan untuk kejaksaan)

---

## 1. KESIMPULAN UTAMA

### ✅ SANGAT MEMUNGKINKAN

Projek kejaksaan_app **SANGAT MEMUNGKINKAN** untuk membuat laporan baru sesuai format yang diminta. Infrastruktur yang ada sudah sangat mendukung:

**Tingkat Kelayakan: 95/100**

**Alasan:**
1. Data yang dibutuhkan sudah tersedia di database
2. Pattern laporan sudah matang dan terbukti
3. Struktur kode modular dan mudah diperluas
4. Template sistem sudah ada dan dapat dikustomisasi
5. Export features sudah tersedia (Excel, Word)

---

## 2. ANALISA KEBUTUHAN DATA

### Data yang Dibutuhkan dari Gambar

| Kolom yang Diminta | Ketersediaan di Database | Lokasi Data | Status |
|-------------------|--------------------------|-------------|---------|
| **No.** (Nomor urut) | ✅ Tersedia | Auto-generated | Ready |
| **Nama Tersangka** | ✅ Tersedia | `pidum_data.identitas_tersangka` (PIDUM)<br>`pidsus_data.nama_tersangka` (PIDSUS) | Ready |
| **Pasal** | ✅ Tersedia | `pidum_data.keterangan`<br>`pidsus_data.keterangan` | Ready (parsing diperlukan) |
| **Jenis Perkara** | ✅ Tersedia | `pidum_data.jenis_perkara`<br>`pidsus_data.jenis_perkara` | Ready |
| **Pra Penuntutan** | ✅ Tersedia | Filter `tahapan_penanganan = 'PRA PENUNTUTAN'` + `tanggal` | Ready |
| **Penuntutan** | ✅ Tersedia | Filter `tahapan_penanganan = 'PENUNTUTAN'` + `tanggal` | Ready |
| **Upaya Hukum** | ✅ Tersedia | `upaya_hukum_data` (seluruh tabel)<br>Filter `tahapan_penanganan = 'UPAYA HUKUM'` | Ready |

### Catatan Penting:

1. **Relasi Data Antar Tahapan:**
   - Saat ini, setiap tahapan (Pra Penuntutan, Penuntutan, Upaya Hukum) disimpan sebagai row terpisah
   - Untuk laporan ini, perlu JOIN atau aggregasi berdasarkan identitas tersangka/nomor perkara

2. **Field Pasal:**
   - Tersimpan di field `keterangan` bersama informasi lain
   - Perlu ekstraksi atau buat field dedicated `pasal` (rekomendasi)

3. **Nomor Register/Perkara:**
   - Field `no` di semua tabel untuk tracking case number
   - Dapat digunakan sebagai primary key untuk menggabungkan tahapan

---

## 3. INFRASTRUKTUR YANG SUDAH ADA

### A. Database Layer (models/mysql_database.py)

**Fungsi-fungsi yang Relevan:**
```python
# Pattern yang sudah ada:
def get_pidum_report_data(self, bulan=None, tahun=None, start_date=None, end_date=None)
def get_pidsus_report_data(self, bulan=None, tahun=None, start_date=None, end_date=None)
def get_upaya_hukum_report_data(self, bulan=None, tahun=None)

# Yang perlu ditambahkan:
def get_pelacakan_perkara_report_data(self, bulan=None, tahun=None, tersangka=None)
```

**Struktur Tabel yang Relevan:**
- `pidum_data`: 12+ kolom termasuk identitas_tersangka, tahapan_penanganan, tanggal
- `pidsus_data`: 10+ kolom termasuk nama_tersangka, penyidikan, penuntutan
- `upaya_hukum_data`: 30+ kolom untuk tracking legal remedy

### B. Route Handler (app_with_db.py)

**Routes yang Sudah Ada sebagai Referensi:**
```python
@app.route('/laporan_pidum')             # Line ~1800
@app.route('/laporan_pidum_bulanan')     # Line ~1900
@app.route('/laporan_pidum_new')         # Line ~2000
@app.route('/export_pidum_excel')        # Line ~2300
@app.route('/export_pidum_new_word')     # Line ~2500
```

**Route Baru yang Perlu Dibuat:**
```python
@app.route('/laporan_pelacakan_perkara')
@app.route('/export_pelacakan_perkara_excel')
@app.route('/export_pelacakan_perkara_word')  # Optional
```

### C. Template System

**Template yang Sudah Ada:**
- `templates/laporan_pidum.html` - Bootstrap table dengan filter
- `templates/laporan_pidum_new.html` - Enhanced format dengan totals
- `templates/view_pidum.html` - Table dengan search functionality

**Template Baru yang Perlu Dibuat:**
- `templates/laporan_pelacakan_perkara.html` - Format sesuai gambar

### D. Helper Functions

**Import Helpers yang Relevan:**
```python
# src/helpers/import_helper.py
- parse_csv()
- extract_date()
- standardize_jenis_perkara()

# src/helpers/import_pra_penuntutan_helper.py
- import_pra_penuntutan_data()
```

---

## 4. STRATEGI IMPLEMENTASI

### Opsi A: Unified Report (Rekomendasi)

**Konsep:** Buat laporan yang menggabungkan semua tahapan untuk setiap tersangka dalam satu row.

**Kelebihan:**
- Sesuai dengan format gambar (1 tersangka = 1 row)
- Mudah dibaca dan dipahami
- Timeline progression jelas

**Kekurangan:**
- Perlu complex JOIN query
- Harus handle missing tahapan (NULL values)

**Query Strategy:**
```sql
SELECT
    ROW_NUMBER() OVER (ORDER BY p1.created_at) as no,
    COALESCE(p1.identitas_tersangka, p2.identitas_tersangka, '') as nama_tersangka,
    COALESCE(p1.keterangan, p2.keterangan, '') as pasal,
    COALESCE(p1.jenis_perkara, p2.jenis_perkara, '') as jenis_perkara,
    p1.tanggal as pra_penuntutan,
    p2.tanggal as penuntutan,
    uh.created_at as upaya_hukum
FROM
    (SELECT * FROM pidum_data WHERE tahapan_penanganan = 'PRA PENUNTUTAN') p1
LEFT JOIN
    (SELECT * FROM pidum_data WHERE tahapan_penanganan = 'PENUNTUTAN') p2
    ON p1.identitas_tersangka = p2.identitas_tersangka
LEFT JOIN
    upaya_hukum_data uh
    ON p1.identitas_tersangka = uh.terdakwa_terpidana
WHERE
    [filter conditions]
ORDER BY p1.created_at DESC
```

### Opsi B: Create Materialized View/Table

**Konsep:** Buat tabel baru `pelacakan_perkara` yang consolidates data.

**Kelebihan:**
- Performance lebih baik
- Query lebih simple
- Dapat di-index untuk search cepat

**Kekurangan:**
- Perlu trigger/sync mechanism
- Storage overhead
- Kompleksitas maintenance

**Table Schema:**
```sql
CREATE TABLE pelacakan_perkara (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomor_register VARCHAR(50),
    nama_tersangka TEXT,
    pasal VARCHAR(200),
    jenis_perkara VARCHAR(100),
    tanggal_pra_penuntutan DATE,
    tanggal_penuntutan DATE,
    tanggal_upaya_hukum DATE,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nama (nama_tersangka(100)),
    INDEX idx_register (nomor_register)
);
```

### Opsi C: Dynamic Aggregation (Tercepat untuk MVP)

**Konsep:** Aggregate on-the-fly dengan Python pandas after query.

**Kelebihan:**
- No database schema changes
- Flexible filtering and grouping
- Reuse existing data

**Kekurangan:**
- Slower for large datasets (>10k rows)
- More memory usage

**Implementation:**
```python
def get_pelacakan_perkara_report_data(self, bulan=None, tahun=None):
    # 1. Query all relevant data
    pidum_data = self.get_all_pidum_data(filters)
    upaya_hukum_data = self.get_all_upaya_hukum_data(filters)

    # 2. Use pandas to pivot and aggregate
    import pandas as pd
    df = pd.DataFrame(pidum_data)

    # 3. Pivot tahapan into columns
    pivot = df.pivot_table(
        index=['identitas_tersangka', 'jenis_perkara', 'keterangan'],
        columns='tahapan_penanganan',
        values='tanggal',
        aggfunc='first'
    ).reset_index()

    # 4. Merge with upaya_hukum
    # ... join logic

    # 5. Return formatted data
    return pivot.to_dict('records')
```

---

## 5. REKOMENDASI IMPLEMENTASI

### Tahap 1: MVP (Minimum Viable Product) - 2-3 Jam Kerja

**Target:** Laporan dasar yang berfungsi dengan data yang ada.

**Tasks:**
1. ✅ Buat method `get_pelacakan_perkara_report_data()` di `mysql_database.py`
   - Menggunakan Opsi C (Dynamic Aggregation)
   - Support filter bulan/tahun

2. ✅ Buat route `/laporan_pelacakan_perkara` di `app_with_db.py`
   - Copy dari `/laporan_pidum` dan modifikasi
   - Login required decorator

3. ✅ Buat template `laporan_pelacakan_perkara.html`
   - Copy dari `laporan_pidum.html`
   - Adjust kolom sesuai gambar
   - Bootstrap styling

4. ✅ Test dengan data dummy
   - Minimal 5-10 rows test data

**Deliverables:**
- Laporan dapat diakses via browser
- Filter bulan/tahun berfungsi
- Data tampil sesuai format gambar

### Tahap 2: Enhanced Features - 2-3 Jam Kerja

**Target:** Fitur export dan filtering lanjutan.

**Tasks:**
1. ✅ Export to Excel
   - Route `/export_pelacakan_perkara_excel`
   - Format sesuai template gambar
   - Include styling (headers, borders)

2. ✅ Search functionality
   - Search by nama tersangka
   - Filter by jenis perkara
   - Date range selection

3. ✅ Pagination
   - 50 rows per page
   - Navigation controls

4. ✅ Totals row
   - Total count per jenis perkara
   - Summary statistics

### Tahap 3: Optimization (Optional) - 3-4 Jam Kerja

**Target:** Performance dan data quality improvements.

**Tasks:**
1. ✅ Database optimization
   - Add index pada nama_tersangka
   - Add index pada tanggal
   - Query profiling

2. ✅ Data quality
   - Buat field dedicated `pasal` (migrate dari keterangan)
   - Normalisasi nama tersangka
   - Case linking mechanism

3. ✅ Advanced features
   - Chart visualization (progression timeline)
   - Print-friendly view
   - Word export

---

## 6. PERKIRAAN EFFORT

| Tahap | Komponen | Estimasi Waktu | Kompleksitas |
|-------|----------|----------------|--------------|
| **Tahap 1: MVP** | Database method | 45 menit | Medium |
| | Route handler | 30 menit | Low |
| | Template HTML | 45 menit | Low |
| | Testing & debugging | 30 menit | Medium |
| | **Subtotal Tahap 1** | **2.5 jam** | |
| **Tahap 2: Enhanced** | Excel export | 1 jam | Medium |
| | Search & filter | 45 menit | Medium |
| | Pagination | 30 menit | Low |
| | Styling & polish | 45 menit | Low |
| | **Subtotal Tahap 2** | **3 jam** | |
| **Tahap 3: Optional** | DB optimization | 1.5 jam | High |
| | Data migration | 1 jam | Medium |
| | Advanced features | 1.5 jam | Medium |
| | **Subtotal Tahap 3** | **4 jam** | |
| **TOTAL** | | **9.5 jam** | |

**Rekomendasi:** Mulai dengan Tahap 1 (MVP) untuk validasi konsep, kemudian lanjut ke Tahap 2 setelah mendapat feedback.

---

## 7. RISIKO DAN MITIGASI

### Risiko Teknis

| Risiko | Dampak | Probabilitas | Mitigasi |
|--------|---------|--------------|----------|
| **Data tersangka tidak konsisten** | Medium | High | Normalisasi dan deduplikasi saat query |
| **Tahapan tidak lengkap (NULL values)** | Low | High | Handle NULL dengan dash (-) seperti di gambar |
| **Performance dengan data besar** | High | Medium | Implementasi pagination + caching |
| **Relasi antar tahapan tidak jelas** | Medium | Medium | Gunakan nomor register sebagai key |
| **Field pasal perlu parsing** | Low | High | Regex extraction atau dedicated field |

### Risiko Data Quality

1. **Nama tersangka tidak standar:**
   - Mitigasi: Buat helper function `normalize_name()`
   - Implementasi fuzzy matching untuk linking

2. **Missing timestamps:**
   - Mitigasi: Default ke `created_at` jika `tanggal` NULL
   - Warning message di laporan

3. **Duplicate entries:**
   - Mitigasi: DISTINCT query atau deduplication logic
   - Show count di UI

---

## 8. CONTOH KODE IMPLEMENTASI

### A. Database Method (mysql_database.py)

```python
def get_pelacakan_perkara_report_data(self, bulan=None, tahun=None,
                                      start_date=None, end_date=None,
                                      jenis_perkara=None, tersangka=None):
    """
    Generate laporan pelacakan perkara dengan format:
    No | Nama Tersangka | Pasal | Jenis Perkara | Pra Penuntutan | Penuntutan | Upaya Hukum
    """
    with self.get_connection() as conn:
        cursor = conn.cursor(dictionary=True)

        # Build WHERE conditions
        where_conditions = ["1=1"]  # Base condition
        params = []

        if bulan and tahun:
            where_conditions.append("MONTH(tanggal) = %s AND YEAR(tanggal) = %s")
            params.extend([bulan, tahun])
        elif tahun:
            where_conditions.append("YEAR(tanggal) = %s")
            params.append(tahun)

        if start_date and end_date:
            where_conditions.append("tanggal BETWEEN %s AND %s")
            params.extend([start_date, end_date])

        if jenis_perkara:
            where_conditions.append("jenis_perkara = %s")
            params.append(jenis_perkara)

        if tersangka:
            where_conditions.append("identitas_tersangka LIKE %s")
            params.append(f"%{tersangka}%")

        where_clause = " AND ".join(where_conditions)

        # Main query - aggregate by tersangka
        query = f"""
            SELECT
                identitas_tersangka as nama_tersangka,
                jenis_perkara,
                keterangan as pasal,
                MAX(CASE WHEN tahapan_penanganan = 'PRA PENUNTUTAN'
                    THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as pra_penuntutan,
                MAX(CASE WHEN tahapan_penanganan = 'PENUNTUTAN'
                    THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as penuntutan,
                MAX(CASE WHEN tahapan_penanganan = 'UPAYA HUKUM'
                    THEN DATE_FORMAT(tanggal, '%d/%m/%Y') END) as upaya_hukum
            FROM pidum_data
            WHERE {where_clause}
            GROUP BY identitas_tersangka, jenis_perkara, keterangan
            ORDER BY
                MAX(CASE WHEN tahapan_penanganan = 'PRA PENUNTUTAN' THEN tanggal END) DESC
        """

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Add row numbers and format
        result = []
        for i, row in enumerate(rows, start=1):
            result.append({
                'NO': i,
                'nama_tersangka': row['nama_tersangka'] or '-',
                'pasal': row['pasal'] or '-',
                'jenis_perkara': row['jenis_perkara'] or '-',
                'pra_penuntutan': row['pra_penuntutan'] or '-',
                'penuntutan': row['penuntutan'] or '-',
                'upaya_hukum': row['upaya_hukum'] or '-'
            })

        return result
```

### B. Route Handler (app_with_db.py)

```python
@app.route('/laporan_pelacakan_perkara')
@login_required
def laporan_pelacakan_perkara():
    """Laporan pelacakan perkara per tersangka"""
    # Get filter parameters
    bulan = request.args.get('bulan', type=int)
    tahun = request.args.get('tahun', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    jenis_perkara = request.args.get('jenis_perkara')
    tersangka = request.args.get('tersangka')

    # Default to current year
    if not tahun and not start_date:
        tahun = datetime.now().year

    # Get report data
    try:
        report_data = db.get_pelacakan_perkara_report_data(
            bulan=bulan,
            tahun=tahun,
            start_date=start_date,
            end_date=end_date,
            jenis_perkara=jenis_perkara,
            tersangka=tersangka
        )

        # Calculate totals
        total_keseluruhan = len(report_data)
        total_pra_penuntutan = sum(1 for item in report_data if item['pra_penuntutan'] != '-')
        total_penuntutan = sum(1 for item in report_data if item['penuntutan'] != '-')
        total_upaya_hukum = sum(1 for item in report_data if item['upaya_hukum'] != '-')

        # Prepare context
        return render_template('laporan_pelacakan_perkara.html',
                             report_data=report_data,
                             total_keseluruhan=total_keseluruhan,
                             total_pra_penuntutan=total_pra_penuntutan,
                             total_penuntutan=total_penuntutan,
                             total_upaya_hukum=total_upaya_hukum,
                             bulan=bulan,
                             tahun=tahun,
                             start_date=start_date,
                             end_date=end_date,
                             jenis_perkara=jenis_perkara,
                             tersangka=tersangka,
                             month_names=MONTH_NAMES)

    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'danger')
        return redirect(url_for('index'))
```

### C. Template HTML (templates/laporan_pelacakan_perkara.html)

```html
{% extends "base.html" %}

{% block title %}Laporan Pelacakan Perkara{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h4 class="mb-0">
                <i class="fas fa-chart-line"></i> Laporan Pelacakan Perkara
            </h4>
        </div>

        <div class="card-body">
            <!-- Filter Form -->
            <form method="GET" action="{{ url_for('laporan_pelacakan_perkara') }}" class="mb-4">
                <div class="row g-3">
                    <!-- Month Selection -->
                    <div class="col-md-3">
                        <label class="form-label">Bulan</label>
                        <select name="bulan" class="form-select">
                            <option value="">Semua Bulan</option>
                            {% for i in range(1, 13) %}
                            <option value="{{ i }}" {% if bulan == i %}selected{% endif %}>
                                {{ month_names[i] }}
                            </option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- Year Selection -->
                    <div class="col-md-3">
                        <label class="form-label">Tahun</label>
                        <select name="tahun" class="form-select">
                            <option value="">Pilih Tahun</option>
                            {% for y in range(2020, 2031) %}
                            <option value="{{ y }}" {% if tahun == y %}selected{% endif %}>
                                {{ y }}
                            </option>
                            {% endfor %}
                        </select>
                    </div>

                    <!-- Jenis Perkara Filter -->
                    <div class="col-md-3">
                        <label class="form-label">Jenis Perkara</label>
                        <select name="jenis_perkara" class="form-select">
                            <option value="">Semua Jenis</option>
                            <option value="NARKOBA" {% if jenis_perkara == 'NARKOBA' %}selected{% endif %}>NARKOBA</option>
                            <option value="JUDI" {% if jenis_perkara == 'JUDI' %}selected{% endif %}>JUDI</option>
                            <option value="KDRT" {% if jenis_perkara == 'KDRT' %}selected{% endif %}>KDRT</option>
                            <!-- Add more options -->
                        </select>
                    </div>

                    <!-- Submit Button -->
                    <div class="col-md-3 d-flex align-items-end">
                        <button type="submit" class="btn btn-primary w-100">
                            <i class="fas fa-search"></i> Tampilkan
                        </button>
                    </div>
                </div>

                <!-- Search by Name -->
                <div class="row g-3 mt-2">
                    <div class="col-md-6">
                        <label class="form-label">Cari Nama Tersangka</label>
                        <input type="text" name="tersangka" class="form-control"
                               value="{{ tersangka or '' }}"
                               placeholder="Ketik nama tersangka...">
                    </div>
                </div>
            </form>

            <!-- Export Buttons -->
            <div class="mb-3">
                <a href="{{ url_for('export_pelacakan_perkara_excel',
                          bulan=bulan, tahun=tahun,
                          jenis_perkara=jenis_perkara, tersangka=tersangka) }}"
                   class="btn btn-success">
                    <i class="fas fa-file-excel"></i> Export Excel
                </a>
            </div>

            <!-- Report Table -->
            <div class="table-responsive">
                <table class="table table-bordered table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th style="width: 5%;">NO</th>
                            <th style="width: 20%;">NAMA TERSANGKA</th>
                            <th style="width: 10%;">PASAL</th>
                            <th style="width: 15%;">JENIS PERKARA</th>
                            <th style="width: 15%;">PRA PENUNTUTAN</th>
                            <th style="width: 15%;">PENUNTUTAN</th>
                            <th style="width: 20%;">UPAYA HUKUM</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if report_data %}
                            {% for item in report_data %}
                            <tr>
                                <td class="text-center">{{ item.NO }}</td>
                                <td>{{ item.nama_tersangka }}</td>
                                <td class="text-center">{{ item.pasal }}</td>
                                <td>{{ item.jenis_perkara }}</td>
                                <td class="text-center">{{ item.pra_penuntutan }}</td>
                                <td class="text-center">{{ item.penuntutan }}</td>
                                <td class="text-center">{{ item.upaya_hukum }}</td>
                            </tr>
                            {% endfor %}

                            <!-- Total Row -->
                            <tr class="table-warning fw-bold">
                                <td colspan="4" class="text-end">TOTAL:</td>
                                <td class="text-center">{{ total_pra_penuntutan }}</td>
                                <td class="text-center">{{ total_penuntutan }}</td>
                                <td class="text-center">{{ total_upaya_hukum }}</td>
                            </tr>
                        {% else %}
                            <tr>
                                <td colspan="7" class="text-center text-muted">
                                    <i class="fas fa-info-circle"></i>
                                    Tidak ada data untuk filter yang dipilih
                                </td>
                            </tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>

            <!-- Summary Statistics -->
            {% if report_data %}
            <div class="alert alert-info mt-3">
                <strong>Ringkasan:</strong>
                Total {{ total_keseluruhan }} perkara tercatat.
                {{ total_pra_penuntutan }} di tahap Pra Penuntutan,
                {{ total_penuntutan }} di tahap Penuntutan,
                {{ total_upaya_hukum }} masuk Upaya Hukum.
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

### D. Excel Export Route (app_with_db.py)

```python
@app.route('/export_pelacakan_perkara_excel')
@login_required
def export_pelacakan_perkara_excel():
    """Export laporan pelacakan perkara ke Excel"""
    # Get same filters as main report
    bulan = request.args.get('bulan', type=int)
    tahun = request.args.get('tahun', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    jenis_perkara = request.args.get('jenis_perkara')
    tersangka = request.args.get('tersangka')

    # Get data
    report_data = db.get_pelacakan_perkara_report_data(
        bulan=bulan, tahun=tahun, start_date=start_date,
        end_date=end_date, jenis_perkara=jenis_perkara, tersangka=tersangka
    )

    # Create Excel file
    import io
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

    wb = Workbook()
    ws = wb.active
    ws.title = "Pelacakan Perkara"

    # Title
    ws.merge_cells('A1:G1')
    title_cell = ws['A1']
    title_cell.value = "LAPORAN PELACAKAN PERKARA"
    title_cell.font = Font(size=14, bold=True)
    title_cell.alignment = Alignment(horizontal='center', vertical='center')

    # Period info
    ws.merge_cells('A2:G2')
    period_text = f"Periode: "
    if bulan and tahun:
        period_text += f"{MONTH_NAMES[bulan]} {tahun}"
    elif tahun:
        period_text += f"Tahun {tahun}"
    else:
        period_text += "Semua Periode"
    ws['A2'].value = period_text
    ws['A2'].alignment = Alignment(horizontal='center')

    # Headers
    headers = ['NO', 'NAMA TERSANGKA', 'PASAL', 'JENIS PERKARA',
               'PRA PENUNTUTAN', 'PENUNTUTAN', 'UPAYA HUKUM']
    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    header_font = Font(color='FFFFFF', bold=True)

    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # Data rows
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    for row_num, item in enumerate(report_data, start=5):
        ws.cell(row=row_num, column=1, value=item['NO']).alignment = Alignment(horizontal='center')
        ws.cell(row=row_num, column=2, value=item['nama_tersangka'])
        ws.cell(row=row_num, column=3, value=item['pasal']).alignment = Alignment(horizontal='center')
        ws.cell(row=row_num, column=4, value=item['jenis_perkara'])
        ws.cell(row=row_num, column=5, value=item['pra_penuntutan']).alignment = Alignment(horizontal='center')
        ws.cell(row=row_num, column=6, value=item['penuntutan']).alignment = Alignment(horizontal='center')
        ws.cell(row=row_num, column=7, value=item['upaya_hukum']).alignment = Alignment(horizontal='center')

        # Apply borders
        for col in range(1, 8):
            ws.cell(row=row_num, column=col).border = thin_border

    # Column widths
    ws.column_dimensions['A'].width = 6
    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 18
    ws.column_dimensions['F'].width = 18
    ws.column_dimensions['G'].width = 18

    # Save to BytesIO
    excel_file = io.BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    # Generate filename
    filename = f"Laporan_Pelacakan_Perkara_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )
```

---

## 9. NAVIGASI MENU

Tambahkan menu item di `templates/base.html` atau navigation template:

```html
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('laporan_pelacakan_perkara') }}">
        <i class="fas fa-list-check"></i> Laporan Pelacakan Perkara
    </a>
</li>
```

---

## 10. TESTING CHECKLIST

### Unit Tests
- [ ] Database query returns correct data structure
- [ ] NULL values handled properly (displayed as dash)
- [ ] Date formatting correct (DD/MM/YYYY)
- [ ] Row numbering sequential

### Integration Tests
- [ ] Filter by bulan works
- [ ] Filter by tahun works
- [ ] Search by nama tersangka works
- [ ] Multiple filters work together

### UI/UX Tests
- [ ] Table responsive on mobile
- [ ] Export button generates valid Excel
- [ ] Pagination works (if implemented)
- [ ] No data message displays correctly

### Performance Tests
- [ ] Load time < 2 seconds for 100 rows
- [ ] Load time < 5 seconds for 1000 rows
- [ ] Excel export completes without timeout

---

## 11. DEPLOYMENT STEPS

1. **Database Changes:**
   ```bash
   # No schema changes needed for MVP
   # Optional: Add indexes for performance
   ALTER TABLE pidum_data ADD INDEX idx_identitas (identitas_tersangka(100));
   ALTER TABLE pidum_data ADD INDEX idx_tanggal (tanggal);
   ```

2. **Code Deployment:**
   ```bash
   # Add new code to mysql_database.py
   # Add new routes to app_with_db.py
   # Add new template to templates/
   ```

3. **Restart Application:**
   ```bash
   # If using systemd:
   sudo systemctl restart kejaksaan_app

   # If using gunicorn directly:
   pkill gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.app_with_db:app
   ```

4. **Verify:**
   - Navigate to /laporan_pelacakan_perkara
   - Test filters
   - Test export

---

## 12. FUTURE ENHANCEMENTS

### Phase 4: Advanced Features (Post-Launch)

1. **Timeline Visualization:**
   - Gantt chart showing case progression
   - Color-coded by status
   - Highlight delays/bottlenecks

2. **Case Status Tracking:**
   - Add status field: "Dalam Proses", "Selesai", "Ditangguhkan"
   - Status change history log
   - Notification when status changes

3. **Analytics Dashboard:**
   - Average time per tahapan
   - Success rate by jenis perkara
   - Workload distribution

4. **Document Attachment:**
   - Upload related documents per case
   - Link to physical file location
   - Document versioning

5. **Case Linking:**
   - Link related cases
   - Track split/merged cases
   - Family tree view

---

## 13. KESIMPULAN DAN REKOMENDASI

### ✅ FEASIBILITY: VERY HIGH (95%)

**Kesimpulan:**
Permintaan laporan pelacakan perkara baru **sangat layak dan mudah diimplementasikan**. Aplikasi kejaksaan sudah memiliki semua komponen yang dibutuhkan:

1. ✅ Data tersedia di database
2. ✅ Pattern laporan sudah matang
3. ✅ Template system sudah ada
4. ✅ Export functionality sudah ada
5. ✅ Authentication & authorization sudah ada

**Rekomendasi Next Steps:**

1. **Implementasi MVP (Tahap 1)** terlebih dahulu
   - Estimasi: 2-3 jam
   - Delivery: Laporan dasar yang berfungsi

2. **User Acceptance Testing**
   - Test dengan real data
   - Gather feedback dari user

3. **Iterasi berdasarkan feedback**
   - Add features dari Tahap 2
   - Optimize query performance

4. **Production deployment**
   - Deploy to staging first
   - Monitor performance
   - Deploy to production

**Prioritas Fitur:**

| Prioritas | Fitur | Alasan |
|-----------|-------|--------|
| P0 (Must Have) | Basic report dengan 7 kolom | Core requirement |
| P0 | Filter bulan/tahun | User convenience |
| P1 (Should Have) | Excel export | Common request |
| P1 | Search by nama | Usability |
| P2 (Nice to Have) | Pagination | Performance for large data |
| P2 | Word export | Optional format |

---

## CONTACT & SUPPORT

Untuk pertanyaan implementasi atau diskusi detail teknis, hubungi:
- Development Team
- Project Manager

**Document Version:** 1.0
**Last Updated:** 28 November 2025
**Status:** Ready for Implementation
