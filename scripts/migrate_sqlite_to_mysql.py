#!/usr/bin/env python3
"""
Script untuk migrasi data dari SQLite ke MySQL
"""

import sys
import os
import sqlite3
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Tambahkan path src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import Config
from models.database import get_all_pidum_data, get_all_pidsus_data

class SQLiteToMySQLMigrator:
    """Class untuk handle migrasi dari SQLite ke MySQL"""
    
    def __init__(self):
        self.sqlite_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'kejaksaan.db')
        self.mysql_config = Config.get_mysql_connection_params()
        
    def connect_sqlite(self):
        """Connect to SQLite database"""
        try:
            conn = sqlite3.connect(self.sqlite_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"Error connecting to SQLite: {e}")
            return None
    
    def connect_mysql(self):
        """Connect to MySQL database"""
        try:
            conn = mysql.connector.connect(**self.mysql_config)
            return conn
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def migrate_users(self, sqlite_conn, mysql_conn):
        """Migrate users table"""
        print("Migrating users table...")
        
        sqlite_cursor = sqlite_conn.cursor()
        mysql_cursor = mysql_conn.cursor()
        
        try:
            # Get data from SQLite
            sqlite_cursor.execute("SELECT * FROM users")
            users = sqlite_cursor.fetchall()
            
            # Insert into MySQL
            for user in users:
                query = """
                    INSERT INTO users (id, username, password, created_at) 
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE username = VALUES(username)
                """
                mysql_cursor.execute(query, (
                    user['id'],
                    user['username'],
                    user['password'],
                    user['created_at'] or datetime.now()
                ))
            
            mysql_conn.commit()
            print(f"Migrated {len(users)} users")
            return True
            
        except Exception as e:
            print(f"Error migrating users: {e}")
            mysql_conn.rollback()
            return False
    
    def migrate_pidum_data(self, sqlite_conn, mysql_conn):
        """Migrate pidum_data table"""
        print("Migrating PIDUM data...")
        
        sqlite_cursor = sqlite_conn.cursor()
        mysql_cursor = mysql_conn.cursor()
        
        try:
            # Get data from SQLite
            sqlite_cursor.execute("SELECT * FROM pidum_data")
            pidum_data = sqlite_cursor.fetchall()
            
            # Insert into MySQL
            for row in pidum_data:
                query = """
                    INSERT INTO pidum_data
                    (id, no, periode, tanggal, jenis_perkara, tahapan_penanganan, keterangan, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                mysql_cursor.execute(query, (
                    row['id'],
                    row['no'],
                    row['periode'],
                    row['tanggal'],
                    row['jenis_perkara'],
                    row['tahapan_penanganan'],
                    row['keterangan'],
                    row['created_at'] or datetime.now()
                ))
            
            mysql_conn.commit()
            print(f"Migrated {len(pidum_data)} PIDUM records")
            return True
            
        except Exception as e:
            print(f"Error migrating PIDUM data: {e}")
            mysql_conn.rollback()
            return False
    
    def migrate_pidsus_data(self, sqlite_conn, mysql_conn):
        """Migrate pidsus_data table"""
        print("Migrating PIDSUS data...")
        
        sqlite_cursor = sqlite_conn.cursor()
        mysql_cursor = mysql_conn.cursor()
        
        try:
            # Get data from SQLite
            sqlite_cursor.execute("SELECT * FROM pidsus_data")
            pidsus_data = sqlite_cursor.fetchall()
            
            # Insert into MySQL
            for row in pidsus_data:
                query = """
                    INSERT INTO pidsus_data
                    (id, no, periode, tanggal, jenis_perkara, penyidikan, penuntutan, keterangan, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                mysql_cursor.execute(query, (
                    row['id'],
                    row['no'],
                    row['periode'],
                    row['tanggal'],
                    row['jenis_perkara'],
                    row['penyidikan'],
                    row['penuntutan'],
                    row['keterangan'],
                    row['created_at'] or datetime.now()
                ))
            
            mysql_conn.commit()
            print(f"Migrated {len(pidsus_data)} PIDSUS records")
            return True
            
        except Exception as e:
            print(f"Error migrating PIDSUS data: {e}")
            mysql_conn.rollback()
            return False
    
    def verify_migration(self, sqlite_conn, mysql_conn):
        """Verify migration results"""
        print("Verifying migration...")
        
        sqlite_cursor = sqlite_conn.cursor()
        mysql_cursor = mysql_conn.cursor()
        
        # Verify PIDUM data
        sqlite_cursor.execute("SELECT COUNT(*) FROM pidum_data")
        sqlite_pidum_count = sqlite_cursor.fetchone()[0]
        
        mysql_cursor.execute("SELECT COUNT(*) FROM pidum_data")
        mysql_pidum_count = mysql_cursor.fetchone()[0]
        
        # Verify PIDSUS data
        sqlite_cursor.execute("SELECT COUNT(*) FROM pidsus_data")
        sqlite_pidsus_count = sqlite_cursor.fetchone()[0]
        
        mysql_cursor.execute("SELECT COUNT(*) FROM pidsus_data")
        mysql_pidsus_count = mysql_cursor.fetchone()[0]
        
        # Verify users
        sqlite_cursor.execute("SELECT COUNT(*) FROM users")
        sqlite_users_count = sqlite_cursor.fetchone()[0]
        
        mysql_cursor.execute("SELECT COUNT(*) FROM users")
        mysql_users_count = mysql_cursor.fetchone()[0]
        
        print("\nMigration Summary:")
        pidum_status = "OK" if sqlite_pidum_count == mysql_pidum_count else "ERROR"
        pidsus_status = "OK" if sqlite_pidsus_count == mysql_pidsus_count else "ERROR"
        users_status = "OK" if sqlite_users_count == mysql_users_count else "ERROR"
        print(f"PIDUM: {sqlite_pidum_count} to {mysql_pidum_count} [{pidum_status}]")
        print(f"PIDSUS: {sqlite_pidsus_count} to {mysql_pidsus_count} [{pidsus_status}]")
        print(f"Users: {sqlite_users_count} to {mysql_users_count} [{users_status}]")
        
        return (sqlite_pidum_count == mysql_pidum_count and 
                sqlite_pidsus_count == mysql_pidsus_count and 
                sqlite_users_count == mysql_users_count)
    
    def run_migration(self):
        """Run the complete migration process"""
        print("Starting SQLite to MySQL migration...")
        
        # Check if SQLite database exists
        if not os.path.exists(self.sqlite_path):
            print(f"SQLite database not found at: {self.sqlite_path}")
            return False
        
        # Connect to databases
        sqlite_conn = self.connect_sqlite()
        mysql_conn = self.connect_mysql()
        
        if not sqlite_conn or not mysql_conn:
            print("Failed to connect to databases")
            return False
        
        try:
            # Clear existing data first
            print("Clearing existing MySQL data...")
            mysql_cursor = mysql_conn.cursor()
            mysql_cursor.execute("DELETE FROM pidum_data")
            mysql_cursor.execute("DELETE FROM pidsus_data")
            mysql_cursor.execute("DELETE FROM users")
            mysql_cursor.execute("ALTER TABLE pidum_data AUTO_INCREMENT = 1")
            mysql_cursor.execute("ALTER TABLE pidsus_data AUTO_INCREMENT = 1")
            mysql_cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1")
            mysql_conn.commit()
            print("Existing data cleared.")
            
            # Run migration
            success = True
            success &= self.migrate_users(sqlite_conn, mysql_conn)
            success &= self.migrate_pidum_data(sqlite_conn, mysql_conn)
            success &= self.migrate_pidsus_data(sqlite_conn, mysql_conn)
            
            # Verify migration
            if success:
                success &= self.verify_migration(sqlite_conn, mysql_conn)
            
            if success:
                print("\nMigration completed successfully!")
            else:
                print("\nMigration completed with errors!")
            
            return success
            
        except Exception as e:
            print(f"Migration failed: {e}")
            return False
        finally:
            # Close connections
            if sqlite_conn:
                sqlite_conn.close()
            if mysql_conn:
                mysql_conn.close()

def main():
    """Main function"""
    print("=" * 60)
    print("SQLite to MySQL Migration Tool")
    print("=" * 60)
    
    migrator = SQLiteToMySQLMigrator()
    
    # Auto-continue for testing
    print("Auto-migrating data from SQLite to MySQL...")
    
    # Run migration
    success = migrator.run_migration()
    
    if success:
        print("\nMigration completed successfully!")
        print("You can now update your application to use MySQL database.")
    else:
        print("\nMigration failed!")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()