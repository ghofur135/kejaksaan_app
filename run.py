#!/usr/bin/env python3
"""
Entry point untuk menjalankan aplikasi Kejaksaan
"""

import sys
import os

# Tambahkan folder src ke Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app_with_db import app

if __name__ == '__main__':
    print("Starting Kejaksaan App...")
    print(f"Database initialized at: {app.config.get('DATABASE_PATH', os.path.join(os.path.dirname(__file__), 'db', 'kejaksaan.db'))}")
    app.run(host='0.0.0.0', port=5001, debug=True)