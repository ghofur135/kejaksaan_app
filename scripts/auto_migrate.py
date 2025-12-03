"""
Script untuk melakukan auto-migration database
Akan otomatis menambahkan kolom yang hilang berdasarkan model di source code
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.mysql_database import MySQLDatabase

def print_header(text):
    """Print header"""
    print(f"\n{'='*80}")
    print(f"{text.center(80)}")
    print(f"{'='*80}\n")

def main():
    print_header("AUTO MIGRATION - DATABASE SCHEMA")
    
    try:
        db = MySQLDatabase()
        
        print("Connecting to database...")
        with db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            
            # Get database name
            cursor.execute("SELECT DATABASE() as db_name")
            db_name = cursor.fetchone()['db_name']
            print(f"✓ Connected to: {db_name}\n")
            
            migrations_applied = []
            
            # Migration 1: Add pasal column to pidum_data
            print("Checking pidum_data.pasal...")
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'pidum_data'
                AND COLUMN_NAME = 'pasal'
            """)
            if cursor.fetchone()['count'] == 0:
                print("  → Adding column 'pasal' to pidum_data...")
                cursor.execute("""
                    ALTER TABLE pidum_data
                    ADD COLUMN pasal TEXT AFTER tahapan_penanganan
                """)
                conn.commit()
                print("  ✓ Column 'pasal' added successfully")
                migrations_applied.append("pidum_data.pasal")
            else:
                print("  ✓ Column 'pasal' already exists")
            
            # Migration 2: Add identitas_tersangka column to pidum_data
            print("\nChecking pidum_data.identitas_tersangka...")
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'pidum_data'
                AND COLUMN_NAME = 'identitas_tersangka'
            """)
            if cursor.fetchone()['count'] == 0:
                print("  → Adding column 'identitas_tersangka' to pidum_data...")
                cursor.execute("""
                    ALTER TABLE pidum_data
                    ADD COLUMN identitas_tersangka TEXT AFTER pasal
                """)
                conn.commit()
                print("  ✓ Column 'identitas_tersangka' added successfully")
                migrations_applied.append("pidum_data.identitas_tersangka")
            else:
                print("  ✓ Column 'identitas_tersangka' already exists")
            
            # Migration 3: Add pasal column to pidsus_data
            print("\nChecking pidsus_data.pasal...")
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'pidsus_data'
                AND COLUMN_NAME = 'pasal'
            """)
            if cursor.fetchone()['count'] == 0:
                print("  → Adding column 'pasal' to pidsus_data...")
                cursor.execute("""
                    ALTER TABLE pidsus_data
                    ADD COLUMN pasal TEXT AFTER jenis_perkara
                """)
                conn.commit()
                print("  ✓ Column 'pasal' added successfully")
                migrations_applied.append("pidsus_data.pasal")
            else:
                print("  ✓ Column 'pasal' already exists")
            
            # Migration 4: Add nama_tersangka column to pidsus_data
            print("\nChecking pidsus_data.nama_tersangka...")
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'pidsus_data'
                AND COLUMN_NAME = 'nama_tersangka'
            """)
            if cursor.fetchone()['count'] == 0:
                print("  → Adding column 'nama_tersangka' to pidsus_data...")
                cursor.execute("""
                    ALTER TABLE pidsus_data
                    ADD COLUMN nama_tersangka TEXT AFTER pasal
                """)
                conn.commit()
                print("  ✓ Column 'nama_tersangka' added successfully")
                migrations_applied.append("pidsus_data.nama_tersangka")
            else:
                print("  ✓ Column 'nama_tersangka' already exists")
            
            # Migration 5: Create upaya_hukum_data table
            print("\nChecking upaya_hukum_data table...")
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'upaya_hukum_data'
            """)
            if cursor.fetchone()['count'] == 0:
                print("  → Creating table 'upaya_hukum_data'...")
                cursor.execute("""
                    CREATE TABLE upaya_hukum_data (
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
                print("  ✓ Table 'upaya_hukum_data' created successfully")
                migrations_applied.append("upaya_hukum_data (table)")
            else:
                print("  ✓ Table 'upaya_hukum_data' already exists")
            
            # Summary
            print_header("MIGRATION SUMMARY")
            if migrations_applied:
                print(f"✓ {len(migrations_applied)} migration(s) applied successfully:\n")
                for i, migration in enumerate(migrations_applied, 1):
                    print(f"  {i}. {migration}")
                print("\n✓ Database schema is now up to date!")
            else:
                print("✓ No migrations needed - database is already up to date!")
            
            print("\nYou can now run the application:")
            print("  python src/app_with_db.py")
            
    except Exception as e:
        print(f"\n✗ Error during migration: {e}")
        print("\nPlease check:")
        print("  1. Database connection settings in .env")
        print("  2. MySQL server is running")
        print("  3. User has ALTER TABLE privileges")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
