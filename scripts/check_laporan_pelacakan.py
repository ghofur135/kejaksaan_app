"""
Script untuk mengecek kelengkapan fitur Laporan Pelacakan Perkara
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

def print_header(text):
    print(f"\n{'='*80}")
    print(f"{text.center(80)}")
    print(f"{'='*80}\n")

def print_success(text):
    print(f"✓ {text}")

def print_error(text):
    print(f"✗ {text}")

def print_info(text):
    print(f"ℹ {text}")

def main():
    print_header("CHECKING LAPORAN PELACAKAN PERKARA FEATURE")
    
    all_ok = True
    
    # 1. Check template file
    print("1. Checking template file...")
    template_path = os.path.join('templates', 'laporan_pelacakan_perkara.html')
    if os.path.exists(template_path):
        print_success(f"Template exists: {template_path}")
    else:
        print_error(f"Template NOT found: {template_path}")
        all_ok = False
    
    # 2. Check route in app_with_db.py
    print("\n2. Checking route in app_with_db.py...")
    app_path = os.path.join('src', 'app_with_db.py')
    if os.path.exists(app_path):
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '/laporan_pelacakan_perkara' in content:
                print_success("Route '/laporan_pelacakan_perkara' found in app_with_db.py")
            else:
                print_error("Route '/laporan_pelacakan_perkara' NOT found in app_with_db.py")
                all_ok = False
    else:
        print_error(f"File NOT found: {app_path}")
        all_ok = False
    
    # 3. Check database function
    print("\n3. Checking database function...")
    db_path = os.path.join('src', 'models', 'mysql_database.py')
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'get_pelacakan_perkara_report_data' in content:
                print_success("Function 'get_pelacakan_perkara_report_data' found in mysql_database.py")
            else:
                print_error("Function 'get_pelacakan_perkara_report_data' NOT found in mysql_database.py")
                all_ok = False
    else:
        print_error(f"File NOT found: {db_path}")
        all_ok = False
    
    # 4. Check database schema (identitas_tersangka column)
    print("\n4. Checking database schema...")
    try:
        from models.mysql_database import MySQLDatabase
        db = MySQLDatabase()
        
        with db.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            
            # Check identitas_tersangka column
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'pidum_data'
                AND COLUMN_NAME = 'identitas_tersangka'
            """)
            result = cursor.fetchone()
            
            if result['count'] > 0:
                print_success("Column 'identitas_tersangka' exists in pidum_data table")
            else:
                print_error("Column 'identitas_tersangka' NOT found in pidum_data table")
                print_info("Run: python scripts/auto_migrate.py")
                all_ok = False
            
            # Check pasal column
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'pidum_data'
                AND COLUMN_NAME = 'pasal'
            """)
            result = cursor.fetchone()
            
            if result['count'] > 0:
                print_success("Column 'pasal' exists in pidum_data table")
            else:
                print_error("Column 'pasal' NOT found in pidum_data table")
                print_info("Run: python scripts/auto_migrate.py")
                all_ok = False
                
    except Exception as e:
        print_error(f"Database check failed: {e}")
        print_info("Make sure database is running and .env is configured correctly")
        all_ok = False
    
    # 5. Test the function
    print("\n5. Testing database function...")
    try:
        from models.mysql_database import get_pelacakan_perkara_report_data
        from datetime import datetime
        
        # Test with current year
        current_year = datetime.now().year
        report_data = get_pelacakan_perkara_report_data(tahun=current_year)
        
        print_success(f"Function executed successfully")
        print_info(f"Found {len(report_data)} records for year {current_year}")
        
        if len(report_data) > 0:
            print_info(f"Sample data: {report_data[0]['nama_tersangka']} - {report_data[0]['jenis_perkara']}")
        else:
            print_info("No data found (this is OK if database is empty)")
            
    except Exception as e:
        print_error(f"Function test failed: {e}")
        import traceback
        traceback.print_exc()
        all_ok = False
    
    # Summary
    print_header("SUMMARY")
    if all_ok:
        print_success("All checks passed! ✓")
        print_info("\nYou can access the feature at:")
        print_info("  http://localhost:5001/laporan_pelacakan_perkara")
        print_info("\nMake sure the application is running:")
        print_info("  python src/app_with_db.py")
    else:
        print_error("Some checks failed!")
        print_info("\nPlease fix the issues above and try again.")
        print_info("\nCommon fixes:")
        print_info("  1. Run migration: python scripts/auto_migrate.py")
        print_info("  2. Check .env configuration")
        print_info("  3. Make sure MySQL is running")
        print_info("  4. Pull latest code: git pull")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
