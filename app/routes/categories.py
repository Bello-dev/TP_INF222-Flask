from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource
from app.db.db import db
from app.model import Categorie, create_swagger_models  # ← Import unifié

categories_bp = Blueprint("categories", __name__)

categories_ns = Namespace(
    "categories",
    description="Gestion des catégories d'aliments",
    path="/categories"
)

# Utiliser la fonction centralisée du model.py
models = create_swagger_models(categories_ns)

@categories_ns.route('/')
class CategoriesList(Resource):
    @categories_ns.marshal_list_with(models['categorie'])
    def get(self):
        """📋 Liste toutes les catégories"""
        try:
            categories = Categorie.query.all()
            return [cat.to_dict() for cat in categories], 200
        except Exception as e:
            categories_ns.abort(500, f"Erreur serveur: {str(e)}")

    @categories_ns.expect(models['categorie_input'], validate=True)
    @categories_ns.marshal_with(models['categorie'], code=201)
    def post(self):
        """➕ Créer une nouvelle catégorie"""
        try:
            data = request.get_json()
            
            if not data or not data.get('nom'):
                categories_ns.abort(400, "Le nom de la catégorie est requis")
            
            nouvelle_categorie = Categorie(
                nom=data['nom'],
                description=data.get('description')
            )
            
            db.session.add(nouvelle_categorie)
            db.session.commit()
            
            return nouvelle_categorie.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            categories_ns.abort(500, f"Erreur lors de la création: {str(e)}")

@categories_ns.route('/<int:categorie_id>')
@categories_ns.param('categorie_id', 'ID de la catégorie')
class CategoriesDetail(Resource):
    @categories_ns.marshal_with(models['categorie'])
    def get(self, categorie_id):
        """🔍 Obtenir une catégorie par ID"""
        categorie = Categorie.query.get_or_404(categorie_id)
        return categorie.to_dict()

    @categories_ns.expect(models['categorie_input'], validate=True)
    @categories_ns.marshal_with(models['categorie'])
    def put(self, categorie_id):
        """✏️ Modifier une catégorie"""
        categorie = Categorie.query.get_or_404(categorie_id)
        data = request.get_json()
        
        try:
            categorie.nom = data.get('nom', categorie.nom)
            categorie.description = data.get('description', categorie.description)
            
            db.session.commit()
            return categorie.to_dict()
            
        except Exception as e:
            db.session.rollback()
            categories_ns.abort(500, f"Erreur lors de la modification: {str(e)}")

    @categories_ns.marshal_with(models['message'])
    def delete(self, categorie_id):
        """🗑️ Supprimer une catégorie"""
        try:
            categorie = Categorie.query.get_or_404(categorie_id)
            nom_categorie = categorie.nom
            db.session.delete(categorie)
            db.session.commit()
            return {'message': f'Catégorie "{nom_categorie}" supprimée avec succès', 'success': True, 'id': categorie_id}, 200
            
        except Exception as e:
            db.session.rollback()
            categories_ns.abort(500, f"Erreur lors de la suppression: {str(e)}")

# ============= ROUTES FLASK CLASSIQUES (inchangées) =============

@categories_bp.route("/", methods=["GET"])
def get_all():
    categories = Categorie.query.all()
    return jsonify([cat.to_dict() for cat in categories])

@categories_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    
    if not data or not data.get('nom'):
        return jsonify({'error': 'Le nom est requis'}), 400
    
    try:
        nouvelle_categorie = Categorie(
            nom=data['nom'],
            description=data.get('description')
        )
        
        db.session.add(nouvelle_categorie)
        db.session.commit()
        
        return jsonify(nouvelle_categorie.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@categories_bp.route("/<int:categorie_id>", methods=["GET"])
def get_categorie(categorie_id):
    categorie = Categorie.query.get_or_404(categorie_id)
    return jsonify(categorie.to_dict())

@categories_bp.route("/<int:categorie_id>", methods=["PUT"])
def update(categorie_id):
    categorie = Categorie.query.get_or_404(categorie_id)
    data = request.get_json()
    
    try:
        categorie.nom = data.get('nom', categorie.nom)
        categorie.description = data.get('description', categorie.description)
        
        db.session.commit()
        return jsonify(categorie.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@categories_bp.route("/<int:categorie_id>", methods=["DELETE"])
def delete(categorie_id):
    try:
        categorie = Categorie.query.get_or_404(categorie_id)
        db.session.delete(categorie)
        db.session.commit()
        return jsonify({'message': 'Catégorie supprimée avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500