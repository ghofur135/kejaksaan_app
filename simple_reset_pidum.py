#!/usr/bin/env python3
"""
Script Simple untuk Reset Data PIDUM
Versi sederhana untuk reset cepat

Usage:
    python3 simple_reset_pidum.py
"""

import sqlite3
import os
from datetime import datetime
import shutil

# Path database
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'kejaksaan.db')

def get_pidum_count():
    """Mendapatkan jumlah data PIDUM"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pidum_data")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Error: {e}")
        return 0

def create_backup():
    """Membuat backup database"""
    try:
        backup_dir = os.path.join(os.path.dirname(__file__), 'db')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"kejaksaan_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_name)
        
        shutil.copy2(DB_PATH, backup_path)
        print(f"✅ Backup created: {backup_name}")
        return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def reset_all_pidum():
    """Reset semua data PIDUM"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Hapus semua data
        cursor.execute("DELETE FROM pidum_data")
        deleted_count = cursor.rowcount
        
        # Reset auto increment
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='pidum_data'")
        
        conn.commit()
        conn.close()
        
        return deleted_count
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

def main():
    print("=" * 50)
    print("🗃️  SIMPLE RESET DATA PIDUM")
    print("=" * 50)
    
    # Cek database
    if not os.path.exists(DB_PATH):
        print("❌ Database tidak ditemukan!")
        return
    
    # Tampilkan jumlah data current
    current_count = get_pidum_count()
    print(f"\n📊 Data PIDUM saat ini: {current_count} records")
    
    if current_count == 0:
        print("✅ Database PIDUM sudah kosong.")
        return
    
    # Konfirmasi
    print(f"\n⚠️  WARNING: Akan menghapus SEMUA {current_count} data PIDUM!")
    
    response = input("\nLanjutkan? (y/N): ").lower().strip()
    if response not in ['y', 'yes']:
        print("❌ Reset dibatalkan.")
        return
    
    # Buat backup
    print("\n🔄 Creating backup...")
    if not create_backup():
        print("❌ Backup gagal. Reset dibatalkan.")
        return
    
    # Reset data
    print("🔄 Resetting data...")
    deleted_count = reset_all_pidum()
    
    if deleted_count > 0:
        print(f"✅ Berhasil menghapus {deleted_count} data PIDUM")
        
        # Verifikasi
        new_count = get_pidum_count()
        print(f"📊 Data PIDUM sekarang: {new_count} records")
    else:
        print("❌ Reset gagal!")
    
    print("=" * 50)

if __name__ == "__main__":
    main()