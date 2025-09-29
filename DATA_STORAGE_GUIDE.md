# 📊 DATA STORAGE GUIDE - Aplikasi PIDUM & PIDSUS

## 🔍 **LOKASI PENYIMPANAN DATA**

### **Aplikasi Versi LAMA (app.py):**
```
❌ MEMORY STORAGE (Temporary)
├── pidum_data = [] (Python list)
├── pidsus_data = [] (Python list)
└── Data HILANG saat aplikasi restart!
```

### **Aplikasi Versi BARU (app_with_db.py):**
```
✅ DATABASE PERSISTENT (SQLite)
├── Database File: d:\#DHIMAS_BACKUP#\#opreker#\kejaksaan\db\kejaksaan.db
├── Table: pidum_data (data PIDUM)
├── Table: pidsus_data (data PIDSUS)
└── Data TERSIMPAN PERMANEN!
```

## 🚀 **MIGRASI KE DATABASE**

### 1. **Struktur Database SQLite:**

**Tabel PIDUM:**
```sql
CREATE TABLE pidum_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    no TEXT NOT NULL,
    periode TEXT NOT NULL,
    tanggal TEXT NOT NULL,
    jenis_perkara TEXT NOT NULL,
    pra_penututan TEXT NOT NULL,
    penuntutan TEXT NOT NULL,
    upaya_hukum TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Tabel PIDSUS:**
```sql
CREATE TABLE pidsus_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    no TEXT NOT NULL,
    periode TEXT NOT NULL,
    tanggal TEXT NOT NULL,
    jenis_perkara TEXT NOT NULL,
    penyidikan TEXT NOT NULL,
    penuntutan TEXT NOT NULL,
    keterangan TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. **File yang Ditambahkan:**
- `database.py` - Modul database functions
- `app_with_db.py` - Aplikasi Flask dengan database
- `kejaksaan.db` - File database SQLite

### 3. **Cara Menjalankan Versi Database:**
```bash
# Gunakan app versi database
python app_with_db.py

# Buka di browser
http://127.0.0.1:5001
```

## 📂 **STRUKTUR DIREKTORI DATABASE**

```
kejaksaan/
├── app.py                    # Versi LAMA (memory storage)
├── app_with_db.py           # Versi BARU (database storage)
├── database.py              # Database functions
├── db/
│   ├── custom.db           # File lama (tidak terpakai)
│   └── kejaksaan.db        # Database baru (aktif)
└── requirements.txt        # Dependencies
```

## 🔧 **DATABASE OPERATIONS**

### **Fungsi Utama dalam database.py:**

```python
# Initialize database
init_database()

# Insert data
insert_pidum_data(data)
insert_pidsus_data(data)

# Retrieve data
get_all_pidum_data()
get_all_pidsus_data()
get_pidum_data_for_export()
get_pidsus_data_for_export()

# Database stats
get_database_stats()
```

### **Test Database dari Command Line:**
```bash
# Check database
python -c "from database import get_database_stats; print(get_database_stats())"

# Test insert
python -c "
from database import insert_pidum_data, get_database_stats
data = {'NO': '001', 'PERIODE': '2025-Q1', 'TANGGAL': '2025-09-29', 'JENIS PERKARA': 'Test', 'PRA PENUTUTAN': 'Test', 'PENUNTUTAN': 'Test', 'UPAYA HUKUM': 'Test'}
insert_pidum_data(data)
print(get_database_stats())
"
```

## 📊 **PERBANDINGAN VERSI**

| Aspek | app.py (LAMA) | app_with_db.py (BARU) |
|-------|---------------|------------------------|
| **Storage** | Memory (list) | SQLite Database |
| **Persistence** | ❌ Data hilang | ✅ Data tersimpan |
| **Performance** | Cepat | Sedikit lebih lambat |
| **Scalability** | Terbatas | Scalable |
| **Backup** | Tidak ada | File .db |
| **Multi-user** | Tidak support | Bisa support |
| **Query** | Python list | SQL |

## 🛠️ **MAINTENANCE DATABASE**

### **Backup Database:**
```bash
# Copy file database
copy "d:\#DHIMAS_BACKUP#\#opreker#\kejaksaan\db\kejaksaan.db" "backup_kejaksaan_2025-09-29.db"
```

### **View Database dengan Tools:**
- **DB Browser for SQLite** (Recommended)
- **SQLite Expert**  
- **DBeaver**
- **Command Line:** `sqlite3 kejaksaan.db`

### **Query Manual:**
```bash
# Masuk ke SQLite
sqlite3 "d:\#DHIMAS_BACKUP#\#opreker#\kejaksaan\db\kejaksaan.db"

# Query data
SELECT * FROM pidum_data;
SELECT * FROM pidsus_data;
SELECT COUNT(*) FROM pidum_data;
```

## ✅ **REKOMENDASI**

1. **Gunakan `app_with_db.py`** untuk produksi
2. **Backup database** secara rutin
3. **Monitor pertumbuhan file** database
4. **Implementasi pagination** jika data banyak
5. **Add indexing** untuk performa query

## 🚨 **MIGRATION PATH**

Jika sudah ada data di versi lama:
1. Input ulang data ke versi database
2. Atau buat script migration (jika perlu)
3. Verifikasi data sudah tersimpan
4. Hapus versi lama setelah yakin

---

**STATUS SAAT INI:** ✅ Database SQLite sudah siap dan berfungsi!
**Lokasi Database:** `d:\#DHIMAS_BACKUP#\#opreker#\kejaksaan\db\kejaksaan.db`