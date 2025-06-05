import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Utiliser DATABASE_URL en priorité (pour Docker)
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Configuration locale de fallback
        SQLALCHEMY_DATABASE_URI = ('postgresql://tp222_flask:INF222@localhost:5432/aliments_db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key'