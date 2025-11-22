import sys
import os

# Tambahkan src ke Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_path = os.path.join(parent_dir, 'src')
sys.path.insert(0, src_path)

try:
    from app_with_db import app
    print("App imported successfully!")
except Exception as e:
    print(f"Error importing app: {e}")
    raise

# Export untuk Vercel
# app sudah tersedia dari import di atas
