from app.routes.aliments import aliments_bp
from app.routes.buffet import buffet_bp
from app.routes.categories import categories_bp
from app.routes.menu import menu_bp
from app.routes.planificateur import planificateur_bp
from app.routes.utilisateurs import utilisateurs_bp
from app.routes.recettes import recettes_bp
from app.routes.recommandations import recommandations_bp

def register_blueprints(app):
    app.register_blueprint(aliments_bp)
    app.register_blueprint(buffet_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(planificateur_bp)
    app.register_blueprint(utilisateurs_bp)
    app.register_blueprint(recettes_bp)
    app.register_blueprint(recommandations_bp)

