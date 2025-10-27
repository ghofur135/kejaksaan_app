# Step-by-Step Installation Guide

## Prerequisites
- Python 3.13.3 is installed on your system
- Command prompt/terminal access

## Detailed Installation Steps

### Step 1: Backup Current Environment (Optional)
If you want to preserve your current virtual environment:
```
ren venv venv_backup
```

### Step 2: Update requirements.txt
Replace the content of requirements.txt with:
```
Flask==2.3.3
pandas==2.2.2
openpyxl==3.1.2
matplotlib==3.8.4
numpy==1.26.4
Werkzeug==2.3.7
Jinja2==3.1.2
itsdangerous==2.1.2
click==8.1.7
MarkupSafe==2.1.3
gunicorn==23.0.0
setuptools==69.5.1
```

### Step 3: Create New Virtual Environment
```
python -m venv venv
```

### Step 4: Activate Virtual Environment
On Windows:
```
venv\Scripts\activate
```

On Linux/Mac:
```
source venv/bin/activate
```

### Step 5: Upgrade Build Tools
```
python -m pip install --upgrade pip setuptools wheel
```

### Step 6: Install Requirements
```
pip install -r requirements.txt
```

### Step 7: Verify Installation
```
python -c "import flask, pandas, matplotlib, numpy; print('All packages imported successfully')"
```

### Step 8: Run the Application
```
python app_with_db.py
```

## Troubleshooting

### If Installation Still Fails
1. Clear pip cache:
   ```
   pip cache purge
   ```

2. Try installing packages individually:
   ```
   pip install setuptools==69.5.1
   pip install numpy==1.26.4
   pip install pandas==2.2.2
   pip install matplotlib==3.8.4
   pip install Flask==2.3.3
   pip install openpyxl==3.1.2
   pip install gunicorn==23.0.0
   ```

### Alternative: Use Python 3.11
If Python 3.13 continues to cause issues:
1. Download and install Python 3.11 from python.org
2. Create virtual environment with Python 3.11:
   ```
   py -3.11 -m venv venv
   ```
3. Use the original requirements.txt:
   ```
   Flask==2.3.3
   pandas==2.0.3
   openpyxl==3.1.2
   matplotlib==3.7.2
   numpy==1.24.3
   Werkzeug==2.3.7
   Jinja2==3.1.2
   itsdangerous==2.1.2
   click==8.1.7
   MarkupSafe==2.1.3
   gunicorn==23.0.0
   ```

## Verification Checklist
- [ ] Virtual environment created successfully
- [ ] All packages installed without errors
- [ ] Application starts without import errors
- [ ] Database initializes correctly
- [ ] Web interface loads in browser