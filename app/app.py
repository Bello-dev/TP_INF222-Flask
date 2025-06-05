import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.db.db import db
from app.config.config import Config
from app.initialize_functions import register_blueprints

load_dotenv()


def create_app():
    """Factory function pour créer l'application Flask - version simple sans API"""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object('app.config.config.Config')
    
    # Initialiser la base de données
    db.init_app(app)
    
    # Initialiser les migrations
    Migrate(app, db)
    
    # Enregistrer seulement les blueprints Flask (pas l'API)
    register_blueprints(app)
    
    return app