from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource
from app.db.db import db
from app.model import Recommandation
from app.model import Utilisateur
from app.model import Recette
from app.model import create_swagger_models

# Blueprint Flask classique
recommandations_bp = Blueprint('recommandations', __name__)

# Namespace Swagger
recommandations_ns = Namespace('recommandations', 
                              description='💡 Système de recommandations personnalisées',
                              path='/recommandations')

# Créer les modèles Swagger
models = create_swagger_models(recommandations_ns)

@recommandations_ns.route('/')
class RecommandationsList(Resource):
    @recommandations_ns.doc('liste_recommandations',
                           responses={
                               200: 'Liste des recommandations récupérée avec succès',
                               500: 'Erreur serveur'
                           })
    @recommandations_ns.marshal_list_with(models['recommandation'])
    def get(self):
        """📋 Récupérer toutes les recommandations
        
        Retourne la liste de toutes les recommandations du système.
        """
        try:
            recommandations = Recommandation.query.all()
            return [recommandation.to_dict() for recommandation in recommandations], 200
        except Exception as e:
            recommandations_ns.abort(500, f"Erreur serveur: {str(e)}")
    
    @recommandations_ns.doc('creer_recommandation',
                           responses={
                               201: 'Recommandation créée avec succès',
                               400: 'Données invalides',
                               404: 'Utilisateur ou recette non trouvé',
                               500: 'Erreur serveur'
                           })
    @recommandations_ns.expect(models['recommandation_input'], validate=True)
    @recommandations_ns.marshal_with(models['recommandation'], code=201)
    def post(self):
        """➕ Créer une nouvelle recommandation
        
        Crée une recommandation personnalisée pour un utilisateur.
        """
        try:
            data = request.get_json()
            
            # Validations
            if not data or not data.get('utilisateur_id') or not data.get('recette_id'):
                recommandations_ns.abort(400, "ID utilisateur et ID recette sont requis")
            
            # Vérifier que l'utilisateur existe
            utilisateur = Utilisateur.query.get(data['utilisateur_id'])
            if not utilisateur:
                recommandations_ns.abort(404, "Utilisateur non trouvé")
            
            # Vérifier que la recette existe
            recette = Recette.query.get(data['recette_id'])
            if not recette:
                recommandations_ns.abort(404, "Recette non trouvée")
            
            nouvelle_recommandation = Recommandation(
                utilisateur_id=data['utilisateur_id'],
                recette_id=data['recette_id'],
                score=data.get('score', 5.0),
                raison=data.get('raison', 'Recommandation automatique')
            )
            
            db.session.add(nouvelle_recommandation)
            db.session.commit()
            
            return nouvelle_recommandation.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            recommandations_ns.abort(500, f"Erreur lors de la création: {str(e)}")

@recommandations_ns.route('/<int:recommandation_id>')
@recommandations_ns.param('recommandation_id', 'ID unique de la recommandation')
class RecommandationDetail(Resource):
    @recommandations_ns.doc('obtenir_recommandation',
                           responses={
                               200: 'Recommandation trouvée',
                               404: 'Recommandation non trouvée'
                           })
    @recommandations_ns.marshal_with(models['recommandation'])
    def get(self, recommandation_id):
        """🔍 Obtenir une recommandation par son ID
        
        Récupère les détails d'une recommandation spécifique.
        """
        recommandation = Recommandation.query.get_or_404(recommandation_id)
        return recommandation.to_dict()
    
    @recommandations_ns.doc('supprimer_recommandation',
                           responses={
                               200: 'Recommandation supprimée avec succès',
                               404: 'Recommandation non trouvée',
                               500: 'Erreur serveur'
                           })
    @recommandations_ns.marshal_with(models['message'])
    def delete(self, recommandation_id):
        """🗑️ Supprimer une recommandation
        
        Supprime définitivement une recommandation.
        """
        try:
            recommandation = Recommandation.query.get_or_404(recommandation_id)
            db.session.delete(recommandation)
            db.session.commit()
            return {'message': 'Recommandation supprimée avec succès', 'success': True}, 200
            
        except Exception as e:
            db.session.rollback()
            recommandations_ns.abort(500, f"Erreur lors de la suppression: {str(e)}")

@recommandations_ns.route('/utilisateur/<int:utilisateur_id>')
@recommandations_ns.param('utilisateur_id', 'ID de l\'utilisateur')
class RecommandationsByUser(Resource):
    @recommandations_ns.doc('recommandations_utilisateur',
                           responses={
                               200: 'Recommandations pour l\'utilisateur',
                               404: 'Utilisateur non trouvé'
                           })
    @recommandations_ns.marshal_list_with(models['recommandation'])
    def get(self, utilisateur_id):
        """👤 Obtenir les recommandations d'un utilisateur
        
        Retourne toutes les recommandations personnalisées pour un utilisateur.
        """
        try:
            # Vérifier que l'utilisateur existe
            utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
            
            recommandations = Recommandation.query.filter_by(utilisateur_id=utilisateur_id).all()
            return [recommandation.to_dict() for recommandation in recommandations], 200
            
        except Exception as e:
            recommandations_ns.abort(500, f"Erreur lors de la récupération: {str(e)}")

@recommandations_ns.route('/top/<int:limite>')
@recommandations_ns.param('limite', 'Nombre de recommandations à retourner')
class TopRecommandations(Resource):
    @recommandations_ns.doc('top_recommandations',
                           responses={
                               200: 'Top des recommandations',
                               400: 'Limite invalide'
                           })
    @recommandations_ns.marshal_list_with(models['recommandation'])
    def get(self, limite):
        """🏆 Top des meilleures recommandations
        
        Retourne les meilleures recommandations triées par score.
        """
        if limite <= 0 or limite > 100:
            recommandations_ns.abort(400, "La limite doit être entre 1 et 100")
        
        try:
            recommandations = Recommandation.query.order_by(
                Recommandation.score.desc()
            ).limit(limite).all()
            
            return [recommandation.to_dict() for recommandation in recommandations], 200
            
        except Exception as e:
            recommandations_ns.abort(500, f"Erreur lors de la récupération: {str(e)}")

# Route Flask classique
@recommandations_bp.route('/recommandations', methods=['GET'])
def get_recommandations_classic():
    """Route Flask classique"""
    return jsonify({
        'message': 'Utilisez l\'API Swagger pour une meilleure expérience',
        'swagger_url': '/swagger-ui/',
        'api_endpoint': '/api/recommandations/'
    })