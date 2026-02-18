import PyInstaller.__main__
import os
import shutil
from PyInstaller.utils.hooks import collect_all

# Define paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
DIST_DIR = os.path.join(BASE_DIR, 'dist')
BUILD_DIR = os.path.join(BASE_DIR, 'build')

# Clean previous build
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

print("Starting build process...")

# Collect numpy manually to ensure all submodules are present (Fix for numpy 2.x issue)
datas, binaries, hiddenimports = collect_all('numpy')

# PyInstaller arguments
pyinstaller_args = [
    'run.py',                       # Entry point
    '--name=kejaksaan_app',         # Helper name
    '--onefile',                    # Create a single executable
    '--clean',                      # Clean cache
    f'--paths={SRC_DIR}',           # Add src to search path
    
    # Add data files (source;destination)
    # Note: On Windows use ; as separator, on Linux :
    f'--add-data={TEMPLATES_DIR};templates',
    f'--add-data={STATIC_DIR};static',
    
    # Hidden imports that PyInstaller might miss
    '--hidden-import=mysql.connector.plugins',
    '--hidden-import=mysql.connector.plugins.mysql_native_password',
    '--hidden-import=mysql.connector.plugins.caching_sha2_password',
    '--hidden-import=mysql.connector.plugins.mysql_clear_password',
    '--hidden-import=mysql.connector.plugins.sha256_password',
    '--hidden-import=engineio.async_drivers.threading', # Common for Flask-SocketIO if used, safe to add
    
    # Exclude modules (optional, to save space)
    # '--exclude-module=tkinter', 
    
    # Hide console window (Disabled for debugging)
    #'--noconsole',
]

# Add collected numpy data, binaries, and hidden imports
for d in datas:
    pyinstaller_args.append(f'--add-data={d[0]};{d[1]}')
for b in binaries:
    pyinstaller_args.append(f'--add-binary={b[0]};{b[1]}')
for h in hiddenimports:
    pyinstaller_args.append(f'--hidden-import={h}')

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print(f"Build complete. Executable is located at: {os.path.join(DIST_DIR, 'kejaksaan_app.exe')}")
print("IMPORTANT: Copy your .env file to the dist folder before running the executable!")
