import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.db.db import db
from app.config.config import Config
from app.initialize_functions import register_blueprints

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False # Désactive les erreurs 404 pour les chemins avec ou sans slash final
    app.config.from_object('app.config.config.Config')
    db.init_app(app)
    Migrate(app, db)
    register_blueprints(app)
    
    return app