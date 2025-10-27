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
            'KETERANGAN': row['keterangan']
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

def delete_all_pidsus_data():
    """Delete all PIDSUS data (for testing)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pidsus_data')
        conn.commit()

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