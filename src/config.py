import os
from dotenv import load_dotenv
from pathlib import Path
import re

# Get the project root directory (parent of src)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from explicit path
dotenv_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=dotenv_path)

def read_password_from_env_file(dotenv_path):
    """Manually read password from .env file to handle # character"""
    try:
        with open(dotenv_path, 'r') as f:
            for line in f:
                # Match DB_PASSWORD line with quotes
                match = re.match(r"DB_PASSWORD=['\"](.+)['\"]", line.strip())
                if match:
                    return match.group(1)
                # Match DB_PASSWORD line without quotes (legacy)
                match = re.match(r"DB_PASSWORD=(.+)", line.strip())
                if match:
                    # Don't strip after # if no quotes
                    value = match.group(1)
                    return value
    except Exception:
        pass
    return os.getenv('DB_PASSWORD', '')

class Config:
    """Configuration class for the application"""

    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'kejaksaan_app')
    DB_USER = os.getenv('DB_USER', 'root')
    # Manually read password to handle # character
    DB_PASSWORD = read_password_from_env_file(dotenv_path)
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here_change_in_production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Database Connection String
    @staticmethod
    def get_mysql_connection_string():
        """Get MySQL connection string"""
        return (
            f"mysql+mysqlconnector://{Config.DB_USER}:{Config.DB_PASSWORD}"
            f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
        )
    
    # Database Connection Parameters
    @staticmethod
    def get_mysql_connection_params():
        """Get MySQL connection parameters"""
        return {
            'host': Config.DB_HOST,
            'database': Config.DB_NAME,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'port': Config.DB_PORT,
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True
        }