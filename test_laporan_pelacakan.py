"""
Test script untuk Laporan Pelacakan Perkara
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set working directory to app root untuk .env file
os.chdir(os.path.dirname(__file__))

from models.mysql_database import MySQLDatabase
from datetime import datetime

print("=" * 80)
print("TEST: Laporan Pelacakan Perkara")
print("=" * 80)

# Initialize database
db = MySQLDatabase()

# Test 1: Get all data for current year
print("\n[TEST 1] Get all data for current year (2025)")
print("-" * 80)
try:
    report_data = db.get_pelacakan_perkara_report_data(tahun=2025)
    print(f"Total rows: {len(report_data)}")

    if report_data:
        print("\nFirst 5 rows:")
        for i, row in enumerate(report_data[:5], 1):
            print(f"\n{i}. {row['nama_tersangka']}")
            print(f"   Pasal: {row['pasal']}")
            print(f"   Jenis: {row['jenis_perkara']}")
            print(f"   Pra Penuntutan: {row['pra_penuntutan']}")
            print(f"   Penuntutan: {row['penuntutan']}")
            print(f"   Upaya Hukum: {row['upaya_hukum']}")

    print("\n✓ TEST 1 PASSED")
except Exception as e:
    print(f"\n✗ TEST 1 FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Filter by jenis perkara
print("\n[TEST 2] Filter by jenis perkara = NARKOBA")
print("-" * 80)
try:
    report_data = db.get_pelacakan_perkara_report_data(tahun=2025, jenis_perkara='NARKOBA')
    print(f"Total rows with NARKOBA: {len(report_data)}")

    if report_data:
        print("\nSample data:")
        for i, row in enumerate(report_data[:3], 1):
            print(f"{i}. {row['nama_tersangka']} - {row['pasal']}")

    print("\n✓ TEST 2 PASSED")
except Exception as e:
    print(f"\n✗ TEST 2 FAILED: {e}")

# Test 3: Filter by tersangka name
print("\n[TEST 3] Search by tersangka name")
print("-" * 80)
try:
    # Get any name from first result
    all_data = db.get_pelacakan_perkara_report_data(tahun=2025)
    if all_data and len(all_data) > 0:
        sample_name = all_data[0]['nama_tersangka'].split()[0] if all_data[0]['nama_tersangka'] != '-' else ''

        if sample_name:
            report_data = db.get_pelacakan_perkara_report_data(tahun=2025, tersangka=sample_name)
            print(f"Search for '{sample_name}': {len(report_data)} results")

            if report_data:
                for row in report_data[:2]:
                    print(f"  - {row['nama_tersangka']}")

    print("\n✓ TEST 3 PASSED")
except Exception as e:
    print(f"\n✗ TEST 3 FAILED: {e}")

# Test 4: Statistics
print("\n[TEST 4] Calculate statistics")
print("-" * 80)
try:
    report_data = db.get_pelacakan_perkara_report_data(tahun=2025)

    total_keseluruhan = len(report_data)
    total_pra_penuntutan = sum(1 for item in report_data if item['pra_penuntutan'] != '-')
    total_penuntutan = sum(1 for item in report_data if item['penuntutan'] != '-')
    total_upaya_hukum = sum(1 for item in report_data if item['upaya_hukum'] != '-')
    total_ada_pasal = sum(1 for item in report_data if item['pasal'] != '-')

    print(f"Total Perkara: {total_keseluruhan}")
    print(f"Dengan Pra Penuntutan: {total_pra_penuntutan}")
    print(f"Dengan Penuntutan: {total_penuntutan}")
    print(f"Dengan Upaya Hukum: {total_upaya_hukum}")
    print(f"Dengan Pasal: {total_ada_pasal}")

    print("\n✓ TEST 4 PASSED")
except Exception as e:
    print(f"\n✗ TEST 4 FAILED: {e}")

print("\n" + "=" * 80)
print("TEST COMPLETED")
print("=" * 80)
