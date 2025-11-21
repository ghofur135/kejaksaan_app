#!/usr/bin/env python3
"""
Script untuk membuat user admin untuk aplikasi
"""

import sys
import os

# Tambahkan path src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.mysql_database import create_user, get_all_pidsus_data

def main():
    """Main function"""
    print("=" * 50)
    print("Create Admin User Tool")
    print("=" * 50)
    
    # Buat user admin dengan password default
    username = "kejaksaan"
    password = "kejaksaan123"
    
    print(f"Creating user: {username}")
    print(f"Password: {password}")
    
    try:
        success = create_user(username, password)
        if success:
            print("User created successfully!")
            print("\nLogin credentials:")
            print(f"Username: {username}")
            print(f"Password: {password}")
            print("\nYou can now login to the application at http://localhost:5001")
        else:
            print("Failed to create user")
            return False
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)