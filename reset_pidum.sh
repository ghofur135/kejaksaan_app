#!/bin/bash
# 
# Script Bash untuk Reset Data PIDUM
# Quick reset menggunakan SQL langsung
#

DB_PATH="./db/kejaksaan.db"
BACKUP_DIR="./db/backups"

echo "=================================================="
echo "🗃️  BASH SCRIPT - RESET DATA PIDUM"
echo "=================================================="

# Cek apakah database ada
if [ ! -f "$DB_PATH" ]; then
    echo "❌ Database tidak ditemukan: $DB_PATH"
    exit 1
fi

# Buat folder backup jika belum ada
mkdir -p "$BACKUP_DIR"

# Tampilkan jumlah data current
CURRENT_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM pidum_data;")
echo "📊 Data PIDUM saat ini: $CURRENT_COUNT records"

if [ "$CURRENT_COUNT" -eq 0 ]; then
    echo "✅ Database PIDUM sudah kosong."
    exit 0
fi

# Konfirmasi
echo ""
echo "⚠️  WARNING: Akan menghapus SEMUA $CURRENT_COUNT data PIDUM!"
echo ""
read -p "Lanjutkan? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Reset dibatalkan."
    exit 0
fi

# Buat backup
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/kejaksaan_backup_$TIMESTAMP.db"

echo ""
echo "🔄 Creating backup..."
cp "$DB_PATH" "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Backup created: $BACKUP_FILE"
else
    echo "❌ Backup failed!"
    exit 1
fi

# Reset data PIDUM
echo "🔄 Resetting data..."

# Hapus semua data PIDUM
sqlite3 "$DB_PATH" "DELETE FROM pidum_data;"

# Reset auto increment
sqlite3 "$DB_PATH" "DELETE FROM sqlite_sequence WHERE name='pidum_data';"

# Verifikasi hasil
NEW_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM pidum_data;")

echo ""
echo "📋 HASIL RESET:"
echo "   Data yang dihapus: $(($CURRENT_COUNT - $NEW_COUNT)) records"
echo "   Data tersisa: $NEW_COUNT records"
echo "   Backup: $BACKUP_FILE"
echo ""

if [ "$NEW_COUNT" -eq 0 ]; then
    echo "✅ Reset berhasil! Database PIDUM sekarang kosong."
else
    echo "⚠️  Warning: Masih ada $NEW_COUNT data tersisa."
fi

echo "=================================================="