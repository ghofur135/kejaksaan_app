#!/usr/bin/env python3
"""
Script to setup MySQL database schema only
"""

import sys
import os

# Add src path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from config import Config
    import mysql.connector
    from mysql.connector import Error
    
    print("Setting up MySQL Database Schema")
    print("=" * 50)
    
    # Display configuration
    config = Config.get_mysql_connection_params()
    print(f"Host: {config['host']}")
    print(f"Database: {config['database']}")
    print(f"User: {config['user']}")
    print(f"Port: {config['port']}")
    print("=" * 50)
    
    # Connect to MySQL server
    print("Connecting to MySQL server...")
    try:
        # Connect without database first
        test_config = config.copy()
        test_config.pop('database', None)
        
        conn = mysql.connector.connect(**test_config)
        print("SUCCESS: Connected to MySQL server!")
        
        # Create database if not exists
        database_name = config['database']
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"SUCCESS: Database '{database_name}' created or already exists")
        conn.close()
        
        # Connect to database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Read and execute schema file
        schema_file = os.path.join(os.path.dirname(__file__), 'mysql_schema.sql')
        
        if not os.path.exists(schema_file):
            print(f"ERROR: Schema file not found: {schema_file}")
            sys.exit(1)
        
        print("Setting up database schema...")
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:
                cursor.execute(statement)
        
        conn.commit()
        print("SUCCESS: Database schema setup completed!")
        conn.close()
        
        print("SUCCESS: MySQL database schema is ready for use!")
        
    except Error as e:
        print(f"ERROR: Failed to setup database schema: {e}")
        sys.exit(1)

except ImportError as e:
    print(f"ERROR: Failed to import modules: {e}")
    sys.exit(1)