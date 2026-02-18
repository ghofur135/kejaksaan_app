#!/usr/bin/env python3
"""
Entry point untuk menjalankan aplikasi Kejaksaan (Desktop Version)
"""

import sys
import os
import threading
import webview
import time

# Tambahkan folder src ke Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import logging

# Configure logging to file
log_file = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'app.log')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

from app_with_db import app

def start_server():
    """Function to run Flask server in a separate thread"""
    try:
        app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
    except Exception as e:
        logging.error(f"Flask server failed to start: {e}", exc_info=True)

if __name__ == '__main__':
    print("Starting Kejaksaan App (Desktop)...")
    print("Database: MySQL (AWS RDS)")
    
    # Start Flask in a background thread
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    
    # Give Flask a moment to start
    time.sleep(1)
    
    # Create a desktop window
    webview.create_window('Aplikasi Kejaksaan', 'http://127.0.0.1:5001')
    webview.start()
    
    sys.exit()