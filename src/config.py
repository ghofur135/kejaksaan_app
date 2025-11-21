import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'kejaksaan_app')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
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