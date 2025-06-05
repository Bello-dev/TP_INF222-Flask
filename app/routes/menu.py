from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields  # ← Ajout de 'fields'
from datetime import datetime
from app.db.db import db
from app.model import Menu, create_swagger_models  # ← Ajout de create_swagger_models

menu_bp = Blueprint('menu', __name__)

menus_ns = Namespace(
    "menus",
    description="Gestion des menus et planification de repas",
    path="/menus"
)

# Utiliser la fonction centralisée du model.py
models = create_swagger_models(menus_ns)

@menus_ns.route('/')
class MenusList(Resource):
    @menus_ns.marshal_list_with(models['menu'])
    def get(self):
        """📋 Liste tous les menus"""
        try:
            menus = Menu.query.all()
            return [menu.to_dict() for menu in menus], 200
        except Exception as e:
            menus_ns.abort(500, f"Erreur serveur: {str(e)}")

    @menus_ns.expect(models['menu_input'], validate=True)
    @menus_ns.marshal_with(models['menu'], code=201)
    def post(self):
        """➕ Créer un menu"""
        try:
            data = request.get_json()
            
            if not data or not data.get('nom'):
                menus_ns.abort(400, "Le nom du menu est requis")
            
            # Gestion de la date
            date_menu = None
            if data.get('date'):
                try:
                    date_menu = datetime.strptime(data['date'], '%Y-%m-%d').date()
                except ValueError:
                    menus_ns.abort(400, "Format de date invalide. Utilisez YYYY-MM-DD")
            
            nouveau_menu = Menu(
                nom=data['nom'],
                date=date_menu,
                type_repas=data.get('type_repas')
            )
            
            db.session.add(nouveau_menu)
            db.session.commit()
            
            return nouveau_menu.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            menus_ns.abort(500, f"Erreur lors de la création: {str(e)}")

@menus_ns.route('/<int:menu_id>')
@menus_ns.param('menu_id', 'ID du menu')
class MenuDetail(Resource):
    @menus_ns.marshal_with(models['menu'])
    def get(self, menu_id):
        """🔍 Obtenir un menu par ID"""
        menu = Menu.query.get_or_404(menu_id)
        return menu.to_dict()

    @menus_ns.expect(models['menu_input'], validate=True)
    @menus_ns.marshal_with(models['menu'])
    def put(self, menu_id):
        """✏️ Modifier un menu"""
        menu = Menu.query.get_or_404(menu_id)
        data = request.get_json()
        
        try:
            menu.nom = data.get('nom', menu.nom)
            
            # Gestion de la date
            if data.get('date'):
                try:
                    menu.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
                except ValueError:
                    menus_ns.abort(400, "Format de date invalide. Utilisez YYYY-MM-DD")
            
            menu.type_repas = data.get('type_repas', menu.type_repas)
            
            db.session.commit()
            return menu.to_dict()
            
        except Exception as e:
            db.session.rollback()
            menus_ns.abort(500, f"Erreur lors de la modification: {str(e)}")

    @menus_ns.marshal_with(models['message'])
    def delete(self, menu_id):
        """🗑️ Supprimer un menu"""
        try:
            menu = Menu.query.get_or_404(menu_id)
            nom_menu = menu.nom
            db.session.delete(menu)
            db.session.commit()
            return {'message': f'Menu "{nom_menu}" supprimé avec succès', 'success': True, 'id': menu_id}, 200
            
        except Exception as e:
            db.session.rollback()
            menus_ns.abort(500, f"Erreur lors de la suppression: {str(e)}")

@menus_ns.route('/type/<string:type_repas>')
@menus_ns.param('type_repas', 'Type de repas (Petit-déjeuner, Déjeuner, Dîner)')
class MenusByType(Resource):
    @menus_ns.marshal_list_with(models['menu'])
    def get(self, type_repas):
        """🍽️ Obtenir les menus par type de repas"""
        try:
            menus = Menu.query.filter_by(type_repas=type_repas).all()
            return [menu.to_dict() for menu in menus], 200
        except Exception as e:
            menus_ns.abort(500, f"Erreur lors de la récupération: {str(e)}")

# ============= ROUTES FLASK CLASSIQUES (inchangées) =============

@menu_bp.route("/", methods=["GET"])
def get_all():
    """Route Flask existante - reste inchangée"""
    menus = Menu.query.all()
    return jsonify([menu.to_dict() for menu in menus])

@menu_bp.route("/", methods=["POST"])
def create():
    """Route Flask existante - reste inchangée"""
    data = request.get_json()
    
    if not data or not data.get('nom'):
        return jsonify({'error': 'Le nom est requis'}), 400
    
    try:
        # Gestion de la date
        date_menu = None
        if data.get('date'):
            try:
                date_menu = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}), 400
        
        nouveau_menu = Menu(
            nom=data['nom'],
            date=date_menu,
            type_repas=data.get('type_repas')
        )
        
        db.session.add(nouveau_menu)
        db.session.commit()
        
        return jsonify(nouveau_menu.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@menu_bp.route("/<int:menu_id>", methods=["GET"])
def get_menu(menu_id):
    """Route Flask existante - reste inchangée"""
    menu = Menu.query.get_or_404(menu_id)
    return jsonify(menu.to_dict())

@menu_bp.route("/<int:menu_id>", methods=["PUT"])
def update(menu_id):
    """Route Flask existante - reste inchangée"""
    menu = Menu.query.get_or_404(menu_id)
    data = request.get_json()
    
    try:
        menu.nom = data.get('nom', menu.nom)
        
        # Gestion de la date
        if data.get('date'):
            try:
                menu.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}), 400
        
        menu.type_repas = data.get('type_repas', menu.type_repas)
        
        db.session.commit()
        return jsonify(menu.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@menu_bp.route("/<int:menu_id>", methods=["DELETE"])
def delete_menu(menu_id):
    """Route Flask existante - reste inchangée"""
    try:
        menu = Menu.query.get_or_404(menu_id)
        db.session.delete(menu)
        db.session.commit()
        return jsonify({'message': 'Menu supprimé avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500