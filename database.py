import sqlite3
import os
from contextlib import contextmanager

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
                pra_penututan TEXT NOT NULL,
                penuntutan TEXT NOT NULL,
                upaya_hukum TEXT NOT NULL,
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
            INSERT INTO pidum_data (no, periode, tanggal, jenis_perkara, pra_penututan, penuntutan, upaya_hukum)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['NO'], data['PERIODE'], data['TANGGAL'], data['JENIS PERKARA'], 
              data['PRA PENUTUTAN'], data['PENUNTUTAN'], data['UPAYA HUKUM']))
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
            'PRA PENUTUTAN': row['pra_penututan'],
            'PENUNTUTAN': row['penuntutan'],
            'UPAYA HUKUM': row['upaya_hukum']
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