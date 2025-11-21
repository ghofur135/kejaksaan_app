#!/usr/bin/env python3
"""
Script untuk setup database MySQL dan testing koneksi
"""

import sys
import os
import mysql.connector
from mysql.connector import Error

# Tambahkan path src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import Config

class MySQLSetup:
    """Class untuk handle setup database MySQL"""
    
    def __init__(self):
        self.config = Config.get_mysql_connection_params()
        
    def test_connection(self):
        """Test koneksi ke MySQL server"""
        print("🔍 Testing MySQL connection...")
        
        try:
            # Connect tanpa database dulu
            test_config = self.config.copy()
            test_config.pop('database', None)
            
            conn = mysql.connector.connect(**test_config)
            print("✅ MySQL server connection successful!")
            conn.close()
            return True
            
        except Error as e:
            print(f"❌ MySQL connection failed: {e}")
            return False
    
    def create_database(self):
        """Create database jika belum ada"""
        print("🔄 Creating database...")
        
        try:
            # Connect tanpa database dulu
            config = self.config.copy()
            database_name = config.pop('database', None)
            
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Database '{database_name}' created or already exists")
            
            conn.close()
            return True
            
        except Error as e:
            print(f"❌ Failed to create database: {e}")
            return False
    
    def setup_database_schema(self):
        """Setup schema database dari file SQL"""
        print("🔄 Setting up database schema...")
        
        schema_file = os.path.join(os.path.dirname(__file__), 'mysql_schema.sql')
        
        if not os.path.exists(schema_file):
            print(f"❌ Schema file not found: {schema_file}")
            return False
        
        try:
            # Connect ke database
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            # Read and execute schema file
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement:
                    cursor.execute(statement)
            
            conn.commit()
            print("✅ Database schema setup completed!")
            conn.close()
            return True
            
        except Error as e:
            print(f"❌ Failed to setup database schema: {e}")
            return False
    
    def test_database_operations(self):
        """Test operasi database dasar"""
        print("🔄 Testing database operations...")
        
        try:
            from models.mysql_database import db
            
            # Test database stats
            stats = db.get_database_stats()
            print(f"✅ Database stats: {stats}")
            
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
            print(f"✅ Inserted PIDUM test data with ID: {pidum_id}")
            
            # Test retrieve operation
            retrieved_data = db.get_pidum_data_by_id(pidum_id)
            if retrieved_data:
                print(f"✅ Retrieved PIDUM test data: {retrieved_data['no']}")
            else:
                print("❌ Failed to retrieve PIDUM test data")
                return False
            
            # Test delete operation
            delete_success = db.delete_pidum_item(pidum_id)
            if delete_success:
                print("✅ Deleted PIDUM test data")
            else:
                print("❌ Failed to delete PIDUM test data")
                return False
            
            # Test authentication
            auth_result = db.authenticate_user('admin', 'P@ssw0rd25#!')
            if auth_result:
                print(f"✅ Authentication successful for user: {auth_result['username']}")
            else:
                print("❌ Authentication failed for admin user")
                return False
            
            print("✅ All database operations test passed!")
            return True
            
        except Exception as e:
            print(f"❌ Database operations test failed: {e}")
            return False
    
    def run_setup(self):
        """Run complete setup process"""
        print("Starting MySQL database setup...")
        print("=" * 60)
        
        # Test connection
        if not self.test_connection():
            return False
        
        # Create database
        if not self.create_database():
            return False
        
        # Setup schema
        if not self.setup_database_schema():
            return False
        
        # Test operations
        if not self.test_database_operations():
            return False
        
        print("\nMySQL database setup completed successfully!")
        print("Database is ready for use with the application.")
        return True

def main():
    """Main function"""
    print("=" * 60)
    print("MySQL Database Setup Tool")
    print("=" * 60)
    
    # Display configuration
    config = Config.get_mysql_connection_params()
    print(f"Host: {config['host']}")
    print(f"Database: {config['database']}")
    print(f"User: {config['user']}")
    print(f"Port: {config['port']}")
    print("=" * 60)
    
    # Confirm setup - auto-continue for testing
    print("Auto-setting up MySQL database...")
    
    # Run setup
    setup = MySQLSetup()
    success = setup.run_setup()
    
    if success:
        print("\n✅ Setup completed successfully!")
        print("You can now run the migration script to transfer data from SQLite.")
    else:
        print("\n❌ Setup failed!")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()