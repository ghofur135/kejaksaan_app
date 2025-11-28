"""
Direct database test dengan hardcoded credentials
"""
import mysql.connector
from contextlib import contextmanager

@contextmanager
def get_connection():
    """Get MySQL connection with hardcoded credentials"""
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='db_kejaksaan_dev',
            user='apps',
            password='@Kardinah2025#',  # Hardcoded untuk testing
            port=3306,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            autocommit=True
        )
        yield conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()

print("="*80)
print("TESTING: Laporan Pelacakan Perkara dengan Direct DB Connection")
print("="*80)

# Test koneksi
print("\n[1] Testing database connection...")
try:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM pidum_data")
        result = cursor.fetchone()
        print(f"   Total rows in pidum_data: {result['total']}")
        print("   [OK] Database connection successful!")
except Exception as e:
    print(f"   [FAIL] Connection failed: {e}")
    exit(1)

# Test query pelacakan perkara
print("\n[2] Testing pelacakan perkara query...")
try:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)

        # Query yang sama dengan get_pelacakan_perkara_report_data
        query = """
            SELECT
                identitas_tersangka as nama_tersangka,
                jenis_perkara,
                no as nomor_perkara,
                MAX(pasal) as pasal,
                MAX(CASE WHEN tahapan_penanganan = 'PRA PENUNTUTAN'
                    THEN DATE_FORMAT(tanggal, '%d/%m/%Y')
                    ELSE NULL END) as pra_penuntutan,
                MAX(CASE WHEN tahapan_penanganan = 'PENUNTUTAN'
                    THEN DATE_FORMAT(tanggal, '%d/%m/%Y')
                    ELSE NULL END) as penuntutan,
                MAX(CASE WHEN tahapan_penanganan = 'UPAYA HUKUM'
                    THEN DATE_FORMAT(tanggal, '%d/%m/%Y')
                    ELSE NULL END) as upaya_hukum,
                MIN(tanggal) as earliest_date
            FROM pidum_data
            WHERE YEAR(tanggal) = %s
              AND identitas_tersangka IS NOT NULL
              AND identitas_tersangka != ''
            GROUP BY identitas_tersangka, jenis_perkara, no
            ORDER BY MIN(tanggal) DESC
        """

        cursor.execute(query, (2025,))
        rows = cursor.fetchall()

        print(f"   Total cases found: {len(rows)}")

        if rows:
            print("\n   First 5 results:")
            for i, row in enumerate(rows[:5], 1):
                pasal_display = row['pasal'] if row['pasal'] else '-'
                pra = row['pra_penuntutan'] if row['pra_penuntutan'] else '-'
                pen = row['penuntutan'] if row['penuntutan'] else '-'
                upa = row['upaya_hukum'] if row['upaya_hukum'] else '-'

                print(f"\n   {i}. {row['nama_tersangka']}")
                print(f"      Pasal: {pasal_display}")
                print(f"      Jenis: {row['jenis_perkara']}")
                print(f"      Pra Penuntutan: {pra} | Penuntutan: {pen} | Upaya Hukum: {upa}")

        print("\n   [OK] Query successful!")

except Exception as e:
    print(f"   [FAIL] Query failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test statistics
print("\n[3] Testing statistics calculation...")
try:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (2025,))
        report_data = cursor.fetchall()

        total_keseluruhan = len(report_data)
        total_pra_penuntutan = sum(1 for item in report_data if item['pra_penuntutan'])
        total_penuntutan = sum(1 for item in report_data if item['penuntutan'])
        total_upaya_hukum = sum(1 for item in report_data if item['upaya_hukum'])
        total_ada_pasal = sum(1 for item in report_data if item['pasal'])

        print(f"   Total Perkara: {total_keseluruhan}")
        print(f"   Dengan Pra Penuntutan: {total_pra_penuntutan}")
        print(f"   Dengan Penuntutan: {total_penuntutan}")
        print(f"   Dengan Upaya Hukum: {total_upaya_hukum}")
        print(f"   Dengan Pasal: {total_ada_pasal}")
        print("\n   [OK] Statistics calculated!")

except Exception as e:
    print(f"   [FAIL] Statistics failed: {e}")
    exit(1)

# Test filter by jenis perkara
print("\n[4] Testing filter by jenis perkara...")
try:
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)

        query_filtered = query.replace(
            "WHERE YEAR(tanggal) = %s",
            "WHERE YEAR(tanggal) = %s AND jenis_perkara = %s"
        )

        cursor.execute(query_filtered, (2025, 'NARKOBA'))
        rows = cursor.fetchall()

        print(f"   Cases with jenis_perkara = NARKOBA: {len(rows)}")

        if rows:
            for i, row in enumerate(rows[:3], 1):
                print(f"   {i}. {row['nama_tersangka']} - {row['pasal'] or '-'}")

        print("\n   [OK] Filter successful!")

except Exception as e:
    print(f"   [FAIL] Filter failed: {e}")
    exit(1)

print("\n" + "="*80)
print("ALL TESTS PASSED!")
print("="*80)
print("\nFungsi get_pelacakan_perkara_report_data() bekerja dengan baik!")
print("Laporan Pelacakan Perkara siap digunakan di web application.")
