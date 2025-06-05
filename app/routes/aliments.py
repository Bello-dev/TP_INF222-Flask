from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource
from app.db.db import db
from app.model import Aliment
from app.model import create_swagger_models

# Blueprint Flask existant (garde la compatibilité)
aliments_bp = Blueprint('aliments', __name__)

# Namespace Swagger (nouveau)
aliments_ns = Namespace('aliments', 
                       description='🥗 Gestion des aliments et valeurs nutritionnelles',
                       path='/aliments')

# Créer les modèles Swagger
models = create_swagger_models(aliments_ns)

# ============= ROUTES SWAGGER API (NOUVELLES) =============

@aliments_ns.route('/')
class AlimentsList(Resource):
    @aliments_ns.doc('liste_aliments',
                    responses={
                        200: 'Liste des aliments récupérée avec succès',
                        500: 'Erreur serveur'
                    })
    @aliments_ns.marshal_list_with(models['aliment'])
    def get(self):
        """📋 Récupérer la liste de tous les aliments
        
        Retourne la liste complète des aliments avec leurs valeurs nutritionnelles.
        """
        try:
            aliments = Aliment.query.all()
            return [aliment.to_dict() for aliment in aliments], 200
        except Exception as e:
            aliments_ns.abort(500, f"Erreur serveur: {str(e)}")
    
    @aliments_ns.doc('creer_aliment',
                    responses={
                        201: 'Aliment créé avec succès',
                        400: 'Données invalides',
                        409: 'Aliment déjà existant',
                        500: 'Erreur serveur'
                    })
    @aliments_ns.expect(models['aliment_input'], validate=True)
    @aliments_ns.marshal_with(models['aliment'], code=201)
    def post(self):
        """➕ Créer un nouvel aliment
        
        Crée un nouvel aliment avec ses valeurs nutritionnelles.
        """
        try:
            data = request.get_json()
            
            if not data or not data.get('nom'):
                aliments_ns.abort(400, "Le nom de l'aliment est requis")
            
            if Aliment.query.filter_by(nom=data['nom']).first():
                aliments_ns.abort(409, "Un aliment avec ce nom existe déjà")
            
            nouvel_aliment = Aliment(
                nom=data['nom'],
                calories=data.get('calories', 0),
                proteines=data.get('proteines', 0),
                lipides=data.get('lipides', 0),
                glucides=data.get('glucides', 0),
                fibres=data.get('fibres', 0)
            )
            
            db.session.add(nouvel_aliment)
            db.session.commit()
            
            return nouvel_aliment.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            aliments_ns.abort(500, f"Erreur lors de la création: {str(e)}")

@aliments_ns.route('/<int:aliment_id>')
@aliments_ns.param('aliment_id', 'ID unique de l\'aliment')
class AlimentDetail(Resource):
    @aliments_ns.doc('obtenir_aliment')
    @aliments_ns.marshal_with(models['aliment'])
    def get(self, aliment_id):
        """🔍 Obtenir un aliment par son ID"""
        aliment = Aliment.query.get_or_404(aliment_id)
        return aliment.to_dict()
    
    @aliments_ns.doc('modifier_aliment')
    @aliments_ns.expect(models['aliment_input'], validate=True)
    @aliments_ns.marshal_with(models['aliment'])
    def put(self, aliment_id):
        """✏️ Modifier un aliment existant"""
        aliment = Aliment.query.get_or_404(aliment_id)
        data = request.get_json()
        
        try:
            for key, value in data.items():
                if hasattr(aliment, key) and key != 'id':
                    setattr(aliment, key, value)
            
            db.session.commit()
            return aliment.to_dict()
            
        except Exception as e:
            db.session.rollback()
            aliments_ns.abort(500, f"Erreur lors de la modification: {str(e)}")
    
    @aliments_ns.doc('supprimer_aliment')
    @aliments_ns.marshal_with(models['message'])
    def delete(self, aliment_id):
        """🗑️ Supprimer un aliment"""
        try:
            aliment = Aliment.query.get_or_404(aliment_id)
            nom_aliment = aliment.nom
            db.session.delete(aliment)
            db.session.commit()
            return {'message': f'Aliment "{nom_aliment}" supprimé avec succès', 'success': True}, 200
            
        except Exception as e:
            db.session.rollback()
            aliments_ns.abort(500, f"Erreur lors de la suppression: {str(e)}")

@aliments_ns.route('/recherche/<string:terme>')
@aliments_ns.param('terme', 'Terme de recherche')
class AlimentsRecherche(Resource):
    @aliments_ns.doc('rechercher_aliments')
    @aliments_ns.marshal_list_with(models['aliment'])
    def get(self, terme):
        """🔎 Rechercher des aliments par nom"""
        if not terme or len(terme) < 2:
            aliments_ns.abort(400, "Le terme de recherche doit contenir au moins 2 caractères")
        
        try:
            aliments = Aliment.query.filter(
                Aliment.nom.ilike(f'%{terme}%')
            ).all()
            return [aliment.to_dict() for aliment in aliments], 200
            
        except Exception as e:
            aliments_ns.abort(500, f"Erreur lors de la recherche: {str(e)}")

# ============= VOS ROUTES FLASK EXISTANTES (INCHANGÉES) =============

@aliments_bp.route('/aliments', methods=['GET'])
def get_aliments():
    """Route Flask existante - reste inchangée"""
    aliments = Aliment.query.all()
    return jsonify([aliment.to_dict() for aliment in aliments])

@aliments_bp.route('/aliments', methods=['POST'])
def create_aliment():
    """Route Flask existante - reste inchangée"""
    data = request.get_json()
    
    if not data or not data.get('nom'):
        return jsonify({'error': 'Le nom est requis'}), 400
    
    try:
        nouvel_aliment = Aliment(
            nom=data['nom'],
            calories=data.get('calories', 0),
            proteines=data.get('proteines', 0),
            lipides=data.get('lipides', 0),
            glucides=data.get('glucides', 0),
            fibres=data.get('fibres', 0)
        )
        
        db.session.add(nouvel_aliment)
        db.session.commit()
        
        return jsonify(nouvel_aliment.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@aliments_bp.route('/aliments/<int:aliment_id>', methods=['GET'])
def get_aliment(aliment_id):
    """Route Flask existante - reste inchangée"""
    aliment = Aliment.query.get_or_404(aliment_id)
    return jsonify(aliment.to_dict())

@aliments_bp.route('/aliments/<int:aliment_id>', methods=['PUT'])
def update_aliment(aliment_id):
    """Route Flask existante - reste inchangée"""
    aliment = Aliment.query.get_or_404(aliment_id)
    data = request.get_json()
    
    try:
        for key, value in data.items():
            if hasattr(aliment, key) and key != 'id':
                setattr(aliment, key, value)
        
        db.session.commit()
        return jsonify(aliment.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@aliments_bp.route('/aliments/<int:aliment_id>', methods=['DELETE'])
def delete_aliment(aliment_id):
    """Route Flask existante - reste inchangée"""
    try:
        aliment = Aliment.query.get_or_404(aliment_id)
        db.session.delete(aliment)
        db.session.commit()
        return jsonify({'message': 'Aliment supprimé avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500