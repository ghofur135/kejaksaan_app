import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
import hashlib
from config import Config

class MySQLDatabase:
    """MySQL Database operations for Kejaksaan Application"""
    
    def __init__(self):
        self.config = Config.get_mysql_connection_params()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = mysql.connector.connect(**self.config)
            conn.row_factory = lambda cursor, row: dict(zip(cursor.column_names, row))
            yield conn
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise
        finally:
            if conn and conn.is_connected():
                conn.close()
    
    def init_database(self):
        """Initialize database with required tables and run migrations"""
        # Run migrations to ensure schema is up to date
        self._run_migrations()

    def _run_migrations(self):
        """Run database migrations to ensure schema is up to date"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)

                # Check if identitas_tersangka column exists in pidum_data
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = 'pidum_data'
                    AND COLUMN_NAME = 'identitas_tersangka'
                """)
                result = cursor.fetchone()

                if result['count'] == 0:
                    # Add the column
                    print("Migration: Adding 'identitas_tersangka' column to pidum_data...")
                    cursor.execute("""
                        ALTER TABLE pidum_data
                        ADD COLUMN identitas_tersangka TEXT AFTER tahapan_penanganan
                    """)
                    conn.commit()
                    print("Migration completed: 'identitas_tersangka' column added.")

                # Create upaya_hukum_data table if not exists
                self._create_upaya_hukum_table(cursor, conn)

        except Exception as e:
            print(f"Migration check/update skipped: {e}")

    def _create_upaya_hukum_table(self, cursor, conn):
        """Create upaya_hukum_data table if not exists"""
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS upaya_hukum_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    no TEXT,
                    terdakwa_terpidana TEXT,
                    no_tanggal_rp9 TEXT,
                    jenis_perkara TEXT,
                    -- Perlawanan
                    perlawanan_no_tgl_penetapan_pn TEXT,
                    perlawanan_no_tgl_akte TEXT,
                    perlawanan_tgl_pengajuan_memori TEXT,
                    perlawanan_yang_mengajukan_jpu TEXT,
                    perlawanan_yang_mengajukan_terdakwa TEXT,
                    perlawanan_no_tgl_amar_penetapan_pt TEXT,
                    -- Banding
                    banding_no_tgl_akte_permohonan TEXT,
                    banding_tgl_pengajuan_memori TEXT,
                    banding_yang_mengajukan_jpu TEXT,
                    banding_yang_mengajukan_terdakwa TEXT,
                    banding_no_tgl_amar_putusan_pt TEXT,
                    -- Kasasi
                    kasasi_no_tgl_akte_permohonan TEXT,
                    kasasi_tgl_pengajuan_memori TEXT,
                    kasasi_yang_mengajukan_jpu TEXT,
                    kasasi_yang_mengajukan_terdakwa TEXT,
                    kasasi_no_tgl_amar_putusan_ma TEXT,
                    -- Kasasi Demi Hukum
                    kasasi_demi_hukum_tgl_diajukan TEXT,
                    kasasi_demi_hukum_keadaan_putusan_pn TEXT,
                    kasasi_demi_hukum_no_tgl_amar_putusan_ma TEXT,
                    -- PK
                    pk_tgl_diajukan_terpidana TEXT,
                    pk_tgl_pemeriksaan_berita_acara TEXT,
                    pk_no_tgl_amar_putusan TEXT,
                    -- Grasi
                    grasi_tgl_penerimaan_berkas TEXT,
                    grasi_tgl_penundaan_eksekusi TEXT,
                    grasi_tgl_risalah_pertimbangan_kajari TEXT,
                    grasi_tgl_terima_kepres TEXT,
                    grasi_no_tgl_kepres_amar TEXT,
                    -- Metadata
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("Migration: upaya_hukum_data table ensured.")
        except Exception as e:
            print(f"Create upaya_hukum_data table skipped: {e}")
    
    def insert_upaya_hukum_data(self, data):
        """Insert Upaya Hukum data into database"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = '''
                INSERT INTO upaya_hukum_data (
                    no, terdakwa_terpidana, no_tanggal_rp9, jenis_perkara,
                    perlawanan_no_tgl_penetapan_pn, perlawanan_no_tgl_akte, perlawanan_tgl_pengajuan_memori,
                    perlawanan_yang_mengajukan_jpu, perlawanan_yang_mengajukan_terdakwa, perlawanan_no_tgl_amar_penetapan_pt,
                    banding_no_tgl_akte_permohonan, banding_tgl_pengajuan_memori, banding_yang_mengajukan_jpu,
                    banding_yang_mengajukan_terdakwa, banding_no_tgl_amar_putusan_pt,
                    kasasi_no_tgl_akte_permohonan, kasasi_tgl_pengajuan_memori, kasasi_yang_mengajukan_jpu,
                    kasasi_yang_mengajukan_terdakwa, kasasi_no_tgl_amar_putusan_ma,
                    kasasi_demi_hukum_tgl_diajukan, kasasi_demi_hukum_keadaan_putusan_pn, kasasi_demi_hukum_no_tgl_amar_putusan_ma,
                    pk_tgl_diajukan_terpidana, pk_tgl_pemeriksaan_berita_acara, pk_no_tgl_amar_putusan,
                    grasi_tgl_penerimaan_berkas, grasi_tgl_penundaan_eksekusi, grasi_tgl_risalah_pertimbangan_kajari,
                    grasi_tgl_terima_kepres, grasi_no_tgl_kepres_amar
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (
                data.get('no', ''),
                data.get('terdakwa_terpidana', ''),
                data.get('no_tanggal_rp9', ''),
                data.get('jenis_perkara', ''),
                data.get('perlawanan_no_tgl_penetapan_pn', ''),
                data.get('perlawanan_no_tgl_akte', ''),
                data.get('perlawanan_tgl_pengajuan_memori', ''),
                data.get('perlawanan_yang_mengajukan_jpu', ''),
                data.get('perlawanan_yang_mengajukan_terdakwa', ''),
                data.get('perlawanan_no_tgl_amar_penetapan_pt', ''),
                data.get('banding_no_tgl_akte_permohonan', ''),
                data.get('banding_tgl_pengajuan_memori', ''),
                data.get('banding_yang_mengajukan_jpu', ''),
                data.get('banding_yang_mengajukan_terdakwa', ''),
                data.get('banding_no_tgl_amar_putusan_pt', ''),
                data.get('kasasi_no_tgl_akte_permohonan', ''),
                data.get('kasasi_tgl_pengajuan_memori', ''),
                data.get('kasasi_yang_mengajukan_jpu', ''),
                data.get('kasasi_yang_mengajukan_terdakwa', ''),
                data.get('kasasi_no_tgl_amar_putusan_ma', ''),
                data.get('kasasi_demi_hukum_tgl_diajukan', ''),
                data.get('kasasi_demi_hukum_keadaan_putusan_pn', ''),
                data.get('kasasi_demi_hukum_no_tgl_amar_putusan_ma', ''),
                data.get('pk_tgl_diajukan_terpidana', ''),
                data.get('pk_tgl_pemeriksaan_berita_acara', ''),
                data.get('pk_no_tgl_amar_putusan', ''),
                data.get('grasi_tgl_penerimaan_berkas', ''),
                data.get('grasi_tgl_penundaan_eksekusi', ''),
                data.get('grasi_tgl_risalah_pertimbangan_kajari', ''),
                data.get('grasi_tgl_terima_kepres', ''),
                data.get('grasi_no_tgl_kepres_amar', '')
            ))
            conn.commit()
            return cursor.lastrowid

    def get_all_upaya_hukum_data(self):
        """Get all Upaya Hukum data from database"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM upaya_hukum_data ORDER BY created_at DESC')
            rows = cursor.fetchall()
            return rows

    def delete_upaya_hukum_item(self, item_id):
        """Delete single Upaya Hukum item by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('DELETE FROM upaya_hukum_data WHERE id = %s', (item_id,))
            conn.commit()
            return cursor.rowcount > 0

    def insert_pidum_data(self, data):
        """Insert PIDUM data into database"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = '''
                INSERT INTO pidum_data (no, periode, tanggal, jenis_perkara, tahapan_penanganan, identitas_tersangka, keterangan)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (data['NO'], data['PERIODE'], data['TANGGAL'], data['JENIS PERKARA'],
                                  data['TAHAPAN_PENANGANAN'], data.get('IDENTITAS_TERSANGKA', ''), data['KETERANGAN']))
            conn.commit()
            return cursor.lastrowid
    
    def insert_pidsus_data(self, data):
        """Insert PIDSUS data into database"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = '''
                INSERT INTO pidsus_data (no, periode, tanggal, jenis_perkara, penyidikan, penuntutan, keterangan)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (data['NO'], data['PERIODE'], data['TANGGAL'], data['JENIS PERKARA'],
                                  data['PENYIDIKAN'], data['PENUNTUTAN'], data['KETERANGAN']))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_pidum_data(self):
        """Get all PIDUM data from database"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM pidum_data ORDER BY created_at DESC')
            rows = cursor.fetchall()
            return rows
    
    def get_all_pidsus_data(self):
        """Get all PIDSUS data from database"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM pidsus_data ORDER BY created_at DESC')
            rows = cursor.fetchall()
            return rows
    
    def get_pidum_data_for_export(self):
        """Get PIDUM data formatted for export (without id and timestamp)"""
        data = self.get_all_pidum_data()
        export_data = []
        for row in data:
            export_data.append({
                'NO': row['no'],
                'PERIODE': row['periode'],
                'TANGGAL': row['tanggal'],
                'JENIS PERKARA': row['jenis_perkara'],
                'TAHAPAN PENANGANAN': row['tahapan_penanganan'],
                'IDENTITAS TERSANGKA': row.get('identitas_tersangka', ''),
                'KETERANGAN': row['keterangan']
            })
        return export_data
    
    def get_pidsus_data_for_export(self):
        """Get PIDSUS data formatted for export (without id and timestamp)"""
        data = self.get_all_pidsus_data()
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
    
    def delete_all_pidum_data(self):
        """Delete all PIDUM data (for testing)"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('DELETE FROM pidum_data')
            conn.commit()
            return cursor.rowcount
    
    def delete_pidum_item(self, item_id):
        """Delete single PIDUM item by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('DELETE FROM pidum_data WHERE id = %s', (item_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def update_pidum_data(self, item_id, data):
        """Update PIDUM data by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = '''
                UPDATE pidum_data
                SET no=%s, periode=%s, tanggal=%s, jenis_perkara=%s, tahapan_penanganan=%s, identitas_tersangka=%s, keterangan=%s
                WHERE id=%s
            '''
            cursor.execute(query, (data['NO'], data['PERIODE'], data['TANGGAL'], data['JENIS PERKARA'],
                                  data['TAHAPAN_PENANGANAN'], data.get('IDENTITAS_TERSANGKA', ''), data['KETERANGAN'], item_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_pidum_data_by_id(self, item_id):
        """Get single PIDUM data by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM pidum_data WHERE id = %s', (item_id,))
            row = cursor.fetchone()
            return row if row else None
    
    def get_pidsus_data_by_id(self, item_id):
        """Get single PIDSUS data by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM pidsus_data WHERE id = %s', (item_id,))
            row = cursor.fetchone()
            return row if row else None
    
    def update_pidsus_data(self, item_id, data):
        """Update PIDSUS data by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = '''
                UPDATE pidsus_data
                SET no=%s, periode=%s, tanggal=%s, jenis_perkara=%s, penyidikan=%s, penuntutan=%s, keterangan=%s
                WHERE id=%s
            '''
            cursor.execute(query, (data['NO'], data['PERIODE'], data['TANGGAL'], data['JENIS PERKARA'],
                                  data['PENYIDIKAN'], data['PENUNTUTAN'], data['KETERANGAN'], item_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_pidsus_item(self, item_id):
        """Delete single PIDSUS item by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('DELETE FROM pidsus_data WHERE id = %s', (item_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_all_pidsus_data(self):
        """Delete all PIDSUS data (for testing)"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT COUNT(*) as count FROM pidsus_data')
            count = cursor.fetchone()['count']
            
            cursor.execute('DELETE FROM pidsus_data')
            conn.commit()
            
            return count
    
    def get_database_stats(self):
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute('SELECT COUNT(*) as pidum_count FROM pidum_data')
            pidum_result = cursor.fetchone()
            pidum_count = pidum_result['pidum_count']
            
            cursor.execute('SELECT COUNT(*) as pidsus_count FROM pidsus_data')
            pidsus_result = cursor.fetchone()
            pidsus_count = pidsus_result['pidsus_count']
            
            return {
                'pidum_count': pidum_count,
                'pidsus_count': pidsus_count,
                'database_path': 'MySQL Database'
            }
    
    def get_pidum_data_by_tahapan(self, tahapan_penanganan):
        """Get PIDUM data filtered by tahapan penanganan"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM pidum_data WHERE tahapan_penanganan = %s ORDER BY created_at DESC', 
                        (tahapan_penanganan,))
            rows = cursor.fetchall()
            return rows
    
    def get_pidum_report_data(self, bulan=None, tahun=None):
        """Get PIDUM report data aggregated by jenis perkara and tahapan
        Also includes data from upaya_hukum_data table for UPAYA HUKUM column
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)

            # Base query for pidum_data
            query = '''
                SELECT
                    jenis_perkara,
                    tahapan_penanganan,
                    COUNT(*) as jumlah,
                    DATE_FORMAT(tanggal, '%m') as bulan,
                    DATE_FORMAT(tanggal, '%Y') as tahun
                FROM pidum_data
            '''

            params = []
            conditions = []

            if bulan:
                conditions.append("DATE_FORMAT(tanggal, '%m') = %s")
                params.append(str(bulan).zfill(2))

            if tahun:
                conditions.append("DATE_FORMAT(tanggal, '%Y') = %s")
                params.append(str(tahun))

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += '''
                GROUP BY jenis_perkara, tahapan_penanganan, DATE_FORMAT(tanggal, '%m'), DATE_FORMAT(tanggal, '%Y')
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

            # Fill in actual data from pidum_data
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

            # Also query upaya_hukum_data table for UPAYA HUKUM counts
            try:
                upaya_query = '''
                    SELECT
                        jenis_perkara,
                        COUNT(*) as jumlah
                    FROM upaya_hukum_data
                '''

                upaya_params = []
                upaya_conditions = []

                if bulan:
                    upaya_conditions.append("DATE_FORMAT(created_at, '%m') = %s")
                    upaya_params.append(str(bulan).zfill(2))

                if tahun:
                    upaya_conditions.append("DATE_FORMAT(created_at, '%Y') = %s")
                    upaya_params.append(str(tahun))

                if upaya_conditions:
                    upaya_query += " WHERE " + " AND ".join(upaya_conditions)

                upaya_query += " GROUP BY jenis_perkara"

                cursor.execute(upaya_query, upaya_params)
                upaya_rows = cursor.fetchall()

                # Add upaya_hukum_data counts to UPAYA HUKUM column
                for row in upaya_rows:
                    jenis = row['jenis_perkara'] or 'PERKARA LAINNYA'
                    jumlah = row['jumlah']

                    if jenis not in report_data:
                        report_data[jenis] = {
                            'jenis_perkara': jenis,
                            'PRA PENUNTUTAN': 0,
                            'PENUNTUTAN': 0,
                            'UPAYA HUKUM': 0,
                            'JUMLAH': 0
                        }

                    report_data[jenis]['UPAYA HUKUM'] += jumlah
                    report_data[jenis]['JUMLAH'] += jumlah

            except Exception as e:
                # If upaya_hukum_data table doesn't exist yet, just continue
                print(f"Note: Could not query upaya_hukum_data: {e}")

            # Convert to list and add row numbers
            result = []
            for i, jenis in enumerate(jenis_perkara_list, 1):
                data = report_data[jenis]
                data['NO'] = i
                result.append(data)

            return result
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT id, username FROM users WHERE username = %s AND password = %s',
                          (username, hashed_password))
            user = cursor.fetchone()
            
            return user if user else None
    
    def get_pidsus_report_data(self, bulan=None, tahun=None):
        """Get PIDSUS report data aggregated by jenis perkara and tahapan"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            
            # Base query - convert SQLite strftime to MySQL DATE_FORMAT
            query = '''
                SELECT
                    jenis_perkara,
                    penyidikan,
                    penuntutan,
                    COUNT(*) as jumlah,
                    DATE_FORMAT(tanggal, '%m') as bulan,
                    DATE_FORMAT(tanggal, '%Y') as tahun
                FROM pidsus_data
            '''
            
            params = []
            conditions = []
            
            if bulan:
                conditions.append("DATE_FORMAT(tanggal, '%m') = %s")
                params.append(str(bulan).zfill(2))
            
            if tahun:
                conditions.append("DATE_FORMAT(tanggal, '%Y') = %s")
                params.append(str(tahun))
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += '''
                GROUP BY jenis_perkara, penyidikan, penuntutan, DATE_FORMAT(tanggal, '%m'), DATE_FORMAT(tanggal, '%Y')
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
    
    def get_pidsus_report_data_bulanan(self, tahun=None, bulan=None):
        """Get PIDSUS report data for monthly report with chart data"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            
            # Build query with year and optional month filter
            where_conditions = ["DATE_FORMAT(tanggal, '%Y') = %s"]
            params = [str(tahun)]
            
            if bulan:
                where_conditions.append("DATE_FORMAT(tanggal, '%m') = %s")
                params.append(str(bulan).zfill(2))
            
            where_clause = "WHERE " + " AND ".join(where_conditions)
            
            # Get data from pidsus_data table
            query = f"""
            SELECT periode, jenis_perkara, tanggal, penyidikan, penuntutan,
                   DATE_FORMAT(tanggal, '%m') as bulan_num,
                   CASE DATE_FORMAT(tanggal, '%m')
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
            SELECT DISTINCT DATE_FORMAT(tanggal, '%m') as bulan_num,
                   CASE DATE_FORMAT(tanggal, '%m')
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
            WHERE DATE_FORMAT(tanggal, '%Y') = %s
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
    
    def create_user(self, username, password):
        """Create a new user"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)',
                              (username, hashed_password))
                conn.commit()
                return True
            except Error as e:
                print(f"Error creating user: {e}")
                return False

    def execute_query(self, query, params=None):
        """Execute a custom query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return rows

# Create a singleton instance
db = MySQLDatabase()

# Export all functions for compatibility with existing code
def init_database():
    """Initialize database with required tables"""
    return db.init_database()

def insert_pidum_data(data):
    """Insert PIDUM data into database"""
    return db.insert_pidum_data(data)

def insert_pidsus_data(data):
    """Insert PIDSUS data into database"""
    return db.insert_pidsus_data(data)

def get_all_pidum_data():
    """Get all PIDUM data from database"""
    return db.get_all_pidum_data()

def get_all_pidsus_data():
    """Get all PIDSUS data from database"""
    return db.get_all_pidsus_data()

def get_pidum_data_for_export():
    """Get PIDUM data formatted for export (without id and timestamp)"""
    return db.get_pidum_data_for_export()

def get_pidsus_data_for_export():
    """Get PIDSUS data formatted for export (without id and timestamp)"""
    return db.get_pidsus_data_for_export()

def delete_all_pidum_data():
    """Delete all PIDUM data (for testing)"""
    return db.delete_all_pidum_data()

def delete_pidum_item(item_id):
    """Delete single PIDUM item by ID"""
    return db.delete_pidum_item(item_id)

def update_pidum_data(item_id, data):
    """Update PIDUM data by ID"""
    return db.update_pidum_data(item_id, data)

def get_pidum_data_by_id(item_id):
    """Get single PIDUM data by ID"""
    return db.get_pidum_data_by_id(item_id)

def get_pidsus_data_by_id(item_id):
    """Get single PIDSUS data by ID"""
    return db.get_pidsus_data_by_id(item_id)

def update_pidsus_data(item_id, data):
    """Update PIDSUS data by ID"""
    return db.update_pidsus_data(item_id, data)

def delete_pidsus_item(item_id):
    """Delete single PIDSUS item by ID"""
    return db.delete_pidsus_item(item_id)

def delete_all_pidsus_data():
    """Delete all PIDSUS data (for testing)"""
    return db.delete_all_pidsus_data()

def get_database_stats():
    """Get database statistics"""
    return db.get_database_stats()

def get_pidum_data_by_tahapan(tahapan_penanganan):
    """Get PIDUM data filtered by tahapan penanganan"""
    return db.get_pidum_data_by_tahapan(tahapan_penanganan)

def get_pidum_report_data(bulan=None, tahun=None):
    """Get PIDUM report data aggregated by jenis perkara and tahapan"""
    return db.get_pidum_report_data(bulan, tahun)

def authenticate_user(username, password):
    """Authenticate user credentials"""
    return db.authenticate_user(username, password)

def get_pidsus_report_data(bulan=None, tahun=None):
    """Get PIDSUS report data aggregated by jenis perkara and tahapan"""
    return db.get_pidsus_report_data(bulan, tahun)

def get_pidsus_report_data_bulanan(tahun=None, bulan=None):
    """Get PIDSUS report data for monthly report with chart data"""
    return db.get_pidsus_report_data_bulanan(tahun, bulan)

def create_user(username, password):
    """Create a new user"""
    return db.create_user(username, password)

def insert_upaya_hukum_data(data):
    """Insert Upaya Hukum data into database"""
    return db.insert_upaya_hukum_data(data)

def get_all_upaya_hukum_data():
    """Get all Upaya Hukum data from database"""
    return db.get_all_upaya_hukum_data()

def delete_upaya_hukum_item(item_id):
    """Delete single Upaya Hukum item by ID"""
    return db.delete_upaya_hukum_item(item_id)