from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from app.db.db import db
from app.initialize_functions import register_blueprints
import os

def create_app():
    """Factory function principale avec API Flask-RESTX"""
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # 🔧 DEBUG: Afficher les variables d'environnement importantes
    print(f"🔍 DATABASE_URL trouvée: {os.environ.get('DATABASE_URL', 'NON TROUVÉE')}")
    print(f"🔍 FLASK_ENV: {os.environ.get('FLASK_ENV', 'NON DÉFINIE')}")
    
    app.config.from_object("app.config.config.Config")
    
    # 🔧 DEBUG: Vérifier la config après chargement
    print(f"🔍 SQLALCHEMY_DATABASE_URI utilisée: {app.config.get('SQLALCHEMY_DATABASE_URI', 'NON DÉFINIE')}")
    
    # Configuration Swagger/OpenAPI
    api = Api(
        app, 
        version='1.0', 
        title='🍽️ TP 222 Flask - API Aliments & Recettes',
        description='''
        ## API REST pour la gestion des aliments, recettes et recommandations nutritionnelles

        ### Fonctionnalités principales :
        - 🥗 **Aliments** : Gestion complète des aliments et valeurs nutritionnelles
        - 🍳 **Recettes** : Création et gestion de recettes culinaires
        - 👤 **Utilisateurs** : Gestion des profils utilisateurs
        - 💡 **Recommandations** : Suggestions personnalisées
        - 🍽️ **Menus** : Planification de repas
        - 🎉 **Buffets** : Organisation d'événements

        ### Utilisation :
        1. Explorez les endpoints disponibles ci-dessous
        2. Cliquez sur "Try it out" pour tester une API
        3. Remplissez les paramètres et cliquez "Execute"
        ''',
        doc='/swagger-ui/',
        contact='Équipe TP 222 Flask',
        license='MIT License',
        prefix='/api'
    )
    
    # Initialiser la base de données et les migrations
    db.init_app(app)
    Migrate(app, db)
    
    # Enregistrer les blueprints avec l'API
    register_blueprints(app, api)
    
    return app

# Créer l'instance de l'application
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)