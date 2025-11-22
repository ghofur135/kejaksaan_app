import sys
import os

# Tambahkan folder src ke Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app_with_db import app

# Vercel akan memanggil variabel 'app' ini
