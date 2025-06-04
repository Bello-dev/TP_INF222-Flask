from flask import Flask
from flask_migrate import Migrate
from app.db.db import db
from app.initialize_functions import register_blueprints

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False  # ← Ajouter cette ligne

    app.config.from_object("app.config.config.Config")
    
    db.init_app(app)
    Migrate(app, db)
    register_blueprints(app)
    
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
