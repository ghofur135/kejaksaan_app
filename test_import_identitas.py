"""Test script untuk verifikasi import identitas tersangka"""
import sys
import io
sys.path.insert(0, r'D:\my-project\kejaksaan_app\src')

from werkzeug.datastructures import FileStorage
from helpers.import_pra_penuntutan_helper import process_pra_penuntutan_import_file

# File path
filepath = r'D:\my-project\kejaksaan_app\data\csv\REGISTER PENERIMAAN SPDP JANUARI S.D JUNI_output.csv'

print("=" * 60)
print("TEST IMPORT IDENTITAS TERSANGKA")
print("=" * 60)

# Read and create FileStorage
with open(filepath, 'rb') as f:
    content = f.read()
    print(f"File size: {len(content)} bytes")

with open(filepath, 'rb') as f:
    file_storage = FileStorage(
        stream=io.BytesIO(f.read()),
        filename='REGISTER PENERIMAAN SPDP JANUARI S.D JUNI_output.csv',
        content_type='text/csv'
    )

print("\nProcessing file...")
result = process_pra_penuntutan_import_file(file_storage)

print("\n" + "=" * 60)
print("RESULT:")
print("=" * 60)
print(f"Success: {result['success']}")
print(f"Total rows: {result['total_rows']}")
print(f"Columns in CSV: {result.get('columns', [])}")

if result.get('error'):
    print(f"Error: {result['error']}")

if result['data'] and len(result['data']) > 0:
    print(f"\nFirst row keys: {list(result['data'][0].keys())}")
    print(f"\nFirst 5 IDENTITAS_TERSANGKA values:")
    for i, row in enumerate(result['data'][:5]):
        identitas = row.get('IDENTITAS_TERSANGKA', 'NOT_SET')
        print(f"  Row {i+1}: {repr(identitas)[:80]}...")
else:
    print("NO DATA!")

print("\n" + "=" * 60)
