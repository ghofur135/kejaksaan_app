#!/usr/bin/env python3
"""
Script untuk reset data PIDUM dari database
Aplikasi Kejaksaan - Data PIDUM & PIDSUS

Usage:
    python3 reset_pidum_data.py [options]
    
Options:
    --all           Reset semua data PIDUM
    --tahapan=X     Reset data berdasarkan tahapan (PRA PENUNTUTAN, PENUNTUTAN, UPAYA HUKUM)
    --periode=X     Reset data berdasarkan periode
    --confirm       Konfirmasi reset tanpa prompt
    --backup        Buat backup sebelum reset
"""

import sqlite3
import os
import sys
import argparse
from datetime import datetime
import shutil

# Path database
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'kejaksaan.db')
BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'db', 'backups')

def create_backup():
    """Membuat backup database sebelum reset"""
    try:
        # Buat folder backup jika belum ada
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # Generate nama file backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"kejaksaan_backup_{timestamp}.db"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        
        # Copy database ke backup
        shutil.copy2(DB_PATH, backup_path)
        
        print(f"✅ Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return None

def get_pidum_stats():
    """Mendapatkan statistik data PIDUM"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Total data PIDUM
        cursor.execute("SELECT COUNT(*) FROM pidum_data")
        total = cursor.fetchone()[0]
        
        # Data per tahapan
        cursor.execute("""
            SELECT tahapan_penanganan, COUNT(*) 
            FROM pidum_data 
            GROUP BY tahapan_penanganan
        """)
        tahapan_stats = cursor.fetchall()
        
        # Data per periode
        cursor.execute("""
            SELECT periode, COUNT(*) 
            FROM pidum_data 
            GROUP BY periode 
            ORDER BY periode
        """)
        periode_stats = cursor.fetchall()
        
        # Data per jenis perkara
        cursor.execute("""
            SELECT jenis_perkara, COUNT(*) 
            FROM pidum_data 
            GROUP BY jenis_perkara
        """)
        jenis_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            'total': total,
            'tahapan': tahapan_stats,
            'periode': periode_stats,
            'jenis': jenis_stats
        }
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return None

def reset_all_pidum(confirm=False):
    """Reset semua data PIDUM"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Hapus semua data PIDUM
        cursor.execute("DELETE FROM pidum_data")
        deleted_count = cursor.rowcount
        
        # Reset auto increment
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='pidum_data'")
        
        conn.commit()
        conn.close()
        
        print(f"✅ Successfully deleted {deleted_count} PIDUM records")
        return deleted_count
    except Exception as e:
        print(f"❌ Error resetting data: {e}")
        return 0

def reset_pidum_by_tahapan(tahapan, confirm=False):
    """Reset data PIDUM berdasarkan tahapan"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Hapus data berdasarkan tahapan
        cursor.execute("DELETE FROM pidum_data WHERE tahapan_penanganan = ?", (tahapan,))
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"✅ Successfully deleted {deleted_count} PIDUM records with tahapan '{tahapan}'")
        return deleted_count
    except Exception as e:
        print(f"❌ Error resetting data: {e}")
        return 0

def reset_pidum_by_periode(periode, confirm=False):
    """Reset data PIDUM berdasarkan periode"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Hapus data berdasarkan periode
        cursor.execute("DELETE FROM pidum_data WHERE periode = ?", (periode,))
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"✅ Successfully deleted {deleted_count} PIDUM records with periode '{periode}'")
        return deleted_count
    except Exception as e:
        print(f"❌ Error resetting data: {e}")
        return 0

def confirm_action(message):
    """Konfirmasi aksi dari user"""
    response = input(f"{message} (y/N): ").lower().strip()
    return response in ['y', 'yes']

def main():
    parser = argparse.ArgumentParser(description='Reset data PIDUM dari database')
    parser.add_argument('--all', action='store_true', help='Reset semua data PIDUM')
    parser.add_argument('--tahapan', type=str, help='Reset berdasarkan tahapan (PRA PENUNTUTAN, PENUNTUTAN, UPAYA HUKUM)')
    parser.add_argument('--periode', type=str, help='Reset berdasarkan periode')
    parser.add_argument('--confirm', action='store_true', help='Konfirmasi reset tanpa prompt')
    parser.add_argument('--backup', action='store_true', help='Buat backup sebelum reset')
    parser.add_argument('--stats', action='store_true', help='Tampilkan statistik data PIDUM saja')
    
    args = parser.parse_args()
    
    # Cek apakah database ada
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        sys.exit(1)
    
    print("=" * 60)
    print("🗃️  SCRIPT RESET DATA PIDUM")
    print("=" * 60)
    
    # Tampilkan statistik current data
    print("\n📊 STATISTIK DATA PIDUM SAAT INI:")
    stats = get_pidum_stats()
    if stats:
        print(f"   Total Records: {stats['total']}")
        
        if stats['tahapan']:
            print("   Per Tahapan:")
            for tahapan, count in stats['tahapan']:
                print(f"     - {tahapan}: {count} records")
        
        if stats['periode']:
            print("   Per Periode:")
            for periode, count in stats['periode']:
                print(f"     - Periode {periode}: {count} records")
        
        if stats['jenis']:
            print("   Per Jenis Perkara:")
            for jenis, count in stats['jenis']:
                print(f"     - {jenis}: {count} records")
    
    # Jika hanya ingin melihat stats
    if args.stats:
        print("\n✅ Statistik data ditampilkan.")
        sys.exit(0)
    
    # Validasi argumen
    if not any([args.all, args.tahapan, args.periode]):
        print("\n❌ Error: Pilih salah satu opsi reset (--all, --tahapan, atau --periode)")
        print("   Gunakan --help untuk melihat opsi yang tersedia")
        sys.exit(1)
    
    # Buat backup jika diminta
    backup_path = None
    if args.backup:
        print("\n🔄 Creating backup...")
        backup_path = create_backup()
        if not backup_path:
            print("❌ Backup failed. Aborting reset.")
            sys.exit(1)
    
    # Proses reset berdasarkan opsi
    deleted_count = 0
    
    if args.all:
        print(f"\n⚠️  WARNING: Akan menghapus SEMUA {stats['total']} data PIDUM!")
        if not args.confirm:
            if not confirm_action("Apakah Anda yakin ingin menghapus SEMUA data PIDUM?"):
                print("❌ Reset dibatalkan.")
                sys.exit(0)
        
        print("\n🔄 Resetting all PIDUM data...")
        deleted_count = reset_all_pidum(confirm=True)
    
    elif args.tahapan:
        tahapan = args.tahapan.upper()
        valid_tahapan = ['PRA PENUNTUTAN', 'PENUNTUTAN', 'UPAYA HUKUM']
        
        if tahapan not in valid_tahapan:
            print(f"❌ Error: Tahapan tidak valid. Pilih: {', '.join(valid_tahapan)}")
            sys.exit(1)
        
        # Hitung jumlah data yang akan dihapus
        tahapan_count = 0
        for t, count in stats['tahapan']:
            if t == tahapan:
                tahapan_count = count
                break
        
        print(f"\n⚠️  WARNING: Akan menghapus {tahapan_count} data PIDUM dengan tahapan '{tahapan}'!")
        if not args.confirm:
            if not confirm_action(f"Apakah Anda yakin ingin menghapus data tahapan '{tahapan}'?"):
                print("❌ Reset dibatalkan.")
                sys.exit(0)
        
        print(f"\n🔄 Resetting PIDUM data with tahapan '{tahapan}'...")
        deleted_count = reset_pidum_by_tahapan(tahapan, confirm=True)
    
    elif args.periode:
        periode = args.periode
        
        # Hitung jumlah data yang akan dihapus
        periode_count = 0
        for p, count in stats['periode']:
            if str(p) == periode:
                periode_count = count
                break
        
        print(f"\n⚠️  WARNING: Akan menghapus {periode_count} data PIDUM dengan periode '{periode}'!")
        if not args.confirm:
            if not confirm_action(f"Apakah Anda yakin ingin menghapus data periode '{periode}'?"):
                print("❌ Reset dibatalkan.")
                sys.exit(0)
        
        print(f"\n🔄 Resetting PIDUM data with periode '{periode}'...")
        deleted_count = reset_pidum_by_periode(periode, confirm=True)
    
    # Tampilkan hasil
    print("\n" + "=" * 60)
    print("📋 HASIL RESET:")
    print(f"   Data yang dihapus: {deleted_count} records")
    if backup_path:
        print(f"   Backup disimpan: {backup_path}")
    
    # Tampilkan statistik setelah reset
    print("\n📊 STATISTIK DATA PIDUM SETELAH RESET:")
    new_stats = get_pidum_stats()
    if new_stats:
        print(f"   Total Records: {new_stats['total']}")
        if new_stats['tahapan']:
            print("   Per Tahapan:")
            for tahapan, count in new_stats['tahapan']:
                print(f"     - {tahapan}: {count} records")
    
    print("\n✅ Reset completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()