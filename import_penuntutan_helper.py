"""
Import Helper khusus untuk data Penuntutan
Format CSV: No,No_Tanggal_Register_Perkara,Identitas_Tersangka,Tindak_Pidana_Didakwakan,Jaksa_Penuntut_Umum
"""

import pandas as pd
import io
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import re

def allowed_file_penuntutan(filename):
    """Check if uploaded file has allowed extension for penuntutan"""
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_date_from_register(no_tanggal_register):
    """Extract date from No_Tanggal_Register_Perkara field like 'PDM- 10/PRBAL/Eoh.2/07/2025 2025-07-02'"""
    if not no_tanggal_register:
        return datetime.now().strftime('%Y-%m-%d')
    
    # Look for date pattern YYYY-MM-DD at the end
    date_pattern = r'(\d{4}-\d{2}-\d{2})$'
    match = re.search(date_pattern, str(no_tanggal_register))
    
    if match:
        return match.group(1)
    
    # If no date found, try to extract from register format
    # Example: PDM- 10/PRBAL/Eoh.2/07/2025
    parts = str(no_tanggal_register).split('/')
    if len(parts) >= 3:
        try:
            # Try to get month and year from the register format
            month_part = parts[-2] if len(parts) > 2 else '01'
            year_part = parts[-1] if len(parts) > 1 else '2025'
            
            # Clean up the year part (might have extra spaces or date)
            year_clean = re.search(r'\d{4}', year_part)
            if year_clean:
                year = year_clean.group(0)
                month = month_part.strip().zfill(2)
                return f"{year}-{month}-01"
        except:
            pass
    
    # Default to current date if extraction fails
    return datetime.now().strftime('%Y-%m-%d')

def get_jenis_perkara_suggestions_penuntutan(tindak_pidana_text):
    """Suggest jenis perkara based on tindak pidana text for penuntutan data"""
    if not tindak_pidana_text:
        return "PERKARA LAINNYA"
    
    text = str(tindak_pidana_text).upper()
    
    # Enhanced mapping with more specific patterns for penuntutan
    mappings = {
        'NARKOBA': [
            'NARKOTIKA', 'NARKOBA', 'PASAL 112', 'PASAL 114', 'PASAL 127', 'PASAL 117', 'PASAL 119', 'PASAL 120',
            'UU NO. 35 TAHUN 2009', 'UU NOMOR 35 TAHUN 2009'
        ],
        'PERKARA ANAK': [
            'ANAK', 'JUVENILE', 'MINOR', 'REMAJA', 'UU NO. 23 TAHUN 2002', 'UU NOMOR 23 TAHUN 2002',
            'UU NO. 17 TAHUN 2016', 'UU NOMOR 17 TAHUN 2016'
        ],
        'KESUSILAAN': [
            'KESUSILAAN', 'SUSILA', 'MORAL', 'CABUL', 'PERKOSAAN', 'PEMERCABULAN',
            'PASAL 289', 'PASAL 285', 'PASAL 287', 'PASAL 81'
        ],
        'OHARDA': [
            'PASAL 362', 'PASAL 363', 'PASAL 365', 'PASAL 368', 'PASAL 372', 'PASAL 374', 'PASAL 378',
            'PENCURIAN', 'PENGGELAPAN', 'PENIPUAN', 'PEMERASAN', 'KUHP'
        ],
        'JUDI': [
            'JUDI', 'GAMBLING', 'TOGEL', 'TARUHAN'
        ],
        'KDRT': [
            'KDRT', 'KEKERASAN DALAM RUMAH TANGGA', 'DOMESTIC VIOLENCE',
            'PASAL 351', 'PENGANIAYAAN'
        ],
        'PERKARA LAINNYA': [
            'PERLINDUNGAN DATA PRIBADI', 'UU NO. 27 TAHUN 2022', 'PASAL 67', 'PASAL 65',
            'MINYAK DAN GAS BUMI', 'UU NO. 22 TAHUN 2021', 'PERLINDUNGAN KONSUMEN',
            'UU NO. 8 TAHUN 1999', 'METROLOGI LEGAL', 'UU NO. 2 TAHUN 1981',
            'JAMINAN FIDUSIA', 'UU NO. 42 TAHUN 1999'
        ]
    }
    
    # Check each category
    for category, keywords in mappings.items():
        for keyword in keywords:
            if keyword in text:
                return category
    
    return "PERKARA LAINNYA"

def process_penuntutan_import_file(file):
    """Process uploaded file specifically for penuntutan format"""
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
        required_columns = ['No', 'No_Tanggal_Register_Perkara', 'Identitas_Tersangka', 'Tindak_Pidana_Didakwakan', 'Jaksa_Penuntut_Umum']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Kolom yang diperlukan tidak ditemukan: {', '.join(missing_columns)}")
        
        # Convert DataFrame to standardized format
        standardized_data = []
        
        for i, row in df.iterrows():
            # Extract and clean data
            no = str(row.get('No', i + 1)).strip()
            no_tanggal_register = str(row.get('No_Tanggal_Register_Perkara', '')).strip()
            identitas_tersangka = str(row.get('Identitas_Tersangka', '')).strip()
            tindak_pidana_didakwakan = str(row.get('Tindak_Pidana_Didakwakan', '')).strip()
            jaksa_penuntut_umum = str(row.get('Jaksa_Penuntut_Umum', '')).strip()
            
            # Extract date from No_Tanggal_Register_Perkara
            extracted_date = extract_date_from_register(no_tanggal_register)
            
            # Build detailed keterangan
            keterangan_parts = []
            if no_tanggal_register:
                keterangan_parts.append(f"Register: {no_tanggal_register}")
            if identitas_tersangka:
                keterangan_parts.append(f"Tersangka: {identitas_tersangka}")
            if tindak_pidana_didakwakan:
                keterangan_parts.append(f"Pasal: {tindak_pidana_didakwakan}")
            if jaksa_penuntut_umum:
                keterangan_parts.append(f"JPU: {jaksa_penuntut_umum}")
            
            keterangan = " | ".join(keterangan_parts)
            
            # Create standardized row
            std_row = {
                'ROW_INDEX': i,
                'NO': no,
                'PERIODE': '1',  # Default periode
                'TANGGAL': extracted_date,
                'JENIS_PERKARA_ORIGINAL': tindak_pidana_didakwakan,
                'KETERANGAN': keterangan,
                'TAHAPAN_PENANGANAN': 'PENUNTUTAN',
                'NO_TANGGAL_REGISTER_ORIGINAL': no_tanggal_register,
                'IDENTITAS_TERSANGKA_ORIGINAL': identitas_tersangka,
                'TINDAK_PIDANA_ORIGINAL': tindak_pidana_didakwakan,
                'JAKSA_PENUNTUT_UMUM_ORIGINAL': jaksa_penuntut_umum
            }
            
            # Get suggested jenis perkara
            suggestion = get_jenis_perkara_suggestions_penuntutan(tindak_pidana_didakwakan)
            std_row['SUGGESTED_JENIS_PERKARA'] = suggestion
            
            standardized_data.append(std_row)
        
        return {
            'success': True,
            'data': standardized_data,
            'total_rows': len(standardized_data),
            'columns': list(df.columns) if not df.empty else [],
            'format_type': 'penuntutan'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': [],
            'total_rows': 0,
            'columns': [],
            'format_type': 'penuntutan'
        }

def prepare_penuntutan_data_for_db(import_data, form_data):
    """Prepare penuntutan data for database insertion"""
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
            'TAHAPAN_PENANGANAN': 'PENUNTUTAN',
            'KETERANGAN': str(keterangan)
        }
        
        prepared_data.append(prepared_row)
    
    return prepared_data