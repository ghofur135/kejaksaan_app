# Git Ignore Update - Kejaksaan App

## Perubahan pada .gitignore

### Folder dan Files yang Ditambahkan ke .gitignore:

#### **Python Related:**
- `__pycache__/` - Python compiled bytecode
- `*.py[cod]` - Python compiled files
- `*$py.class` - Python class files
- `*.so` - Shared object files
- `.Python` - Python environment marker
- `build/`, `develop-eggs/`, `dist/`, `downloads/`, `eggs/`, `.eggs/` - Python build artifacts
- `lib/`, `lib64/`, `parts/`, `sdist/`, `var/`, `wheels/` - Python package directories
- `*.egg-info/`, `.installed.cfg`, `*.egg`, `MANIFEST` - Python package metadata

#### **Virtual Environments:**
- `venv/` - Virtual environment directory
- `env/`, `ENV/`, `.venv/`, `.env/` - Alternative virtual environment names

#### **Flask Related:**
- `instance/` - Flask instance folder
- `.webassets-cache` - Flask assets cache
- `flask.log` - Flask log files

#### **PM2 Logs:**
- `logs/` - PM2 log directory
- `*.log` - All log files

#### **Database Files:**
- `*.db` - SQLite database files
- `!kejaksaan.db` - Exception: Keep the main kejaksaan.db in tracking

## Alasan Perubahan

### 1. **Logs Folder**
- Log files bersifat temporary dan generated
- Ukuran file log bisa sangat besar
- Berisi informasi runtime yang tidak perlu di-commit
- Setiap environment akan generate log sendiri

### 2. **Python Files**
- `__pycache__` dan compiled files akan regenerate otomatis
- Virtual environment folder berisi dependencies yang bisa diinstall ulang
- Build artifacts tidak perlu di-commit

### 3. **Database Files**
- Database files berisi data yang bersifat instance-specific
- Exception untuk `kejaksaan.db` karena mungkin berisi sample data

## Files yang Sudah Dihapus dari Tracking
- `logs/kejaksaan-flask-app-error.log`
- `logs/kejaksaan-flask-app-out.log`
- `logs/kejaksaan-flask-app.log`

## Best Practices
- Log files akan tetap tergenerate di local tapi tidak akan di-commit
- Folder `logs/` tetap ada untuk functionality PM2
- Database production tidak akan ter-commit secara tidak sengaja
- Repository akan lebih clean dan fokus pada source code

## Commit Message Suggestion
```
git commit -m "Update .gitignore: Add Python, Flask, PM2 logs, and database exclusions"
```