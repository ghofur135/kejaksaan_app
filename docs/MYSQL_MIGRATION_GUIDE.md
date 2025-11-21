# MySQL Migration Guide

## Overview

Dokumen ini menjelaskan proses migrasi database Kejaksaan App dari SQLite ke MySQL yang telah berhasil dilakukan.

## Prerequisites

- Python 3.7+
- MySQL Server (AWS RDS)
- MySQL connector for Python
- Environment variables configuration

## Migration Components

### 1. Configuration Files

#### `.env` File
```env
DB_HOST=ls-bb6ba3d6e32d38edc9b01930d6e73d79c92174ed.ctaoewic65ca.ap-southeast-1.rds.amazonaws.com
DB_NAME=db_kejaksaan_app
DB_USER=kejaksaan
DB_PASSWORD=kejaksaan2025#!
DB_PORT=3306
```

#### `src/config.py`
- Mengelola konfigurasi database dari environment variables
- Menyediakan parameter koneksi MySQL

### 2. Database Schema

#### `scripts/mysql_schema.sql`
- Schema database yang kompatibel dengan MySQL
- Termasuk proper data types, indexes, dan constraints
- Menggunakan InnoDB engine dengan UTF-8 charset

### 3. Database Layer

#### `src/models/mysql_database.py`
- Implementasi lengkap fungsi database untuk MySQL
- Context manager untuk koneksi database
- Konversi query dari SQLite ke MySQL syntax

### 4. Migration Scripts

#### `scripts/migrate_sqlite_to_mysql.py`
- Script otomatis untuk migrasi data
- Memigrasi users, pidum_data, dan pidsus_data
- Verifikasi hasil migrasi

## Migration Results

### Data Migrated Successfully
- **Users**: 1 record
- **PIDUM Data**: 261 records
- **PIDSUS Data**: 7 records

### Verification
- Semua data berhasil dimigrasi tanpa kehilangan
- Primary keys dan foreign keys terjaga
- Data integrity terverifikasi

## Key Changes

### Query Syntax Changes
1. **Date Functions**:
   - SQLite: `strftime('%Y-%m', tanggal)`
   - MySQL: `DATE_FORMAT(tanggal, '%Y-%m')`

2. **Boolean Values**:
   - SQLite: `TRUE/FALSE`
   - MySQL: `1/0`

3. **Parameter Placeholders**:
   - SQLite: `?`
   - MySQL: `%s`

### Connection Management
- Menggunakan `mysql.connector` instead of `sqlite3`
- Context manager untuk proper connection handling
- Connection pooling support

## Running the Application

### Start Application
```bash
python src/app_with_db.py
```

### Access Application
- URL: http://localhost:5001
- Login dengan username dan password yang ada di database

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Pastikan MySQL server accessible
   - Check kredensial di `.env`
   - Verify network connectivity

2. **Character Encoding**
   - Gunakan UTF-8 charset di MySQL
   - Set proper collation (utf8mb4_unicode_ci)

3. **Permission Issues**
   - Pastikan user MySQL memiliki proper privileges
   - Check database dan table permissions

### Rollback Plan

Jika perlu rollback ke SQLite:
1. Hentikan aplikasi
2. Restore backup SQLite database
3. Update imports di `src/app_with_db.py`
4. Install kembali dependencies SQLite

## Performance Considerations

### MySQL Optimizations
- Indexes untuk frequently queried columns
- Proper data types untuk storage efficiency
- Connection pooling untuk concurrent access

### Monitoring
- Monitor connection pool usage
- Track query performance
- Monitor database size growth

## Security

### Credentials Management
- Store credentials di `.env` file
- Never commit credentials ke version control
- Use strong passwords
- Regular password rotation

### Network Security
- Use SSL/TLS untuk database connections
- Implement proper firewall rules
- Consider VPN untuk remote access

## Maintenance

### Regular Tasks
- Database backups
- Performance monitoring
- Security updates
- Schema migrations

### Backup Strategy
```bash
# MySQL backup
mysqldump -h HOST -u USER -p DB_NAME > backup.sql

# Restore backup
mysql -h HOST -u USER -p DB_NAME < backup.sql
```

## Future Enhancements

### Possible Improvements
1. Connection pooling optimization
2. Query optimization
3. Caching layer implementation
4. Read replica setup
5. Database sharding for scalability

### Monitoring Tools
- MySQL Performance Schema
- Slow query log
- Application-level monitoring
- Database metrics collection

## Support

For issues related to MySQL migration:
1. Check application logs
2. Verify database connection
3. Review error messages
4. Consult this documentation
5. Contact database administrator

---

**Migration completed successfully on: 2025-11-21**

**Total records migrated: 269**