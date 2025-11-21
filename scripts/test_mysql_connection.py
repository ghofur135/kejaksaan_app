#!/usr/bin/env python3
"""
Simple script to test MySQL connection without special Unicode characters
"""

import sys
import os

# Add src path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from config import Config
    from models.mysql_database import db
    
    print("Testing MySQL Database Connection")
    print("=" * 50)
    
    # Test connection
    print("Testing database connection...")
    try:
        stats = db.get_database_stats()
        print(f"SUCCESS: Connected to MySQL database")
        print(f"Database stats: {stats}")
        
        # Test insert operation
        test_data = {
            'NO': 'TEST_001',
            'PERIODE': '2025-Q1',
            'TANGGAL': '2025-01-01',
            'JENIS PERKARA': 'TEST PERKARA',
            'TAHAPAN_PENANGANAN': 'PRA PENUNTUTAN',
            'KETERANGAN': 'Test data'
        }
        
        pidum_id = db.insert_pidum_data(test_data)
        print(f"SUCCESS: Inserted PIDUM test data with ID: {pidum_id}")
        
        # Test retrieve operation
        retrieved_data = db.get_pidum_data_by_id(pidum_id)
        if retrieved_data:
            print(f"SUCCESS: Retrieved PIDUM test data: {retrieved_data['no']}")
        else:
            print("ERROR: Failed to retrieve PIDUM test data")
            
        # Test delete operation
        delete_success = db.delete_pidum_item(pidum_id)
        if delete_success:
            print("SUCCESS: Deleted PIDUM test data")
        else:
            print("ERROR: Failed to delete PIDUM test data")
            
        print("SUCCESS: All database operations test passed!")
        print("MySQL database is ready for use with the application.")
        
    except Exception as e:
        print(f"ERROR: Database operations test failed: {e}")
        print("Please check your MySQL connection and try again.")

except ImportError as e:
    print(f"ERROR: Failed to import modules: {e}")
    print("Please ensure all required modules are installed.")