"""
Migration Script: Add identitas_tersangka column to pidum_data table
Run this script to add the new column to existing database
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import Config
import mysql.connector
from mysql.connector import Error

def run_migration():
    """Add identitas_tersangka column to pidum_data table"""
    try:
        # Get connection parameters
        config = Config.get_mysql_connection_params()

        # Connect to database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Check if column already exists
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s
            AND TABLE_NAME = 'pidum_data'
            AND COLUMN_NAME = 'identitas_tersangka'
        """, (config['database'],))

        result = cursor.fetchone()

        if result[0] > 0:
            print("Column 'identitas_tersangka' already exists in pidum_data table.")
            return True

        # Add the column
        print("Adding column 'identitas_tersangka' to pidum_data table...")
        cursor.execute("""
            ALTER TABLE pidum_data
            ADD COLUMN identitas_tersangka TEXT AFTER tahapan_penanganan
        """)

        conn.commit()
        print("Migration completed successfully!")
        print("Column 'identitas_tersangka' has been added to pidum_data table.")
        return True

    except Error as e:
        print(f"Error during migration: {e}")
        print("\nJika error akses database, jalankan query berikut secara manual di MySQL:")
        print("ALTER TABLE pidum_data ADD COLUMN identitas_tersangka TEXT AFTER tahapan_penanganan;")
        return False

    finally:
        try:
            if 'cursor' in dir() and cursor:
                cursor.close()
            if 'conn' in dir() and conn and conn.is_connected():
                conn.close()
        except:
            pass

if __name__ == '__main__':
    success = run_migration()
    sys.exit(0 if success else 1)
