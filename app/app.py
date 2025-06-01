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
    app.config.from_object('app.config.config.Config')
    db.init_app(app)
    Migrate(app, db)
    register_blueprints(app)
    
    return app
