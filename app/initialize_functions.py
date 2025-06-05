from flask import Blueprint

def register_blueprints(app, api=None):
    """Enregistrer tous les blueprints de l'application"""
    
    # Import des blueprints (toujours nécessaires)
    from app.routes.aliments import aliments_bp
    from app.routes.recettes import recettes_bp
    from app.routes.utilisateurs import utilisateurs_bp
    from app.routes.recommandations import recommandations_bp
    from app.routes.menu import menu_bp
    from app.routes.buffet import buffet_bp
    from app.routes.categories import categories_bp
    from app.routes.generation import generation_bp
    from app.routes.menu_auto import menu_auto_bp
    from app.routes.planificateur import planificateur_bp

    # Enregistrer tous les blueprints Flask
    app.register_blueprint(aliments_bp)
    app.register_blueprint(recettes_bp)
    app.register_blueprint(utilisateurs_bp)
    app.register_blueprint(recommandations_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(buffet_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(generation_bp)
    app.register_blueprint(menu_auto_bp)
    app.register_blueprint(planificateur_bp)

    # Si Swagger est activé, ajouter les namespaces (avec protection d'erreur)
    if api is not None:
        try:
            from app.routes.aliments import aliments_ns
            api.add_namespace(aliments_ns, path='/aliments')
        except ImportError as e:
            print(f"⚠️ Namespace aliments non trouvé: {e}")
        
        try:
            from app.routes.recettes import recettes_ns
            api.add_namespace(recettes_ns, path='/recettes')
        except ImportError as e:
            print(f"⚠️ Namespace recettes non trouvé: {e}")
        
        try:
            from app.routes.utilisateurs import utilisateurs_ns
            api.add_namespace(utilisateurs_ns, path='/utilisateurs')
        except ImportError as e:
            print(f"⚠️ Namespace utilisateurs non trouvé: {e}")
        
        try:
            from app.routes.recommandations import recommandations_ns
            api.add_namespace(recommandations_ns, path='/recommandations')
        except ImportError as e:
            print(f"⚠️ Namespace recommandations non trouvé: {e}")
        
        try:
            from app.routes.menu import menus_ns
            api.add_namespace(menus_ns, path='/menus')
        except ImportError as e:
            print(f"⚠️ Namespace menus non trouvé: {e}")
        
        try:
            from app.routes.buffet import buffets_ns
            api.add_namespace(buffets_ns, path='/buffets')
        except ImportError as e:
            print(f"⚠️ Namespace buffets non trouvé: {e}")
        
        try:
            from app.routes.categories import categories_ns
            api.add_namespace(categories_ns, path='/categories')
        except ImportError as e:
            print(f"⚠️ Namespace categories non trouvé: {e}")
        
        try:
            from app.routes.generation import generation_ns
            api.add_namespace(generation_ns, path='/generation')
        except ImportError as e:
            print(f"⚠️ Namespace generation non trouvé: {e}")
        
        try:
            from app.routes.menu_auto import menu_auto_ns
            api.add_namespace(menu_auto_ns, path='/menu_auto')
        except ImportError as e:
            print(f"⚠️ Namespace menu_auto non trouvé: {e}")
        
        try:
            from app.routes.planificateur import planificateur_ns
            api.add_namespace(planificateur_ns, path='/planificateur')
        except ImportError as e:
            print(f"⚠️ Namespace planificateur non trouvé: {e}")