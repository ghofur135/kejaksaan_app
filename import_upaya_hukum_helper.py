"""
Helper functions for importing Upaya Hukum data from CSV files
"""

import pandas as pd
import re
from datetime import datetime
from werkzeug.utils import secure_filename

def allowed_file_upaya_hukum(filename):
    """Check if the uploaded file has an allowed extension for upaya hukum import"""
    allowed_extensions = {'csv', 'xlsx', 'xls'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

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

def get_jenis_perkara_suggestions_upaya_hukum(terdakwa_info):
    """Get jenis perkara suggestions based on terdakwa information"""
    if not terdakwa_info or terdakwa_info.strip() == '':
        return 'PERKARA LAINNYA'
    
    terdakwa_lower = str(terdakwa_info).lower()
    
    # Mapping berdasarkan kata kunci yang mungkin ada dalam data terdakwa
    suggestions = {
        'narkotika': ['narkotika', 'narkoba', 'sabu', 'ganja', 'kokain', 'ekstasi'],
        'korupsi': ['korupsi', 'gratifikasi', 'suap', 'penggelapan'],
        'pencurian': ['curi', 'pencurian', 'theft'],
        'penipuan': ['tipu', 'penipuan', 'fraud'],
        'penganiayaan': ['aniaya', 'penganiayaan', 'kekerasan'],
        'pembunuhan': ['bunuh', 'pembunuhan', 'murder'],
        'perkosaan': ['perkosa', 'pemerkosaan', 'sexual'],
        'pengelapan': ['gelap', 'pengelapan', 'embezzlement'],
    }
    
    # Cek kata kunci dalam terdakwa info
    for jenis, keywords in suggestions.items():
        for keyword in keywords:
            if keyword in terdakwa_lower:
                return jenis.upper()
    
    # Default suggestion
    return 'PERKARA LAINNYA'

def process_upaya_hukum_import_file(file):
    """Process uploaded file specifically for upaya hukum format"""
    try:
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        # Read file based on extension
        if file_ext == 'csv':
            df = pd.read_csv(file)
        elif file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(file)
        else:
            raise ValueError("Format file tidak didukung. Gunakan CSV, XLS, atau XLSX.")
        
        # Validate required columns
        required_columns = ['No', 'Terdakwa_Terpidana', 'No_Tanggal_RP9']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Kolom yang diperlukan tidak ditemukan: {', '.join(missing_columns)}")
        
        # Convert DataFrame to standardized format
        standardized_data = []
        
        for i, row in df.iterrows():
            # Skip header row if it contains values like "1", "2", "3"
            if str(row.get('No', '')).strip() in ['1', '2', '3'] and \
               str(row.get('Terdakwa_Terpidana', '')).strip() in ['1', '2', '3'] and \
               str(row.get('No_Tanggal_RP9', '')).strip() in ['1', '2', '3']:
                continue
            
            # Extract and clean data
            no = str(row.get('No', i + 1)).strip()
            terdakwa_terpidana = str(row.get('Terdakwa_Terpidana', '')).strip()
            no_tanggal_rp9 = str(row.get('No_Tanggal_RP9', '')).strip()
            
            # Skip empty rows
            if not terdakwa_terpidana or terdakwa_terpidana.lower() in ['nan', 'none', '']:
                continue
            
            # Extract date from No_Tanggal_RP9
            extracted_date = extract_date_from_rp9(no_tanggal_rp9)
            
            # Create standardized row
            std_row = {
                'ROW_INDEX': i,
                'NO': no,
                'PERIODE': '1',  # Default periode
                'TANGGAL': extracted_date,
                'JENIS_PERKARA_ORIGINAL': terdakwa_terpidana,
                'KETERANGAN': f"Terdakwa: {terdakwa_terpidana} | RP9: {no_tanggal_rp9}",
                'TAHAPAN_PENANGANAN': 'UPAYA HUKUM',
                'TERDAKWA_ORIGINAL': terdakwa_terpidana,
                'RP9_ORIGINAL': no_tanggal_rp9
            }
            
            # Get suggested jenis perkara
            suggestion = get_jenis_perkara_suggestions_upaya_hukum(terdakwa_terpidana)
            std_row['SUGGESTED_JENIS_PERKARA'] = suggestion
            
            standardized_data.append(std_row)
        
        return {
            'success': True,
            'data': standardized_data,
            'total_rows': len(standardized_data),
            'columns': list(df.columns) if not df.empty else [],
            'format_type': 'upaya_hukum'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': [],
            'total_rows': 0,
            'columns': [],
            'format_type': 'upaya_hukum'
        }

def prepare_upaya_hukum_data_for_db(import_data, form_data):
    """Prepare upaya hukum data for database insertion"""
    prepared_data = []
    
    for i, original_row in enumerate(import_data):
        # Check if this row should be included (checkbox checked)
        include_key = f'include_{i}'
        if include_key not in form_data:
            continue  # Skip unchecked rows
        
        # Get form data for this row
        periode = form_data.get(f'periode_{i}', '1')
        tanggal = form_data.get(f'tanggal_{i}', original_row.get('TANGGAL'))
        jenis_perkara = form_data.get(f'jenis_perkara_{i}', 'PERKARA LAINNYA')
        keterangan = form_data.get(f'keterangan_{i}', original_row.get('KETERANGAN', ''))
        
        # Prepare data for database insertion
        prepared_row = {
            'NO': str(original_row.get('NO', i + 1)),
            'PERIODE': str(periode),
            'TANGGAL': tanggal,
            'JENIS PERKARA': jenis_perkara,
            'TAHAPAN_PENANGANAN': 'UPAYA HUKUM',
            'KETERANGAN': str(keterangan)
        }
        
        prepared_data.append(prepared_row)
    
    return prepared_data