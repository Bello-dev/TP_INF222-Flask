from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource
from werkzeug.security import generate_password_hash, check_password_hash
from app.db.db import db
from app.model import Utilisateur
from app.model import create_swagger_models

# Blueprint Flask existant
utilisateurs_bp = Blueprint('utilisateurs', __name__)

# Namespace Swagger (nouveau)
utilisateurs_ns = Namespace('utilisateurs', 
                           description='👤 Gestion des utilisateurs',
                           path='/utilisateurs')

# Créer les modèles Swagger
models = create_swagger_models(utilisateurs_ns)

# ============= ROUTES SWAGGER API (NOUVELLES) =============

@utilisateurs_ns.route('/')
class UtilisateursList(Resource):
    @utilisateurs_ns.doc('liste_utilisateurs')
    @utilisateurs_ns.marshal_list_with(models['utilisateur'])
    def get(self):
        """📋 Récupérer tous les utilisateurs"""
        try:
            utilisateurs = Utilisateur.query.all()
            return [utilisateur.to_dict() for utilisateur in utilisateurs], 200
        except Exception as e:
            utilisateurs_ns.abort(500, f"Erreur serveur: {str(e)}")
    
    @utilisateurs_ns.doc('creer_utilisateur')
    @utilisateurs_ns.expect(models['utilisateur_input'], validate=True)
    @utilisateurs_ns.marshal_with(models['utilisateur'], code=201)
    def post(self):
        """➕ Créer un nouvel utilisateur"""
        try:
            data = request.get_json()
            
            if not data or not data.get('email') or not data.get('mot_de_passe'):
                utilisateurs_ns.abort(400, "Email et mot de passe sont requis")
            
            if Utilisateur.query.filter_by(email=data['email']).first():
                utilisateurs_ns.abort(409, "Un utilisateur avec cet email existe déjà")
            
            nouvel_utilisateur = Utilisateur(
                nom=data.get('nom', ''),
                prenom=data.get('prenom', ''),
                email=data['email'],
                mot_de_passe=generate_password_hash(data['mot_de_passe']),
                age=data.get('age'),
                poids=data.get('poids'),
                taille=data.get('taille')
            )
            
            db.session.add(nouvel_utilisateur)
            db.session.commit()
            
            return nouvel_utilisateur.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            utilisateurs_ns.abort(500, f"Erreur lors de la création: {str(e)}")

@utilisateurs_ns.route('/<int:utilisateur_id>')
@utilisateurs_ns.param('utilisateur_id', 'ID unique de l\'utilisateur')
class UtilisateurDetail(Resource):
    @utilisateurs_ns.doc('obtenir_utilisateur')
    @utilisateurs_ns.marshal_with(models['utilisateur'])
    def get(self, utilisateur_id):
        """🔍 Obtenir un utilisateur par son ID"""
        utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
        return utilisateur.to_dict()
    
    @utilisateurs_ns.doc('modifier_utilisateur')
    @utilisateurs_ns.expect(models['utilisateur_input'])
    @utilisateurs_ns.marshal_with(models['utilisateur'])
    def put(self, utilisateur_id):
        """✏️ Modifier un utilisateur existant"""
        utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
        data = request.get_json()
        
        try:
            for key, value in data.items():
                if hasattr(utilisateur, key) and key not in ['id', 'created_at']:
                    if key == 'mot_de_passe':
                        setattr(utilisateur, key, generate_password_hash(value))
                    else:
                        setattr(utilisateur, key, value)
            
            db.session.commit()
            return utilisateur.to_dict()
            
        except Exception as e:
            db.session.rollback()
            utilisateurs_ns.abort(500, f"Erreur lors de la modification: {str(e)}")
    
    @utilisateurs_ns.doc('supprimer_utilisateur')
    @utilisateurs_ns.marshal_with(models['message'])
    def delete(self, utilisateur_id):
        """🗑️ Supprimer un utilisateur"""
        try:
            utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
            nom_complet = f"{utilisateur.prenom} {utilisateur.nom}"
            db.session.delete(utilisateur)
            db.session.commit()
            return {'message': f'Utilisateur "{nom_complet}" supprimé avec succès', 'success': True}, 200
            
        except Exception as e:
            db.session.rollback()
            utilisateurs_ns.abort(500, f"Erreur lors de la suppression: {str(e)}")

# ============= VOS ROUTES FLASK EXISTANTES (INCHANGÉES) =============

@utilisateurs_bp.route('/utilisateurs', methods=['GET'])
def get_utilisateurs():
    """Route Flask existante - reste inchangée"""
    utilisateurs = Utilisateur.query.all()
    return jsonify([utilisateur.to_dict() for utilisateur in utilisateurs])

@utilisateurs_bp.route('/utilisateurs', methods=['POST'])
def create_utilisateur():
    """Route Flask existante - reste inchangée"""
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'error': 'Email requis'}), 400
    
    try:
        nouvel_utilisateur = Utilisateur(
            nom=data.get('nom', ''),
            prenom=data.get('prenom', ''),
            email=data['email'],
            mot_de_passe=generate_password_hash(data.get('mot_de_passe', '')),
            age=data.get('age'),
            poids=data.get('poids'),
            taille=data.get('taille')
        )
        
        db.session.add(nouvel_utilisateur)
        db.session.commit()
        
        return jsonify(nouvel_utilisateur.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@utilisateurs_bp.route('/utilisateurs/<int:utilisateur_id>', methods=['GET'])
def get_utilisateur(utilisateur_id):
    """Route Flask existante - reste inchangée"""
    utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
    return jsonify(utilisateur.to_dict())

@utilisateurs_bp.route('/utilisateurs/<int:utilisateur_id>', methods=['PUT'])
def update_utilisateur(utilisateur_id):
    """Route Flask existante - reste inchangée"""
    utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
    data = request.get_json()
    
    try:
        for key, value in data.items():
            if hasattr(utilisateur, key) and key not in ['id', 'created_at']:
                if key == 'mot_de_passe':
                    setattr(utilisateur, key, generate_password_hash(value))
                else:
                    setattr(utilisateur, key, value)
        
        db.session.commit()
        return jsonify(utilisateur.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@utilisateurs_bp.route('/utilisateurs/<int:utilisateur_id>', methods=['DELETE'])
def delete_utilisateur(utilisateur_id):
    """Route Flask existante - reste inchangée"""
    try:
        utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
        db.session.delete(utilisateur)
        db.session.commit()
        return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500