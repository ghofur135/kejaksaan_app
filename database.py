import sqlite3
import os
from contextlib import contextmanager
import hashlib

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'db', 'kejaksaan.db')

def init_database():
    """Initialize database with required tables"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        
        # Create PIDUM table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pidum_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                no TEXT NOT NULL,
                periode TEXT NOT NULL,
                tanggal TEXT NOT NULL,
                jenis_perkara TEXT NOT NULL,
                tahapan_penanganan TEXT NOT NULL,
                keterangan TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create PIDSUS table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pidsus_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                no TEXT NOT NULL,
                periode TEXT NOT NULL,
                tanggal TEXT NOT NULL,
                jenis_perkara TEXT NOT NULL,
                penyidikan TEXT NOT NULL,
                penuntutan TEXT NOT NULL,
                keterangan TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create users table for authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default admin user if not exists
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            # Hash the default password
            hashed_password = hashlib.sha256('P@ssw0rd25#!'.encode()).hexdigest()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                          ('admin', hashed_password))
        
        conn.commit()

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def insert_pidum_data(data):
    """Insert PIDUM data into database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pidum_data (no, periode, tanggal, jenis_perkara, tahapan_penanganan, keterangan)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['NO'], data['PERIODE'], data['TANGGAL'], data['JENIS PERKARA'],
              data['TAHAPAN_PENANGANAN'], data['KETERANGAN']))
        conn.commit()
        return cursor.lastrowid

def insert_pidsus_data(data):
    """Insert PIDSUS data into database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pidsus_data (no, periode, tanggal, jenis_perkara, penyidikan, penuntutan, keterangan)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['NO'], data['PERIODE'], data['TANGGAL'], data['JENIS PERKARA'],
              data['PENYIDIKAN'], data['PENUNTUTAN'], data['KETERANGAN']))
        conn.commit()
        return cursor.lastrowid

def get_all_pidum_data():
    """Get all PIDUM data from database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pidum_data ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries (compatible with existing code)
        return [dict(row) for row in rows]

def get_all_pidsus_data():
    """Get all PIDSUS data from database"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pidsus_data ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries (compatible with existing code)
        return [dict(row) for row in rows]

def get_pidum_data_for_export():
    """Get PIDUM data formatted for export (without id and timestamp)"""
    data = get_all_pidum_data()
    export_data = []
    for row in data:
        export_data.append({
            'NO': row['no'],
            'PERIODE': row['periode'],
            'TANGGAL': row['tanggal'],
            'JENIS PERKARA': row['jenis_perkara'],
            'TAHAPAN PENANGANAN': row['tahapan_penanganan'],
            'KETERANGAN': row['keterangan']
        })
    return export_data

def get_pidsus_data_for_export():
    """Get PIDSUS data formatted for export (without id and timestamp)"""
    data = get_all_pidsus_data()
    export_data = []
    for row in data:
        export_data.append({
            'NO': row['no'],
            'PERIODE': row['periode'],
            'TANGGAL': row['tanggal'],
            'JENIS PERKARA': row['jenis_perkara'],
            'PENYIDIKAN': row['penyidikan'],
            'PENUNTUTAN': row['penuntutan'],
            'KETERANGAN': row['keterangan'],
            'id': row['id']  # Add ID for edit/delete functionality
        })
    return export_data

def delete_all_pidum_data():
    """Delete all PIDUM data (for testing)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pidum_data')
        conn.commit()
        return cursor.rowcount

def delete_pidum_item(item_id):
    """Delete single PIDUM item by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pidum_data WHERE id = ?', (item_id,))
        conn.commit()
        return cursor.rowcount > 0

def update_pidum_data(item_id, data):
    """Update PIDUM data by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE pidum_data
            SET no=?, periode=?, tanggal=?, jenis_perkara=?, tahapan_penanganan=?, keterangan=?
            WHERE id=?
        ''', (data['NO'], data['PERIODE'], data['TANGGAL'], data['JENIS PERKARA'],
              data['TAHAPAN_PENANGANAN'], data['KETERANGAN'], item_id))
        conn.commit()
        return cursor.rowcount > 0

def get_pidum_data_by_id(item_id):
    """Get single PIDUM data by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pidum_data WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_pidsus_data_by_id(item_id):
    """Get single PIDSUS data by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pidsus_data WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_pidsus_data(item_id, data):
    """Update PIDSUS data by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE pidsus_data
            SET no=?, periode=?, tanggal=?, jenis_perkara=?, penyidikan=?, penuntutan=?, keterangan=?
            WHERE id=?
        ''', (data['NO'], data['PERIODE'], data['TANGGAL'], data['JENIS PERKARA'],
              data['PENYIDIKAN'], data['PENUNTUTAN'], data['KETERANGAN'], item_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_pidsus_item(item_id):
    """Delete single PIDSUS item by ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pidsus_data WHERE id = ?', (item_id,))
        conn.commit()
        return cursor.rowcount > 0

def delete_all_pidsus_data():
    """Delete all PIDSUS data (for testing)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM pidsus_data')
        count = cursor.fetchone()[0]
        
        cursor.execute('DELETE FROM pidsus_data')
        conn.commit()
        
        return count

def get_database_stats():
    """Get database statistics"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM pidum_data')
        pidum_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM pidsus_data')
        pidsus_count = cursor.fetchone()[0]
        
        return {
            'pidum_count': pidum_count,
            'pidsus_count': pidsus_count,
            'database_path': DATABASE_PATH
        }

def get_pidum_data_by_tahapan(tahapan_penanganan):
    """Get PIDUM data filtered by tahapan penanganan"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pidum_data WHERE tahapan_penanganan = ? ORDER BY created_at DESC', (tahapan_penanganan,))
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries (compatible with existing code)
        return [dict(row) for row in rows]

def get_pidum_report_data(bulan=None, tahun=None):
    """Get PIDUM report data aggregated by jenis perkara and tahapan"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Base query
        query = '''
            SELECT 
                jenis_perkara,
                tahapan_penanganan,
                COUNT(*) as jumlah,
                strftime('%m', tanggal) as bulan,
                strftime('%Y', tanggal) as tahun
            FROM pidum_data
        '''
        
        params = []
        conditions = []
        
        if bulan:
            conditions.append("strftime('%m', tanggal) = ?")
            params.append(f"{bulan:02d}")
        
        if tahun:
            conditions.append("strftime('%Y', tanggal) = ?")
            params.append(str(tahun))
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += '''
            GROUP BY jenis_perkara, tahapan_penanganan, strftime('%m', tanggal), strftime('%Y', tanggal)
            ORDER BY jenis_perkara, tahapan_penanganan
        '''
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Organize data by jenis_perkara
        report_data = {}
        
        # Initialize all jenis perkara with zero values
        jenis_perkara_list = ['NARKOBA', 'PERKARA ANAK', 'KESUSILAAN', 'JUDI', 'KDRT', 'OHARDA', 'PERKARA LAINNYA']
        tahapan_list = ['PRA PENUNTUTAN', 'PENUNTUTAN', 'UPAYA HUKUM']
        
        for jenis in jenis_perkara_list:
            report_data[jenis] = {
                'jenis_perkara': jenis,
                'PRA PENUNTUTAN': 0,
                'PENUNTUTAN': 0,
                'UPAYA HUKUM': 0,
                'JUMLAH': 0
            }
        
        # Fill in actual data
        for row in rows:
            jenis = row['jenis_perkara']
            tahapan = row['tahapan_penanganan']
            jumlah = row['jumlah']
            
            if jenis not in report_data:
                report_data[jenis] = {
                    'jenis_perkara': jenis,
                    'PRA PENUNTUTAN': 0,
                    'PENUNTUTAN': 0,
                    'UPAYA HUKUM': 0,
                    'JUMLAH': 0
                }
            
            report_data[jenis][tahapan] = jumlah
            report_data[jenis]['JUMLAH'] += jumlah
        
        # Convert to list and add row numbers
        result = []
        for i, jenis in enumerate(jenis_perkara_list, 1):
            data = report_data[jenis]
            data['NO'] = i
            result.append(data)
        
        return result

def authenticate_user(username, password):
    """Authenticate user credentials"""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username FROM users WHERE username = ? AND password = ?',
                      (username, hashed_password))
        user = cursor.fetchone()
        
        return dict(user) if user else None

def get_pidsus_report_data(bulan=None, tahun=None):
    """Get PIDSUS report data aggregated by jenis perkara and tahapan"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Base query
        query = '''
            SELECT
                jenis_perkara,
                penyidikan,
                penuntutan,
                COUNT(*) as jumlah,
                strftime('%m', tanggal) as bulan,
                strftime('%Y', tanggal) as tahun
            FROM pidsus_data
        '''
        
        params = []
        conditions = []
        
        if bulan:
            conditions.append("strftime('%m', tanggal) = ?")
            params.append(f"{bulan:02d}")
        
        if tahun:
            conditions.append("strftime('%Y', tanggal) = ?")
            params.append(str(tahun))
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += '''
            GROUP BY jenis_perkara, penyidikan, penuntutan, strftime('%m', tanggal), strftime('%Y', tanggal)
            ORDER BY jenis_perkara, penyidikan, penuntutan
        '''
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Organize data by jenis_perkara
        report_data = {}
        
        # Initialize all jenis perkara with zero values
        jenis_perkara_list = ['KORUPSI', 'TINDAK PIDANA KORUPSI', 'PENYALAHGUNAAN WEWENANG', 'GRATIFIKASI', 'SUAP', 'PENGGELEMBUNGAN PAJAK', 'PERKARA LAINNYA']
        
        for jenis in jenis_perkara_list:
            report_data[jenis] = {
                'jenis_perkara': jenis,
                'PENYIDIKAN': 0,
                'PENUNTUTAN': 0,
                'JUMLAH': 0
            }
        
        # Fill in actual data
        for row in rows:
            jenis = row['jenis_perkara']
            penyidikan_val = row['penyidikan']
            penuntutan_val = row['penuntutan']
            jumlah = row['jumlah']
            
            if jenis not in report_data:
                report_data[jenis] = {
                    'jenis_perkara': jenis,
                    'PENYIDIKAN': 0,
                    'PENUNTUTAN': 0,
                    'JUMLAH': 0
                }
            
            # Count based on penyidikan and penuntutan values
            if penyidikan_val == '1':
                report_data[jenis]['PENYIDIKAN'] += jumlah
            if penuntutan_val == '1':
                report_data[jenis]['PENUNTUTAN'] += jumlah
            
            report_data[jenis]['JUMLAH'] += jumlah
        
        # Convert to list and add row numbers
        result = []
        for i, jenis in enumerate(jenis_perkara_list, 1):
            data = report_data[jenis]
            data['NO'] = i
            result.append(data)
        
        return result

def get_pidsus_report_data_bulanan(tahun=None, bulan=None):
    """Get PIDSUS report data for monthly report with chart data"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Build query with year and optional month filter
        where_conditions = ["strftime('%Y', tanggal) = ?"]
        params = [str(tahun)]
        
        if bulan:
            where_conditions.append("strftime('%m', tanggal) = ?")
            params.append(f"{bulan:02d}")
        
        where_clause = "WHERE " + " AND ".join(where_conditions)
        
        # Get data from pidsus_data table
        query = f"""
        SELECT periode, jenis_perkara, tanggal, penyidikan, penuntutan,
               strftime('%m', tanggal) as bulan_num,
               CASE strftime('%m', tanggal)
                   WHEN '01' THEN 'Januari'
                   WHEN '02' THEN 'Februari'
                   WHEN '03' THEN 'Maret'
                   WHEN '04' THEN 'April'
                   WHEN '05' THEN 'Mei'
                   WHEN '06' THEN 'Juni'
                   WHEN '07' THEN 'Juli'
                   WHEN '08' THEN 'Agustus'
                   WHEN '09' THEN 'September'
                   WHEN '10' THEN 'Oktober'
                   WHEN '11' THEN 'November'
                   WHEN '12' THEN 'Desember'
               END as bulan_nama
        FROM pidsus_data {where_clause}
        ORDER BY bulan_num, jenis_perkara
        """
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Get available months for filter dropdown
        month_query = f"""
        SELECT DISTINCT strftime('%m', tanggal) as bulan_num,
               CASE strftime('%m', tanggal)
                   WHEN '01' THEN 'Januari'
                   WHEN '02' THEN 'Februari'
                   WHEN '03' THEN 'Maret'
                   WHEN '04' THEN 'April'
                   WHEN '05' THEN 'Mei'
                   WHEN '06' THEN 'Juni'
                   WHEN '07' THEN 'Juli'
                   WHEN '08' THEN 'Agustus'
                   WHEN '09' THEN 'September'
                   WHEN '10' THEN 'Oktober'
                   WHEN '11' THEN 'November'
                   WHEN '12' THEN 'Desember'
               END as bulan_nama
        FROM pidsus_data
        WHERE strftime('%Y', tanggal) = ?
        ORDER BY bulan_num
        """
        
        cursor.execute(month_query, [str(tahun)])
        available_months = cursor.fetchall()
        
        # Define all categories that should always appear
        predefined_categories = ['TIPIKOR', 'KEPABEANAN', 'BEA CUKAI', 'TPPU', 'PERPAJAKAN', 'PERKARA LAINNYA']
        
        # Get all months that should be displayed
        month_names = {
            1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
            5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
            9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
        }
        
        # Determine which months to display
        if bulan:
            display_months = [month_names.get(bulan, 'Januari')]
        else:
            # Show all months that have data or all 12 months if no specific month is selected
            months_with_data = set()
            for month in available_months:
                months_with_data.add(month['bulan_nama'])
            
            # If no specific month is selected, show all months that have data
            display_months = list(months_with_data) if months_with_data else list(month_names.values())
        
        # Process data for report
        data_summary = {}
        
        # Process data for charts by tahapan
        chart_data = {
            'penyidikan': {},
            'penuntutan': {}
        }
        
        # Normalisasi mapping untuk jenis perkara
        def normalize_jenis_perkara(jenis_text):
            if not jenis_text:
                return 'PERKARA LAINNYA'
            jenis_upper = jenis_text.upper().strip()
            if 'TIPIKOR' in jenis_upper or 'TINDAK PIDANA KORUPSI' in jenis_upper or 'TPK' in jenis_upper:
                return 'TIPIKOR'
            if 'KEPABEA' in jenis_upper:
                return 'KEPABEANAN'
            if 'BEA CUKAI' in jenis_upper or ('CUKAI' in jenis_upper and 'BEA' in jenis_upper):
                return 'BEA CUKAI'
            if 'TPPU' in jenis_upper or ('PENCUCIAN' in jenis_upper and 'UANG' in jenis_upper):
                return 'TPPU'
            if 'PAJAK' in jenis_upper or 'PERPAJAKAN' in jenis_upper:
                return 'PERPAJAKAN'
            return 'PERKARA LAINNYA'
        
        for row in rows:
            normalized = normalize_jenis_perkara(row['jenis_perkara'])
            key = (row['bulan_nama'], normalized)
            
            # Initialize data structure if not exists
            if key not in data_summary:
                data_summary[key] = {
                    'BULAN': row['bulan_nama'],
                    'JENIS_PERKARA': normalized,
                    'JUMLAH': 0,
                    'PENYIDIKAN': 0,
                    'PENUNTUTAN': 0
                }
            
            # Update data summary
            if row['penyidikan'] == '1':
                data_summary[key]['PENYIDIKAN'] += 1
                chart_data['penyidikan'][normalized] = chart_data['penyidikan'].get(normalized, 0) + 1
            if row['penuntutan'] == '1':
                data_summary[key]['PENUNTUTAN'] += 1
                chart_data['penuntutan'][normalized] = chart_data['penuntutan'].get(normalized, 0) + 1
            
            data_summary[key]['JUMLAH'] = data_summary[key]['PENYIDIKAN'] + data_summary[key]['PENUNTUTAN']
        
        # Ensure all predefined categories are present for each month
        for month in display_months:
            for category in predefined_categories:
                key = (month, category)
                if key not in data_summary:
                    data_summary[key] = {
                        'BULAN': month,
                        'JENIS_PERKARA': category,
                        'JUMLAH': 0,
                        'PENYIDIKAN': 0,
                        'PENUNTUTAN': 0
                    }
        
        # Ensure all categories are present in chart data
        for category in predefined_categories:
            if category not in chart_data['penyidikan']:
                chart_data['penyidikan'][category] = 0
            if category not in chart_data['penuntutan']:
                chart_data['penuntutan'][category] = 0
        
        # Convert to list and sort
        report_data = list(data_summary.values())
        
        # Sort by month order, then by category order
        month_order = {name: i for i, name in enumerate(month_names.values())}
        category_order = {cat: i for i, cat in enumerate(predefined_categories)}
        
        report_data.sort(key=lambda x: (month_order.get(x['BULAN'], 0), category_order.get(x['JENIS_PERKARA'], 0)))
        
        return {
            'report_data': report_data,
            'available_months': available_months,
            'chart_data': chart_data
        }

def create_user(username, password):
    """Create a new user"""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                          (username, hashed_password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False