"""
Script untuk mengecek sinkronisasi schema database MySQL dengan model di source code
Akan menampilkan:
1. Kolom yang ada di database
2. Kolom yang seharusnya ada (dari model)
3. Kolom yang hilang (perlu ditambahkan)
4. Kolom yang berlebih (tidak ada di model)
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.mysql_database import MySQLDatabase
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

def print_header(text):
    """Print colored header"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}{text.center(80)}")
    print(f"{Fore.CYAN}{'='*80}\n")

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}✓ {text}")

def print_warning(text):
    """Print warning message"""
    print(f"{Fore.YELLOW}⚠ {text}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}✗ {text}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.BLUE}ℹ {text}")

def get_table_columns(cursor, table_name):
    """Get all columns from a table"""
    cursor.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION
    """)
    return cursor.fetchall()

def check_table_exists(cursor, table_name):
    """Check if table exists"""
    cursor.execute(f"""
        SELECT COUNT(*) as count
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = '{table_name}'
    """)
    result = cursor.fetchone()
    return result['count'] > 0

def main():
    print_header("DATABASE SCHEMA SYNCHRONIZATION CHECKER")
    
    # Expected schema based on model
    expected_schema = {
        'pidum_data': [
            'id', 'no', 'periode', 'tanggal', 'jenis_perkara', 
            'tahapan_penanganan', 'pasal', 'identitas_tersangka', 
            'keterangan', 'created_at'
        ],
        'pidsus_data': [
            'id', 'no', 'periode', 'tanggal', 'jenis_perkara', 
            'pasal', 'nama_tersangka', 'penyidikan', 'penuntutan', 
            'keterangan', 'created_at'
        ],
        'upaya_hukum_data': [
            'id', 'no', 'terdakwa_terpidana', 'no_tanggal_rp9', 'jenis_perkara',
            # Perlawanan
            'perlawanan_no_tgl_penetapan_pn', 'perlawanan_no_tgl_akte', 
            'perlawanan_tgl_pengajuan_memori', 'perlawanan_yang_mengajukan_jpu',
            'perlawanan_yang_mengajukan_terdakwa', 'perlawanan_no_tgl_amar_penetapan_pt',
            # Banding
            'banding_no_tgl_akte_permohonan', 'banding_tgl_pengajuan_memori',
            'banding_yang_mengajukan_jpu', 'banding_yang_mengajukan_terdakwa',
            'banding_no_tgl_amar_putusan_pt',
            # Kasasi
            'kasasi_no_tgl_akte_permohonan', 'kasasi_tgl_pengajuan_memori',
            'kasasi_yang_mengajukan_jpu', 'kasasi_yang_mengajukan_terdakwa',
            'kasasi_no_tgl_amar_putusan_ma',
            # Kasasi Demi Hukum
            'kasasi_demi_hukum_tgl_diajukan', 'kasasi_demi_hukum_keadaan_putusan_pn',
            'kasasi_demi_hukum_no_tgl_amar_putusan_ma',
            # PK
            'pk_tgl_diajukan_terpidana', 'pk_tgl_pemeriksaan_berita_acara',
            'pk_no_tgl_amar_putusan',
            # Grasi
            'grasi_tgl_penerimaan_berkas', 'grasi_tgl_penundaan_eksekusi',
            'grasi_tgl_risalah_pertimbangan_kajari', 'grasi_tgl_terima_kepres',
            'grasi_no_tgl_kepres_amar',
            # Metadata
            'created_at'
        ],
        'users': [
            'id', 'username', 'password', 'created_at'
        ]
    }
    
    try:
        db = MySQLDatabase()
        
        with db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            
            # Get database name
            cursor.execute("SELECT DATABASE() as db_name")
            db_name = cursor.fetchone()['db_name']
            print_info(f"Connected to database: {Fore.WHITE}{db_name}")
            
            all_synced = True
            
            # Check each table
            for table_name, expected_columns in expected_schema.items():
                print_header(f"Checking Table: {table_name}")
                
                # Check if table exists
                if not check_table_exists(cursor, table_name):
                    print_error(f"Table '{table_name}' does not exist!")
                    print_warning(f"Run migration to create this table")
                    all_synced = False
                    continue
                
                # Get actual columns
                actual_columns_data = get_table_columns(cursor, table_name)
                actual_columns = [col['COLUMN_NAME'] for col in actual_columns_data]
                
                # Compare
                expected_set = set(expected_columns)
                actual_set = set(actual_columns)
                
                missing_columns = expected_set - actual_set
                extra_columns = actual_set - expected_set
                
                # Display results
                print(f"\n{Fore.WHITE}Expected columns: {len(expected_columns)}")
                print(f"{Fore.WHITE}Actual columns:   {len(actual_columns)}")
                
                if not missing_columns and not extra_columns:
                    print_success(f"Table '{table_name}' is fully synchronized! ✓")
                else:
                    all_synced = False
                    
                    if missing_columns:
                        print_error(f"\nMissing columns ({len(missing_columns)}):")
                        for col in sorted(missing_columns):
                            print(f"  {Fore.RED}- {col}")
                        
                        # Generate ALTER TABLE statements
                        print(f"\n{Fore.YELLOW}Migration SQL needed:")
                        for col in sorted(missing_columns):
                            if col == 'pasal':
                                print(f"  ALTER TABLE {table_name} ADD COLUMN {col} TEXT;")
                            elif col == 'identitas_tersangka':
                                print(f"  ALTER TABLE {table_name} ADD COLUMN {col} TEXT AFTER pasal;")
                            elif col == 'nama_tersangka':
                                print(f"  ALTER TABLE {table_name} ADD COLUMN {col} TEXT AFTER pasal;")
                            else:
                                print(f"  ALTER TABLE {table_name} ADD COLUMN {col} TEXT;")
                    
                    if extra_columns:
                        print_warning(f"\nExtra columns (not in model) ({len(extra_columns)}):")
                        for col in sorted(extra_columns):
                            print(f"  {Fore.YELLOW}+ {col}")
                
                # Show column details
                print(f"\n{Fore.CYAN}Column Details:")
                print(f"{Fore.WHITE}{'Column Name':<35} {'Type':<15} {'Nullable':<10} {'Key':<10}")
                print(f"{Fore.WHITE}{'-'*70}")
                for col_data in actual_columns_data:
                    col_name = col_data['COLUMN_NAME']
                    col_type = col_data['DATA_TYPE']
                    nullable = col_data['IS_NULLABLE']
                    key = col_data['COLUMN_KEY'] or '-'
                    
                    # Color code based on status
                    if col_name in missing_columns:
                        color = Fore.RED
                    elif col_name in extra_columns:
                        color = Fore.YELLOW
                    else:
                        color = Fore.GREEN
                    
                    print(f"{color}{col_name:<35} {col_type:<15} {nullable:<10} {key:<10}")
            
            # Final summary
            print_header("SUMMARY")
            if all_synced:
                print_success("All tables are synchronized with the model! 🎉")
                print_info("Your database schema matches the source code perfectly.")
            else:
                print_warning("Some tables need migration!")
                print_info("Run the following command to auto-migrate:")
                print(f"  {Fore.WHITE}python src/app_with_db.py")
                print_info("\nOr run migrations manually using the SQL statements above.")
            
    except Exception as e:
        print_error(f"Error connecting to database: {e}")
        print_info("\nMake sure:")
        print("  1. MySQL server is running")
        print("  2. .env file is configured correctly")
        print("  3. Database credentials are correct")
        return 1
    
    return 0 if all_synced else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
