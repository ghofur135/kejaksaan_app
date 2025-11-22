"""
Helper functions for importing Upaya Hukum data from CSV files
Extended format support for Register Upaya Hukum with Perlawanan, Banding, Kasasi, PK, Grasi
"""

import pandas as pd
import re
from datetime import datetime
from werkzeug.utils import secure_filename

def allowed_file_upaya_hukum(filename):
    """Check if the uploaded file has an allowed extension for upaya hukum import"""
    allowed_extensions = {'csv', 'xlsx', 'xls'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def clean_value(val):
    """Clean a value - convert nan, None, '-' to empty string"""
    if pd.isna(val) or val is None:
        return ''
    val_str = str(val).strip()
    if val_str.lower() in ['nan', 'none', '-', '']:
        return ''
    return val_str

def extract_date_from_rp9(no_tanggal_rp9):
    """Extract date from No_Tanggal_RP9 field (e.g., PDM- 08/PRBAL/Eoh.2/06/2025)"""
    try:
        # Pattern untuk mengekstrak tanggal dari format seperti PDM- 08/PRBAL/Eoh.2/06/2025
        # Mengambil bulan dan tahun terakhir
        patterns = [
            r'(\d{2})/(\d{4})$',  # MM/YYYY di akhir
            r'(\d{1,2})/(\d{4})$',  # M/YYYY di akhir
        ]

        for pattern in patterns:
            match = re.search(pattern, str(no_tanggal_rp9))
            if match:
                month = match.group(1).zfill(2)
                year = match.group(2)
                # Gunakan tanggal 1 sebagai default
                return f"{year}-{month}-01"

        # Jika tidak ada pattern yang cocok, gunakan tanggal hari ini
        return datetime.now().strftime('%Y-%m-%d')

    except Exception as e:
        print(f"Error extracting date from RP9: {e}")
        return datetime.now().strftime('%Y-%m-%d')

def extract_date_from_transaksi(tanggal_transaksi):
    """Extract date from Tanggal_Transaksi field (e.g., 'Terdakwa: 2025-09-08 0' or 'Jaksa: 2025- 09-01 0')"""
    try:
        # Pattern untuk mengekstrak tanggal dari format seperti "Terdakwa: 2025-09-08 0"
        patterns = [
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD atau YYYY-M-D
            r'(\d{4})-\s*(\d{1,2})-(\d{1,2})',  # YYYY- MM-DD (dengan spasi)
        ]

        for pattern in patterns:
            match = re.search(pattern, str(tanggal_transaksi))
            if match:
                year = match.group(1)
                month = match.group(2).zfill(2)
                day = match.group(3).zfill(2)
                return f"{year}-{month}-{day}"

        # Jika tidak ada pattern yang cocok, gunakan tanggal hari ini
        return datetime.now().strftime('%Y-%m-%d')

    except Exception as e:
        print(f"Error extracting date from transaksi: {e}")
        return datetime.now().strftime('%Y-%m-%d')

# Column mapping from CSV to database fields
CSV_TO_DB_MAPPING = {
    'No': 'no',
    'Terdakwa_Terpidana': 'terdakwa_terpidana',
    'No_Tanggal_RP9': 'no_tanggal_rp9',
    # Perlawanan
    'Perlawanan_No_Tgl_Penetapan_PN': 'perlawanan_no_tgl_penetapan_pn',
    'Perlawanan_No_Tgl_Akte': 'perlawanan_no_tgl_akte',
    'Perlawanan_Tgl_Pengajuan_Memori': 'perlawanan_tgl_pengajuan_memori',
    'Perlawanan_Yang_Mengajukan_JPU': 'perlawanan_yang_mengajukan_jpu',
    'Perlawanan_Yang_Mengajukan_Terdakwa': 'perlawanan_yang_mengajukan_terdakwa',
    'Perlawanan_No_Tgl_Amar_Penetapan_PT': 'perlawanan_no_tgl_amar_penetapan_pt',
    # Banding
    'Banding_No_Tgl_Akte_Permohonan': 'banding_no_tgl_akte_permohonan',
    'Banding_Tgl_Pengajuan_Memori': 'banding_tgl_pengajuan_memori',
    'Banding_Yang_Mengajukan_JPU': 'banding_yang_mengajukan_jpu',
    'Banding_Yang_Mengajukan_Terdakwa': 'banding_yang_mengajukan_terdakwa',
    'Banding_No_Tgl_Amar_Putusan_PT': 'banding_no_tgl_amar_putusan_pt',
    # Kasasi
    'Kasasi_No_Tgl_Akte_Permohonan': 'kasasi_no_tgl_akte_permohonan',
    'Kasasi_Tgl_Pengajuan_Memori': 'kasasi_tgl_pengajuan_memori',
    'Kasasi_Yang_Mengajukan_JPU': 'kasasi_yang_mengajukan_jpu',
    'Kasasi_Yang_Mengajukan_Terdakwa': 'kasasi_yang_mengajukan_terdakwa',
    'Kasasi_No_Tanggal_Amar_Putusan_MA': 'kasasi_no_tgl_amar_putusan_ma',
    # Kasasi Demi Hukum
    'KasasiDemiHukum_Tanggal_Diajukan': 'kasasi_demi_hukum_tgl_diajukan',
    'KasasiDemiHukum_Keadaan_Putusan_PN': 'kasasi_demi_hukum_keadaan_putusan_pn',
    'KasasiDemiHukum_No_Tgl_Amar_Putusan_MA': 'kasasi_demi_hukum_no_tgl_amar_putusan_ma',
    # PK
    'PK_Tgl_Diajukan_Terpidana': 'pk_tgl_diajukan_terpidana',
    'PK_Tgl_Pemeriksaan_Berita_Acara': 'pk_tgl_pemeriksaan_berita_acara',
    'PK_No_Tgl_Amar_Putusan': 'pk_no_tgl_amar_putusan',
    # Grasi
    'Grasi_Tgl_Penerimaan_Berkas': 'grasi_tgl_penerimaan_berkas',
    'Grasi_Tgl_Penundaan_Eksekusi': 'grasi_tgl_penundaan_eksekusi',
    'Grasi_Tgl_Risalah_Pertimbangan_Kajari': 'grasi_tgl_risalah_pertimbangan_kajari',
    'Grasi_Tgl_Terima_KEPRES': 'grasi_tgl_terima_kepres',
    'Grasi_No_Tgl_KEPRES_Amar': 'grasi_no_tgl_kepres_amar',
}

def detect_csv_format(columns):
    """Detect if CSV is extended format (with Perlawanan, Banding, etc.) or simple format"""
    extended_columns = ['Perlawanan_No_Tgl_Penetapan_PN', 'Banding_No_Tgl_Akte_Permohonan',
                       'Kasasi_No_Tgl_Akte_Permohonan', 'PK_Tgl_Diajukan_Terpidana',
                       'Grasi_Tgl_Penerimaan_Berkas']

    # Check if any extended column exists
    for col in extended_columns:
        if col in columns:
            return 'extended'
    return 'simple'

def get_jenis_perkara_suggestions_upaya_hukum(terdakwa_info):
    """Get jenis perkara suggestions based on terdakwa information"""
    if not terdakwa_info or terdakwa_info.strip() == '':
        return 'PERKARA LAINNYA'
    
    terdakwa_lower = str(terdakwa_info).lower()
    
    # Mapping berdasarkan kata kunci yang mungkin ada dalam data terdakwa
    # Hanya 7 jenis perkara yang diizinkan
    suggestions = {
        'NARKOBA': ['narkotika', 'narkoba', 'sabu', 'ganja', 'kokain', 'ekstasi', 'heroin', 'methamphetamin'],
        'PERKARA ANAK': ['anak', 'juvenile', 'minor', 'remaja', 'uu no. 23 tahun 2002', 'uu no.23 tahun 2002', 'anak di bawah umur'],
        'KESUSILAAN': ['kesusilaan', 'susila', 'moral', 'cabul', 'layanan seks', 'prostitusi', 'asusila', 'perkosa', 'pemerkosaan', 'sexual'],
        'JUDI': ['judi', 'gambling', 'togel', 'taruhan', 'sabung ayam'],
        'KDRT': ['kdrt', 'kekerasan dalam rumah tangga', 'domestic violence', 'istri', 'suami', 'orang tua'],
        'OHARDA': ['oharda', 'orang hilang', 'harta benda', 'pasal 372', 'pasal 378', 'pasal 362', 'pasal 363', 'gelap', 'pengelapan', 'embezzlement', 'penggapaian', 'curi', 'pencurian', 'theft', 'maling', 'tipu', 'penipuan', 'fraud', 'penipuan investasi'],
        'PERKARA LAINNYA': []  # Default for cases that don't match other categories
    }
    
    # Cek kata kunci dalam terdakwa info
    for jenis, keywords in suggestions.items():
        for keyword in keywords:
            if keyword in terdakwa_lower:
                return jenis
    
    # Default suggestion
    return 'PERKARA LAINNYA'

def process_upaya_hukum_import_file(file):
    """Process uploaded file for upaya hukum format - supports both simple and extended formats"""
    try:
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()

        # Read file based on extension
        if file_ext == 'csv':
            df = pd.read_csv(file, encoding='utf-8')
        elif file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(file)
        else:
            raise ValueError("Format file tidak didukung. Gunakan CSV, XLS, atau XLSX.")

        # Validate required columns
        required_columns = ['No', 'Terdakwa_Terpidana', 'No_Tanggal_RP9']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Kolom yang diperlukan tidak ditemukan: {', '.join(missing_cols)}")

        # Detect format type
        format_type = detect_csv_format(df.columns)

        # Convert DataFrame to standardized format
        standardized_data = []

        for i, row in df.iterrows():
            # Skip header row duplicates (rows where No contains "1", "2", "3" as text headers)
            no_val = clean_value(row.get('No', ''))
            terdakwa_val = clean_value(row.get('Terdakwa_Terpidana', ''))

            # Skip if it looks like a repeated header row
            if no_val in ['1', '2', '3'] and terdakwa_val in ['1', '2', '3', '2']:
                continue

            # Skip empty rows
            if not terdakwa_val:
                continue

            # Build data row based on format
            std_row = {
                'ROW_INDEX': i,
                'format_type': format_type,
            }

            # Map all CSV columns to database fields
            for csv_col, db_field in CSV_TO_DB_MAPPING.items():
                if csv_col in df.columns:
                    std_row[db_field] = clean_value(row.get(csv_col, ''))
                else:
                    std_row[db_field] = ''

            # Get suggested jenis perkara
            suggestion = get_jenis_perkara_suggestions_upaya_hukum(std_row.get('terdakwa_terpidana', ''))
            std_row['jenis_perkara'] = suggestion
            std_row['SUGGESTED_JENIS_PERKARA'] = suggestion

            # Determine active upaya hukum types for display
            active_types = []
            if std_row.get('banding_no_tgl_akte_permohonan') or std_row.get('banding_no_tgl_amar_putusan_pt'):
                active_types.append('Banding')
            if std_row.get('kasasi_no_tgl_akte_permohonan') or std_row.get('kasasi_no_tgl_amar_putusan_ma'):
                active_types.append('Kasasi')
            if std_row.get('pk_tgl_diajukan_terpidana') or std_row.get('pk_no_tgl_amar_putusan'):
                active_types.append('PK')
            if std_row.get('grasi_tgl_penerimaan_berkas') or std_row.get('grasi_no_tgl_kepres_amar'):
                active_types.append('Grasi')
            if std_row.get('perlawanan_no_tgl_penetapan_pn') or std_row.get('perlawanan_no_tgl_amar_penetapan_pt'):
                active_types.append('Perlawanan')

            std_row['active_upaya_types'] = ', '.join(active_types) if active_types else '-'

            standardized_data.append(std_row)

        return {
            'success': True,
            'data': standardized_data,
            'total_rows': len(standardized_data),
            'columns': list(df.columns) if not df.empty else [],
            'format_type': format_type
        }

    except Exception as e:
        import traceback
        print(f"Error processing upaya hukum file: {e}")
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'data': [],
            'total_rows': 0,
            'columns': [],
            'format_type': 'unknown'
        }

def prepare_upaya_hukum_data_for_db(import_data, form_data):
    """Prepare upaya hukum data for database insertion into upaya_hukum_data table"""
    prepared_data = []

    for i, original_row in enumerate(import_data):
        # Check if this row should be included (checkbox checked)
        include_key = f'include_{i}'
        if include_key not in form_data:
            continue  # Skip unchecked rows

        # Get jenis_perkara from form (can be edited by user)
        jenis_perkara = form_data.get(f'jenis_perkara_{i}', original_row.get('jenis_perkara', 'PERKARA LAINNYA'))

        # Prepare data for database insertion - map directly to upaya_hukum_data columns
        prepared_row = {
            'no': original_row.get('no', str(i + 1)),
            'terdakwa_terpidana': original_row.get('terdakwa_terpidana', ''),
            'no_tanggal_rp9': original_row.get('no_tanggal_rp9', ''),
            'jenis_perkara': jenis_perkara,
            # Perlawanan
            'perlawanan_no_tgl_penetapan_pn': original_row.get('perlawanan_no_tgl_penetapan_pn', ''),
            'perlawanan_no_tgl_akte': original_row.get('perlawanan_no_tgl_akte', ''),
            'perlawanan_tgl_pengajuan_memori': original_row.get('perlawanan_tgl_pengajuan_memori', ''),
            'perlawanan_yang_mengajukan_jpu': original_row.get('perlawanan_yang_mengajukan_jpu', ''),
            'perlawanan_yang_mengajukan_terdakwa': original_row.get('perlawanan_yang_mengajukan_terdakwa', ''),
            'perlawanan_no_tgl_amar_penetapan_pt': original_row.get('perlawanan_no_tgl_amar_penetapan_pt', ''),
            # Banding
            'banding_no_tgl_akte_permohonan': original_row.get('banding_no_tgl_akte_permohonan', ''),
            'banding_tgl_pengajuan_memori': original_row.get('banding_tgl_pengajuan_memori', ''),
            'banding_yang_mengajukan_jpu': original_row.get('banding_yang_mengajukan_jpu', ''),
            'banding_yang_mengajukan_terdakwa': original_row.get('banding_yang_mengajukan_terdakwa', ''),
            'banding_no_tgl_amar_putusan_pt': original_row.get('banding_no_tgl_amar_putusan_pt', ''),
            # Kasasi
            'kasasi_no_tgl_akte_permohonan': original_row.get('kasasi_no_tgl_akte_permohonan', ''),
            'kasasi_tgl_pengajuan_memori': original_row.get('kasasi_tgl_pengajuan_memori', ''),
            'kasasi_yang_mengajukan_jpu': original_row.get('kasasi_yang_mengajukan_jpu', ''),
            'kasasi_yang_mengajukan_terdakwa': original_row.get('kasasi_yang_mengajukan_terdakwa', ''),
            'kasasi_no_tgl_amar_putusan_ma': original_row.get('kasasi_no_tgl_amar_putusan_ma', ''),
            # Kasasi Demi Hukum
            'kasasi_demi_hukum_tgl_diajukan': original_row.get('kasasi_demi_hukum_tgl_diajukan', ''),
            'kasasi_demi_hukum_keadaan_putusan_pn': original_row.get('kasasi_demi_hukum_keadaan_putusan_pn', ''),
            'kasasi_demi_hukum_no_tgl_amar_putusan_ma': original_row.get('kasasi_demi_hukum_no_tgl_amar_putusan_ma', ''),
            # PK
            'pk_tgl_diajukan_terpidana': original_row.get('pk_tgl_diajukan_terpidana', ''),
            'pk_tgl_pemeriksaan_berita_acara': original_row.get('pk_tgl_pemeriksaan_berita_acara', ''),
            'pk_no_tgl_amar_putusan': original_row.get('pk_no_tgl_amar_putusan', ''),
            # Grasi
            'grasi_tgl_penerimaan_berkas': original_row.get('grasi_tgl_penerimaan_berkas', ''),
            'grasi_tgl_penundaan_eksekusi': original_row.get('grasi_tgl_penundaan_eksekusi', ''),
            'grasi_tgl_risalah_pertimbangan_kajari': original_row.get('grasi_tgl_risalah_pertimbangan_kajari', ''),
            'grasi_tgl_terima_kepres': original_row.get('grasi_tgl_terima_kepres', ''),
            'grasi_no_tgl_kepres_amar': original_row.get('grasi_no_tgl_kepres_amar', ''),
        }

        prepared_data.append(prepared_row)

    return prepared_data