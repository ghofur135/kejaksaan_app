#!/usr/bin/env python3
"""
Test script for import functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from helpers.import_pra_penuntutan_helper import process_pra_penuntutan_import_file
import pandas as pd

def test_import():
    """Test import functionality with the new CSV format"""
    print("Testing import functionality...")
    
    # Read the CSV file
    csv_path = "data/csv/REGISTER_PENERIMAAN_SPDP_JANUARI_S_D_JUNI_extracted_20251031_092415.csv"
    
    try:
        # Read CSV first to check structure
        df = pd.read_csv(csv_path)
        print(f"CSV loaded successfully!")
        print(f"Columns: {list(df.columns)}")
        print(f"Total rows: {len(df)}")
        print("\nFirst few rows:")
        print(df.head())
        
        # Test import processing
        print("\n\nTesting import processing...")
        
        # Create a mock file object
        class MockFile:
            def __init__(self, filename):
                self.filename = filename
                self.content = None
                
            def read(self, size=None):
                if self.content is None:
                    with open(self.filename, 'rb') as f:
                        self.content = f.read()
                if size is not None:
                    return self.content[:size]
                return self.content
                
        mock_file = MockFile(csv_path)
        mock_file.filename = csv_path
        
        # Process the file
        result = process_pra_penuntutan_import_file(mock_file)
        
        if result['success']:
            print(f"✅ Import processing successful!")
            print(f"Total processed rows: {result['total_rows']}")
            
            # Show some sample data
            print("\nSample processed data:")
            for i, row in enumerate(result['data'][:5]):
                print(f"Row {i+1}:")
                print(f"  NO: {row.get('NO')}")
                print(f"  TANGGAL: {row.get('TANGGAL')}")
                print(f"  SUGGESTED_JENIS_PERKARA: {row.get('SUGGESTED_JENIS_PERKARA')}")
                print(f"  PASAL_ORIGINAL: {row.get('PASAL_ORIGINAL', '')[:100]}...")
                print()
                
            # Show category distribution
            categories = {}
            for row in result['data']:
                cat = row.get('SUGGESTED_JENIS_PERKARA', 'PERKARA LAINNYA')
                categories[cat] = categories.get(cat, 0) + 1
            
            print("Category distribution:")
            for cat, count in categories.items():
                print(f"  {cat}: {count}")
                
        else:
            print(f"X Import processing failed: {result['error']}")
            
    except Exception as e:
        print(f"X Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_import()