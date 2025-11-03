"""
Import Helper khusus untuk data Pra Penuntutan
Format CSV: No, Tgl_Nomor, Pasal_yang_Disangkakan
"""

import pandas as pd
import io
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import re
import json
import tempfile
import uuid

def allowed_file_pra_penuntutan(filename):
    """Check if uploaded file has allowed extension for pra penuntutan"""
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_import_data_to_temp(data, filename):
    """Save import data to temporary file and return session ID"""
    # Generate unique session ID
    session_id = str(uuid.uuid4())

    # Create temp directory if not exists
    temp_dir = os.path.join(tempfile.gettempdir(), 'kejaksaan_imports')
    os.makedirs(temp_dir, exist_ok=True)

    # Save data to temp file
    temp_file = os.path.join(temp_dir, f'{session_id}.json')

    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump({
            'data': data,
            'filename': filename,
            'timestamp': datetime.now().isoformat()
        }, f)

    return session_id

def load_import_data_from_temp(session_id):
    """Load import data from temporary file"""
    if not session_id:
        return None

    temp_dir = os.path.join(tempfile.gettempdir(), 'kejaksaan_imports')
    temp_file = os.path.join(temp_dir, f'{session_id}.json')

    if not os.path.exists(temp_file):
        return None

    try:
        with open(temp_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading temp file: {e}")
        return None

def cleanup_import_temp_file(session_id):
    """Clean up temporary import file"""
    if not session_id:
        return

    temp_dir = os.path.join(tempfile.gettempdir(), 'kejaksaan_imports')
    temp_file = os.path.join(temp_dir, f'{session_id}.json')

    if os.path.exists(temp_file):
        try:
            os.remove(temp_file)
        except Exception as e:
            print(f"Error removing temp file: {e}")

def extract_date_from_tgl_nomor(tgl_nomor_value):
    """Extract date from Tgl_Nomor field like '2025-08-28 SPDP/63/VIII/RES.1.24/2025/Reskrim'"""
    if not tgl_nomor_value:
        return datetime.now().strftime('%Y-%m-%d')
    
    # Look for date pattern YYYY-MM-DD at the beginning
    date_pattern = r'^(\d{4}-\d{2}-\d{2})'
    match = re.search(date_pattern, str(tgl_nomor_value))
    
    if match:
        return match.group(1)
    
    # If no date found, try to extract year and month from SPDP format
    # Example: SPDP/63/VIII/RES.1.24/2025/Reskrim
    year_pattern = r'/(\d{4})/'
    year_match = re.search(year_pattern, str(tgl_nomor_value))
    
    if year_match:
        year = year_match.group(1)
        # Try to extract month from roman numerals
        month_map = {
            'I': '01', 'II': '02', 'III': '03', 'IV': '04', 'V': '05', 'VI': '06',
            'VII': '07', 'VIII': '08', 'IX': '09', 'X': '10', 'XI': '11', 'XII': '12'
        }
        
        for roman, numeric in month_map.items():
            if f'/{roman}/' in str(tgl_nomor_value):
                return f"{year}-{numeric}-01"
    
    # Default to current date if extraction fails
    return datetime.now().strftime('%Y-%m-%d')

def get_jenis_perkara_suggestions_pra_penuntutan(pasal_text):
    """Suggest jenis perkara based on pasal text for pra penuntutan data"""
    if not pasal_text:
        return "PERKARA LAINNYA"
    
    text = str(pasal_text).upper()
    
    # Enhanced mapping with more specific patterns for pra penuntutan
    mappings = {
        'NARKOBA': [
            'UU RI NOMOR 35 TAHUN 2009', 'UU NOMOR 35 TAHUN 2009', 'NARKOTIKA',
            'PASAL 114', 'PASAL 112', 'PASAL 127', 'PASAL 117', 'PASAL 119', 'PASAL 120'
        ],
        'PERKARA ANAK': [
            'UU NOMOR 17 TAHUN 2016', 'UU NOMOR 23 TAHUN 2002', 'PERLINDUNGAN ANAK',
            'PASAL 81', 'PASAL 82', 'PERUBAHAN KEDUA ATAS UNDANG-UNDANG NOMOR 23 TAHUN 2002'
        ],
        'KESUSILAAN': [
            'KESUSILAAN', 'SUSILA', 'MORAL', 'CABUL', 'PERKOSAAN',
            'PASAL 289', 'PASAL 285', 'PASAL 287'
        ],
        'OHARDA': [
            'PASAL 362', 'PASAL 363', 'PASAL 365', 'PASAL 368', 'PASAL 372', 'PASAL 374', 'PASAL 378',
            'PENCURIAN', 'PENGGELAPAN', 'PENIPUAN', 'PEMERASAN'
        ],
        'JUDI': [
            'JUDI', 'GAMBLING', 'TOGEL', 'TARUHAN'
        ],
        'KDRT': [
            'KDRT', 'KEKERASAN DALAM RUMAH TANGGA', 'DOMESTIC VIOLENCE',
            'PASAL 351', 'PENGANIAYAAN'
        ],
        'PERKARA LAINNYA': [
            'PERLINDUNGAN DATA PRIBADI', 'UU NOMOR 27 TAHUN 2022', 'PASAL 67', 'PASAL 65',
            'MINYAK DAN GAS BUMI', 'UU NO. 22 TAHUN 2021', 'PERLINDUNGAN KONSUMEN',
            'UU NO. 8 TAHUN 1999', 'METROLOGI LEGAL', 'UU NO. 2 TAHUN 1981',
            'JAMINAN FIDUSIA', 'UU NOMOR 42 TAHUN 1999'
        ]
    }
    
    # Check each category
    for category, keywords in mappings.items():
        for keyword in keywords:
            if keyword in text:
                return category
    
    return "PERKARA LAINNYA"

def process_pra_penuntutan_import_file(file):
    """Process uploaded file specifically for pra penuntutan format"""
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
        required_columns = ['No', 'Tgl_Nomor', 'Pasal_yang_Disangkakan']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Kolom yang diperlukan tidak ditemukan: {', '.join(missing_columns)}")
        
        # Convert DataFrame to standardized format
        standardized_data = []
        
        for i, row in df.iterrows():
            # Extract and clean data
            no = str(row.get('No', i + 1)).strip()
            tgl_nomor = str(row.get('Tgl_Nomor', '')).strip()
            pasal_disangkakan = str(row.get('Pasal_yang_Disangkakan', '')).strip()
            
            # Extract date from Tgl_Nomor
            extracted_date = extract_date_from_tgl_nomor(tgl_nomor)
            
            # Create standardized row
            std_row = {
                'ROW_INDEX': i,
                'NO': no,
                'PERIODE': '1',  # Default periode
                'TANGGAL': extracted_date,
                'JENIS_PERKARA_ORIGINAL': pasal_disangkakan,
                'KETERANGAN': f"SPDP: {tgl_nomor} | Pasal: {pasal_disangkakan}",
                'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',
                'TGL_NOMOR_ORIGINAL': tgl_nomor,
                'PASAL_ORIGINAL': pasal_disangkakan
            }
            
            # Get suggested jenis perkara
            suggestion = get_jenis_perkara_suggestions_pra_penuntutan(pasal_disangkakan)
            std_row['SUGGESTED_JENIS_PERKARA'] = suggestion
            
            standardized_data.append(std_row)
        
        return {
            'success': True,
            'data': standardized_data,
            'total_rows': len(standardized_data),
            'columns': list(df.columns) if not df.empty else [],
            'format_type': 'pra_penuntutan'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': [],
            'total_rows': 0,
            'columns': [],
            'format_type': 'pra_penuntutan'
        }

def prepare_pra_penuntutan_data_for_db(import_data, form_data):
    """Prepare pra penuntutan data for database insertion"""
    prepared_data = []
    
    for i, original_row in enumerate(import_data):
        # Check if this row should be included (not removed)
        jenis_perkara_key = f'jenis_perkara_{i}'
        if jenis_perkara_key not in form_data:
            continue  # Skip removed rows
        
        # Get form data for this row
        periode = form_data.get(f'periode_{i}', '1')
        tanggal = form_data.get(f'tanggal_{i}', original_row.get('TANGGAL'))
        jenis_perkara = form_data.get(jenis_perkara_key, 'PERKARA LAINNYA')
        keterangan = form_data.get(f'keterangan_{i}', original_row.get('KETERANGAN', ''))
        
        # Prepare data for database insertion
        prepared_row = {
            'NO': str(original_row.get('NO', i + 1)),
            'PERIODE': str(periode),
            'TANGGAL': tanggal,
            'JENIS PERKARA': jenis_perkara,
            'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',
            'KETERANGAN': str(keterangan)
        }
        
        prepared_data.append(prepared_row)
    
    return prepared_data