from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource
from app.db.db import db
from app.model import Recette
from app.model import create_swagger_models

# Blueprint Flask existant
recettes_bp = Blueprint('recettes', __name__)

# Namespace Swagger (nouveau)
recettes_ns = Namespace('recettes', 
                       description='🍳 Gestion des recettes culinaires',
                       path='/recettes')

# Créer les modèles Swagger
models = create_swagger_models(recettes_ns)

# ============= ROUTES SWAGGER API (NOUVELLES) =============

@recettes_ns.route('/')
class RecettesList(Resource):
    @recettes_ns.doc('liste_recettes')
    @recettes_ns.marshal_list_with(models['recette'])
    def get(self):
        """📋 Récupérer toutes les recettes"""
        try:
            recettes = Recette.query.all()
            return [recette.to_dict() for recette in recettes], 200
        except Exception as e:
            recettes_ns.abort(500, f"Erreur serveur: {str(e)}")
    
    @recettes_ns.doc('creer_recette')
    @recettes_ns.expect(models['recette_input'], validate=True)
    @recettes_ns.marshal_with(models['recette'], code=201)
    def post(self):
        """➕ Créer une nouvelle recette"""
        try:
            data = request.get_json()
            
            if not data or not data.get('nom'):
                recettes_ns.abort(400, "Le nom de la recette est requis")
            
            if Recette.query.filter_by(nom=data['nom']).first():
                recettes_ns.abort(409, "Une recette avec ce nom existe déjà")
            
            nouvelle_recette = Recette(
                nom=data['nom'],
                description=data.get('description', ''),
                instructions=data.get('instructions', ''),
                temps_preparation=data.get('temps_preparation', 0),
                difficulte=data.get('difficulte', 'Facile'),
                portions=data.get('portions', 1)
            )
            
            db.session.add(nouvelle_recette)
            db.session.commit()
            
            return nouvelle_recette.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            recettes_ns.abort(500, f"Erreur lors de la création: {str(e)}")

@recettes_ns.route('/<int:recette_id>')
@recettes_ns.param('recette_id', 'ID unique de la recette')
class RecetteDetail(Resource):
    @recettes_ns.doc('obtenir_recette')
    @recettes_ns.marshal_with(models['recette'])
    def get(self, recette_id):
        """🔍 Obtenir une recette par son ID"""
        recette = Recette.query.get_or_404(recette_id)
        return recette.to_dict()
    
    @recettes_ns.doc('modifier_recette')
    @recettes_ns.expect(models['recette_input'])
    @recettes_ns.marshal_with(models['recette'])
    def put(self, recette_id):
        """✏️ Modifier une recette existante"""
        recette = Recette.query.get_or_404(recette_id)
        data = request.get_json()
        
        try:
            for key, value in data.items():
                if hasattr(recette, key) and key != 'id':
                    setattr(recette, key, value)
            
            db.session.commit()
            return recette.to_dict()
            
        except Exception as e:
            db.session.rollback()
            recettes_ns.abort(500, f"Erreur lors de la modification: {str(e)}")
    
    @recettes_ns.doc('supprimer_recette')
    @recettes_ns.marshal_with(models['message'])
    def delete(self, recette_id):
        """🗑️ Supprimer une recette"""
        try:
            recette = Recette.query.get_or_404(recette_id)
            nom_recette = recette.nom
            db.session.delete(recette)
            db.session.commit()
            return {'message': f'Recette "{nom_recette}" supprimée avec succès', 'success': True}, 200
            
        except Exception as e:
            db.session.rollback()
            recettes_ns.abort(500, f"Erreur lors de la suppression: {str(e)}")

# ============= VOS ROUTES FLASK EXISTANTES (INCHANGÉES) =============

@recettes_bp.route('/recettes', methods=['GET'])
def get_recettes():
    """Route Flask existante - reste inchangée"""
    recettes = Recette.query.all()
    return jsonify([recette.to_dict() for recette in recettes])

@recettes_bp.route('/recettes', methods=['POST'])
def create_recette():
    """Route Flask existante - reste inchangée"""
    data = request.get_json()
    
    if not data or not data.get('nom'):
        return jsonify({'error': 'Le nom est requis'}), 400
    
    try:
        nouvelle_recette = Recette(
            nom=data['nom'],
            description=data.get('description', ''),
            instructions=data.get('instructions', ''),
            temps_preparation=data.get('temps_preparation', 0),
            difficulte=data.get('difficulte', 'Facile'),
            portions=data.get('portions', 1)
        )
        
        db.session.add(nouvelle_recette)
        db.session.commit()
        
        return jsonify(nouvelle_recette.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recettes_bp.route('/recettes/<int:recette_id>', methods=['GET'])
def get_recette(recette_id):
    """Route Flask existante - reste inchangée"""
    recette = Recette.query.get_or_404(recette_id)
    return jsonify(recette.to_dict())

@recettes_bp.route('/recettes/<int:recette_id>', methods=['PUT'])
def update_recette(recette_id):
    """Route Flask existante - reste inchangée"""
    recette = Recette.query.get_or_404(recette_id)
    data = request.get_json()
    
    try:
        for key, value in data.items():
            if hasattr(recette, key) and key != 'id':
                setattr(recette, key, value)
        
        db.session.commit()
        return jsonify(recette.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recettes_bp.route('/recettes/<int:recette_id>', methods=['DELETE'])
def delete_recette(recette_id):
    """Route Flask existante - reste inchangée"""
    try:
        recette = Recette.query.get_or_404(recette_id)
        db.session.delete(recette)
        db.session.commit()
        return jsonify({'message': 'Recette supprimée avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500