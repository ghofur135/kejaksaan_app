#!/usr/bin/env python3
"""
Migration script to update database schema for tahapan penanganan system
"""

import sqlite3
import os
from database import DATABASE_PATH

def migrate_database():
    """Migrate database to new schema with tahapan_penanganan and keterangan"""
    
    # Backup existing database
    backup_path = DATABASE_PATH + '.backup'
    if os.path.exists(DATABASE_PATH):
        import shutil
        shutil.copy2(DATABASE_PATH, backup_path)
        print(f"✅ Database backed up to: {backup_path}")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if new columns exist
        cursor.execute("PRAGMA table_info(pidum_data)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'tahapan_penanganan' not in columns:
            print("🔄 Adding tahapan_penanganan column...")
            cursor.execute("ALTER TABLE pidum_data ADD COLUMN tahapan_penanganan TEXT DEFAULT 'PRA PENUNTUTAN'")
        
        if 'keterangan' not in columns:
            print("🔄 Adding keterangan column...")
            cursor.execute("ALTER TABLE pidum_data ADD COLUMN keterangan TEXT DEFAULT ''")
        
        # Remove old columns by creating new table and copying data
        print("🔄 Removing old columns (pra_penututan, penuntutan, upaya_hukum)...")
        
        # Create new table with correct schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pidum_data_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                no TEXT NOT NULL,
                periode TEXT NOT NULL,
                tanggal TEXT NOT NULL,
                jenis_perkara TEXT NOT NULL,
                tahapan_penanganan TEXT NOT NULL,
                keterangan TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Copy data from old table to new table
        cursor.execute('''
            INSERT INTO pidum_data_new (id, no, periode, tanggal, jenis_perkara, tahapan_penanganan, keterangan, created_at)
            SELECT id, no, periode, tanggal, jenis_perkara, 
                   COALESCE(tahapan_penanganan, 'PRA PENUNTUTAN'),
                   COALESCE(keterangan, ''),
                   created_at
            FROM pidum_data
        ''')
        
        # Drop old table and rename new table
        cursor.execute("DROP TABLE pidum_data")
        cursor.execute("ALTER TABLE pidum_data_new RENAME TO pidum_data")
        
        conn.commit()
        print("✅ Database migration completed successfully!")
        
        # Show statistics
        cursor.execute("SELECT COUNT(*) FROM pidum_data")
        pidum_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pidsus_data")
        pidsus_count = cursor.fetchone()[0]
        
        print(f"📊 Current data: {pidum_count} PIDUM records, {pidsus_count} PIDSUS records")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Starting database migration...")
    migrate_database()
    print("🎉 Migration completed!")