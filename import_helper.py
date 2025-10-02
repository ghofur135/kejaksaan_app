import pandas as pd
import io
from werkzeug.utils import secure_filename
import os
from datetime import datetime

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_import_file(file, tahapan_penanganan=None):
    """Process uploaded file and return data for preview"""
    try:
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        # Read file based on extension
        if file_ext == 'csv':
            df = pd.read_csv(file)
        elif file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format")
        
        # Convert DataFrame to list of dictionaries for easier handling
        data = df.to_dict('records')
        
        # Clean and standardize column names
        standardized_data = []
        for i, row in enumerate(data):
            # Create standardized row with expected columns
            std_row = {
                'ROW_INDEX': i,
                'NO': '',
                'PERIODE': '',
                'TANGGAL': '',
                'JENIS_PERKARA_ORIGINAL': '',
                'KETERANGAN': '',
                'TAHAPAN_PENANGANAN': tahapan_penanganan or 'PRA PENUNTUTAN'
            }
            
            # Handle Tindak_Pidana_Didakwakan for jenis perkara analysis
            tindak_pidana = ''
            
            for key, value in row.items():
                # Clean key names (remove spaces, convert to uppercase)
                clean_key = str(key).strip().upper()
                clean_value = str(value).strip() if pd.notna(value) else ''
                
                # Map common column variations to standard names
                if any(keyword in clean_key for keyword in ['NO', 'NOMOR', 'NUMBER']) and 'REGISTER' not in clean_key:
                    # Only use simple number, not the full register format
                    if clean_value.isdigit():
                        std_row['NO'] = clean_value
                    else:
                        std_row['NO'] = str(i + 1)
                elif 'PERIODE' in clean_key:
                    std_row['PERIODE'] = clean_value
                elif any(keyword in clean_key for keyword in ['TANGGAL', 'DATE', 'TGL']) and 'REGISTER' not in clean_key:
                    std_row['TANGGAL'] = clean_value
                elif any(keyword in clean_key for keyword in ['JENIS', 'KATEGORI', 'TYPE']):
                    std_row['JENIS_PERKARA_ORIGINAL'] = clean_value
                elif 'TINDAK_PIDANA_DIDAKWAKAN' in clean_key:
                    # This is the main source for jenis perkara analysis
                    tindak_pidana = clean_value
                    std_row['JENIS_PERKARA_ORIGINAL'] = clean_value
                    if std_row['KETERANGAN']:
                        std_row['KETERANGAN'] = f"Pasal: {clean_value} | {std_row['KETERANGAN']}"
                    else:
                        std_row['KETERANGAN'] = f"Pasal: {clean_value}"
                elif any(keyword in clean_key for keyword in ['KETERANGAN', 'DESCRIPTION', 'PASAL', 'NOTE', 'PELANGGARAN']):
                    std_row['KETERANGAN'] = clean_value
                # Handle specific format for penuntutan data
                elif 'NO_TANGGAL_REGISTER_PERKARA' in clean_key:
                    # Extract date from register format like "PDM-\n22/PRBAL/Enz.2/09/2025\n2025-09-01"
                    register_value = clean_value
                    if '\n' in register_value:
                        parts = register_value.split('\n')
                        # Look for the date part (format YYYY-MM-DD)
                        for part in parts:
                            part = part.strip()
                            if len(part) == 10 and part.count('-') == 2:  # Format YYYY-MM-DD
                                try:
                                    # Validate it's a proper date
                                    year, month, day = part.split('-')
                                    if len(year) == 4 and len(month) == 2 and len(day) == 2:
                                        std_row['TANGGAL'] = part
                                        break
                                except:
                                    continue
                    else:
                        # If no newline, try to extract date from the register number itself
                        # Look for pattern like "/09/2025" in "PDM-22/PRBAL/Enz.2/09/2025"
                        parts = register_value.split('/')
                        if len(parts) >= 3:
                            month = parts[-2].zfill(2) if parts[-2].isdigit() else '01'
                            year = parts[-1] if parts[-1].isdigit() else '2025'
                            std_row['TANGGAL'] = f"{year}-{month}-01"
                elif 'IDENTITAS_TERSANGKA' in clean_key:
                    # Store suspect identity as part of keterangan
                    if std_row['KETERANGAN']:
                        std_row['KETERANGAN'] += f" | Tersangka: {clean_value}"
                    else:
                        std_row['KETERANGAN'] = f"Tersangka: {clean_value}"
                elif 'JAKSA_PENUNTUT_UMUM' in clean_key:
                    # Store prosecutor information as part of keterangan
                    if std_row['KETERANGAN']:
                        std_row['KETERANGAN'] += f" | JPU: {clean_value}"
                    else:
                        std_row['KETERANGAN'] = f"JPU: {clean_value}"
            
            # Use tindak pidana for jenis perkara suggestion if available
            if tindak_pidana and not std_row['JENIS_PERKARA_ORIGINAL']:
                std_row['JENIS_PERKARA_ORIGINAL'] = tindak_pidana
            
            # If no explicit NO, use row index + 1
            if not std_row['NO']:
                std_row['NO'] = str(i + 1)
            
            # If no explicit PERIODE, default to 1
            if not std_row['PERIODE']:
                std_row['PERIODE'] = '1'
            
            # If no explicit TANGGAL, use current date
            if not std_row['TANGGAL']:
                std_row['TANGGAL'] = datetime.now().strftime('%Y-%m-%d')
            
            standardized_data.append(std_row)
        
        return {
            'success': True,
            'data': standardized_data,
            'total_rows': len(standardized_data),
            'columns': list(df.columns) if not df.empty else []
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': [],
            'total_rows': 0,
            'columns': []
        }

def get_jenis_perkara_suggestions(original_text):
    """Suggest jenis perkara based on original text"""
    if not original_text:
        return "PERKARA LAINNYA"
    
    text = str(original_text).upper()
    
    # Mapping suggestions based on keywords
    mappings = {
        'NARKOBA': ['NARKOBA', 'NARKOTIKA', 'DRUGS', 'SABU', 'GANJA', 'UU NO. 35 TAHUN 2009', 'UU NO.35 TAHUN 2009', 'PASAL 112', 'PASAL 114', 'PASAL 119', 'PASAL 117', 'PASAL 120', 'PASAL 127'],
        'PERKARA ANAK': ['ANAK', 'JUVENILE', 'MINOR', 'REMAJA', 'UU NO. 23 TAHUN 2002', 'UU NO.23 TAHUN 2002'],
        'KESUSILAAN': ['KESUSILAAN', 'SUSILA', 'MORAL', 'CABUL', 'PERKOSAAN', 'PASAL 289', 'PASAL 81'],
        'JUDI': ['JUDI', 'GAMBLING', 'TOGEL', 'TARUHAN'],
        'KDRT': ['KDRT', 'KEKERASAN DALAM RUMAH TANGGA', 'DOMESTIC VIOLENCE'],
        'OHARDA': ['OHARDA', 'ORANG HILANG', 'HARTA BENDA', 'PASAL 372', 'PASAL 378', 'PASAL 362', 'PASAL 363'],
        'PERKARA LAINNYA': ['KUHP', 'PASAL 351', 'UU NO. 36 TAHUN 2009', 'UU NO.36 TAHUN 2009', 'PASAL 196', 'UU NO. 17 TAHUN 2016', 'UU NO.17 TAHUN 2016'],
    }
    
    for category, keywords in mappings.items():
        for keyword in keywords:
            if keyword in text:
                return category
    
    return "PERKARA LAINNYA"

def prepare_import_data(import_data, jenis_perkara_mapping):
    """Prepare data for database insertion with selected jenis perkara"""
    prepared_data = []
    
    for i, row in enumerate(import_data):
        # Get selected jenis perkara from mapping
        selected_jenis_perkara = jenis_perkara_mapping.get(str(i), "PERKARA LAINNYA")
        
        # Format tanggal
        tanggal = row.get('TANGGAL', '')
        if tanggal:
            try:
                # Try to parse various date formats
                if isinstance(tanggal, str):
                    # Try common date formats
                    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y']:
                        try:
                            parsed_date = datetime.strptime(tanggal, fmt)
                            tanggal = parsed_date.strftime('%Y-%m-%d')
                            break
                        except ValueError:
                            continue
                elif hasattr(tanggal, 'date'):  # pandas datetime
                    tanggal = tanggal.strftime('%Y-%m-%d')
            except:
                tanggal = datetime.now().strftime('%Y-%m-%d')
        else:
            tanggal = datetime.now().strftime('%Y-%m-%d')
        
        prepared_row = {
            'NO': str(row.get('NO', '')),
            'PERIODE': str(row.get('PERIODE', '')),
            'TANGGAL': tanggal,
            'JENIS PERKARA': selected_jenis_perkara,
            'TAHAPAN_PENANGANAN': row.get('TAHAPAN_PENANGANAN', 'PRA PENUNTUTAN'),
            'KETERANGAN': str(row.get('KETERANGAN', ''))
        }
        
        prepared_data.append(prepared_row)
    
    return prepared_data