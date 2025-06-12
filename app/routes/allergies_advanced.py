from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from sqlalchemy import func, and_, or_
from app.model import (db, ReactionAllergique, AllergieUtilisateur, 
                      Utilisateur, Aliment, Recette, Allergie)
from app.model import create_swagger_models
from datetime import datetime, timedelta

# Blueprint Flask pour les routes classiques
allergies_bp = Blueprint('allergies_advanced', __name__)

# Namespace Swagger pour l'API avancée
allergies_ns = Namespace(
    "allergies", 
    description="🦠 **Système Avancé de Gestion des Allergies** avec Intelligence Artificielle",
    path='/allergies'
)

# ============= ROUTES API SWAGGER AVANCÉES =============

@allergies_ns.route('/users/<int:user_id>/profile')
@allergies_ns.param('user_id', 'ID unique de l\'utilisateur')
class UserAllergyProfile(Resource):
    @allergies_ns.doc('get_user_allergy_profile')
    def get(self, user_id):
        """🩺 **Profil Allergique Complet** - Analyse détaillée des allergies d'un utilisateur"""
        try:
            user = Utilisateur.query.get_or_404(user_id)
            
            # Récupérer toutes les réactions de l'utilisateur
            reactions = ReactionAllergique.query.filter_by(utilisateur_id=user_id).all()
            
            # Allergies confirmées (détectées automatiquement ou ajoutées manuellement)
            allergies_confirmees = db.session.query(
                AllergieUtilisateur, Allergie
            ).join(Allergie).filter(
                AllergieUtilisateur.utilisateur_id == user_id
            ).all()
            
            # Analyse des risques par aliment
            risques_aliments = []
            for reaction in reactions:
                if reaction.aliment_id:
                    aliment = Aliment.query.get(reaction.aliment_id)
                    probabilite = reaction.probabilite_allergie()
                    niveau_risque = self._get_risk_level(probabilite)
                    
                    risques_aliments.append({
                        'aliment': aliment.to_dict() if aliment else None,
                        'times_eaten': reaction.times_eaten,
                        'times_reacted': reaction.times_reacted,
                        'probabilite_allergie': round(probabilite, 2),
                        'niveau_risque': niveau_risque,
                        'is_allergic': reaction.is_allergic(),
                        'derniere_reaction': reaction.updated_at.isoformat()
                    })
            
            # Statistiques globales
            total_aliments_testes = len(reactions)
            allergies_detectees = len([r for r in reactions if r.is_allergic()])
            pourcentage_allergies = (allergies_detectees / total_aliments_testes * 100) if total_aliments_testes > 0 else 0
            
            # Recommandations personnalisées
            recommandations = self._generate_recommendations(user_id, reactions, allergies_confirmees)
            
            profile = {
                'utilisateur': {
                    'id': user.id,
                    'nom_complet': f"{user.prenom} {user.nom}",
                    'email': user.email
                },
                'resume_allergique': {
                    'total_aliments_testes': total_aliments_testes,
                    'allergies_detectees': allergies_detectees,
                    'pourcentage_allergies': round(pourcentage_allergies, 2),
                    'niveau_risque_global': self._get_global_risk_level(pourcentage_allergies)
                },
                'allergies_confirmees': [
                    {
                        'allergie': allergie_util[1].to_dict(),
                        'gravite_personnelle': allergie_util[0].gravite_personnelle,
                        'detectee_automatiquement': allergie_util[0].detectee_automatiquement,
                        'date_detection': allergie_util[0].created_at.isoformat()
                    }
                    for allergie_util in allergies_confirmees
                ],
                'analyse_risques_aliments': sorted(risques_aliments, 
                                                 key=lambda x: x['probabilite_allergie'], 
                                                 reverse=True),
                'recommandations': recommandations,
                'derniere_analyse': datetime.utcnow().isoformat()
            }
            
            return profile, 200
            
        except Exception as e:
            return {'message': f'Erreur lors de l\'analyse: {str(e)}'}, 500
    
    def _get_risk_level(self, probabilite):
        """Détermine le niveau de risque basé sur la probabilité"""
        if probabilite >= 50:
            return 'TRÈS ÉLEVÉ'
        elif probabilite >= 30:
            return 'ÉLEVÉ'
        elif probabilite >= 15:
            return 'MODÉRÉ'
        elif probabilite > 0:
            return 'FAIBLE'
        else:
            return 'AUCUN'
    
    def _get_global_risk_level(self, pourcentage):
        """Détermine le niveau de risque global de l'utilisateur"""
        if pourcentage >= 25:
            return 'PROFIL À HAUT RISQUE'
        elif pourcentage >= 10:
            return 'PROFIL MODÉRÉ'
        else:
            return 'PROFIL FAIBLE RISQUE'
    
    def _generate_recommendations(self, user_id, reactions, allergies_confirmees):
        """Génère des recommandations personnalisées"""
        recommendations = []
        
        # Recommandations basées sur les réactions à risque
        high_risk_reactions = [r for r in reactions if r.probabilite_allergie() >= 15]
        
        if high_risk_reactions:
            recommendations.append({
                'type': 'ÉVITEMENT',
                'priorite': 'HAUTE',
                'message': f'Évitez les {len(high_risk_reactions)} aliment(s) à risque identifié(s)',
                'details': [r.aliment_id for r in high_risk_reactions if r.aliment_id]
            })
        
        # Recommandation de consultation médicale
        severe_allergies = len([a for a in allergies_confirmees if a[0].gravite_personnelle == 'Sévère'])
        if severe_allergies > 0:
            recommendations.append({
                'type': 'MÉDICAL',
                'priorite': 'CRITIQUE',
                'message': 'Consultez un allergologue pour vos allergies sévères',
                'details': f'{severe_allergies} allergie(s) sévère(s) détectée(s)'
            })
        
        # Recommandation de test supplémentaire
        untested_period = len([r for r in reactions if r.updated_at < datetime.utcnow() - timedelta(days=90)])
        if untested_period > 2:
            recommendations.append({
                'type': 'SUIVI',
                'priorite': 'MOYENNE',
                'message': 'Réévaluez vos réactions allergiques anciennes',
                'details': f'{untested_period} réaction(s) datant de plus de 3 mois'
            })
        
        return recommendations


@allergies_ns.route('/users/<int:user_id>/reactions')
@allergies_ns.param('user_id', 'ID unique de l\'utilisateur')
class UserReactionsList(Resource):
    @allergies_ns.doc('add_reaction')
    def post(self, user_id):
        """📝 **Enregistrer une Réaction** - Ajouter une nouvelle réaction allergique"""
        try:
            data = request.get_json()
            
            # Validation des données
            if not data.get('aliment_id') and not data.get('recette_id'):
                return {'message': 'Vous devez spécifier soit aliment_id soit recette_id'}, 400
            
            if data.get('aliment_id') and data.get('recette_id'):
                return {'message': 'Vous ne pouvez pas spécifier aliment_id ET recette_id'}, 400
            
            times_eaten = data.get('times_eaten', 1)
            times_reacted = data.get('times_reacted', 0)
            
            if times_reacted > times_eaten:
                return {'message': 'Le nombre de réactions ne peut pas dépasser le nombre de consommations'}, 400
            
            # Vérifier si l'utilisateur existe
            user = Utilisateur.query.get_or_404(user_id)
            
            # Chercher une réaction existante
            filter_kwargs = {'utilisateur_id': user_id}
            if data.get('aliment_id'):
                filter_kwargs['aliment_id'] = data['aliment_id']
            else:
                filter_kwargs['recette_id'] = data['recette_id']
            
            reaction = ReactionAllergique.query.filter_by(**filter_kwargs).first()
            
            if reaction:
                # Mettre à jour la réaction existante
                reaction.times_eaten = times_eaten
                reaction.times_reacted = times_reacted
                reaction.updated_at = datetime.utcnow()
                action = 'updated'
            else:
                # Créer une nouvelle réaction
                reaction = ReactionAllergique(
                    utilisateur_id=user_id,
                    aliment_id=data.get('aliment_id'),
                    recette_id=data.get('recette_id'),
                    times_eaten=times_eaten,
                    times_reacted=times_reacted
                )
                db.session.add(reaction)
                action = 'created'
            
            db.session.commit()
            
            # Vérifier si cela déclenche une détection d'allergie automatique
            allergie_detectee = self._check_auto_allergy_detection(reaction)
            
            response = {
                'reaction': reaction.to_dict(),
                'action': action,
                'allergie_detectee_automatiquement': allergie_detectee is not None,
                'message': f'Réaction {action} avec succès'
            }
            
            if allergie_detectee:
                response['nouvelle_allergie'] = allergie_detectee
                response['message'] += f'. ⚠️ ALLERGIE DÉTECTÉE automatiquement: {allergie_detectee["nom"]}'
            
            return response, 201 if action == 'created' else 200
            
        except Exception as e:
            db.session.rollback()
            return {'message': f'Erreur lors de l\'enregistrement: {str(e)}'}, 500
    
    def _check_auto_allergy_detection(self, reaction):
        """Vérifie si une allergie doit être détectée automatiquement"""
        if not reaction.is_allergic():
            return None
        
        # Si c'est un aliment, chercher/créer l'allergie correspondante
        if reaction.aliment_id:
            aliment = Aliment.query.get(reaction.aliment_id)
            if not aliment:
                return None
            
            # Chercher une allergie existante pour cet aliment
            allergie = Allergie.query.filter_by(nom=aliment.nom).first()
            
            if not allergie:
                # Créer une nouvelle allergie
                allergie = Allergie(
                    nom=aliment.nom,
                    description=f'Allergie détectée automatiquement pour {aliment.nom}',
                    gravite='Modéré'
                )
                db.session.add(allergie)
                db.session.commit()
            
            # Vérifier si l'utilisateur a déjà cette allergie
            allergie_user = AllergieUtilisateur.query.filter_by(
                utilisateur_id=reaction.utilisateur_id,
                allergie_id=allergie.id
            ).first()
            
            if not allergie_user:
                # Ajouter l'allergie à l'utilisateur
                allergie_user = AllergieUtilisateur(
                    utilisateur_id=reaction.utilisateur_id,
                    allergie_id=allergie.id,
                    gravite_personnelle='Modéré',
                    detectee_automatiquement=True
                )
                db.session.add(allergie_user)
                db.session.commit()
                
                return allergie.to_dict()
        
        return None


@allergies_ns.route('/users/<int:user_id>/allergies')
@allergies_ns.param('user_id', 'ID unique de l\'utilisateur')
class UserAllergiesList(Resource):
    @allergies_ns.doc('get_user_allergies')
    def get(self, user_id):
        """🔍 **Liste des Allergies** - Toutes les allergies confirmées de l'utilisateur"""
        try:
            user = Utilisateur.query.get_or_404(user_id)
            
            allergies = db.session.query(
                AllergieUtilisateur, Allergie
            ).join(Allergie).filter(
                AllergieUtilisateur.utilisateur_id == user_id
            ).all()
            
            result = []
            for allergie_user, allergie in allergies:
                allergie_data = allergie.to_dict()
                allergie_data.update({
                    'gravite_personnelle': allergie_user.gravite_personnelle,
                    'detectee_automatiquement': allergie_user.detectee_automatiquement,
                    'date_detection': allergie_user.created_at.isoformat()
                })
                result.append(allergie_data)
            
            return {
                'utilisateur': user.to_dict(),
                'total_allergies': len(result),
                'allergies_auto_detectees': len([a for a in result if a['detectee_automatiquement']]),
                'allergies': result
            }, 200
            
        except Exception as e:
            return {'message': f'Erreur lors de la récupération: {str(e)}'}, 500


@allergies_ns.route('/check/<int:user_id>/<int:aliment_id>')
@allergies_ns.param('user_id', 'ID de l\'utilisateur')
@allergies_ns.param('aliment_id', 'ID de l\'aliment à vérifier')
class AllergyCheck(Resource):
    @allergies_ns.doc('check_allergy_risk')
    def get(self, user_id, aliment_id):
        """🚨 **Vérification de Risque** - Analyse instantanée du risque allergique"""
        try:
            user = Utilisateur.query.get_or_404(user_id)
            aliment = Aliment.query.get_or_404(aliment_id)
            
            # Chercher les réactions existantes
            reaction = ReactionAllergique.query.filter_by(
                utilisateur_id=user_id,
                aliment_id=aliment_id
            ).first()
            
            # Chercher les allergies confirmées
            allergie = Allergie.query.filter_by(nom=aliment.nom).first()
            allergie_confirmee = None
            
            if allergie:
                allergie_confirmee = AllergieUtilisateur.query.filter_by(
                    utilisateur_id=user_id,
                    allergie_id=allergie.id
                ).first()
            
            # Analyse du risque
            if allergie_confirmee:
                niveau_risque = 'ALLERGIE CONFIRMÉE'
                recommandation = 'ÉVITEMENT TOTAL RECOMMANDÉ'
                probabilite = 100.0
            elif reaction and reaction.is_allergic():
                niveau_risque = 'TRÈS ÉLEVÉ'
                recommandation = 'ÉVITEMENT FORTEMENT RECOMMANDÉ'
                probabilite = reaction.probabilite_allergie()
            elif reaction:
                probabilite = reaction.probabilite_allergie()
                if probabilite >= 15:
                    niveau_risque = 'MODÉRÉ'
                    recommandation = 'CONSOMMATION AVEC PRUDENCE'
                elif probabilite > 0:
                    niveau_risque = 'FAIBLE'
                    recommandation = 'SURVEILLANCE RECOMMANDÉE'
                else:
                    niveau_risque = 'AUCUN RISQUE CONNU'
                    recommandation = 'CONSOMMATION NORMALE'
            else:
                niveau_risque = 'INCONNU'
                recommandation = 'PREMIER TEST - CONSOMMATION PRUDENTE'
                probabilite = 0.0
            
            return {
                'utilisateur': {
                    'id': user.id,
                    'nom_complet': f"{user.prenom} {user.nom}"
                },
                'aliment': aliment.to_dict(),
                'analyse_risque': {
                    'niveau_risque': niveau_risque,
                    'probabilite_allergie': round(probabilite, 2),
                    'recommandation': recommandation,
                    'allergie_confirmee': allergie_confirmee is not None,
                    'historique_reactions': reaction.to_dict() if reaction else None
                },
                'timestamp': datetime.utcnow().isoformat()
            }, 200
            
        except Exception as e:
            return {'message': f'Erreur lors de la vérification: {str(e)}'}, 500


@allergies_ns.route('/statistics')
class AllergyStatistics(Resource):
    @allergies_ns.doc('get_allergy_statistics')
    def get(self):
        """📊 **Statistiques Globales** - Analyse des tendances allergiques"""
        try:
            # Statistiques générales
            total_users = Utilisateur.query.count()
            total_reactions = ReactionAllergique.query.count()
            total_allergies = AllergieUtilisateur.query.count()
            
            # Allergies les plus fréquentes
            allergies_frequentes = db.session.query(
                Allergie.nom,
                func.count(AllergieUtilisateur.id).label('count')
            ).join(AllergieUtilisateur).group_by(
                Allergie.nom
            ).order_by(
                func.count(AllergieUtilisateur.id).desc()
            ).limit(10).all()
            
            # Aliments les plus problématiques
            aliments_problematiques = db.session.query(
                Aliment.nom,
                func.avg(ReactionAllergique.times_reacted * 100.0 / ReactionAllergique.times_eaten).label('avg_reaction_rate')
            ).join(ReactionAllergique).filter(
                ReactionAllergique.times_eaten > 0
            ).group_by(
                Aliment.nom
            ).order_by(
                func.avg(ReactionAllergique.times_reacted * 100.0 / ReactionAllergique.times_eaten).desc()
            ).limit(10).all()
            
            # Détections automatiques récentes
            detections_auto = AllergieUtilisateur.query.filter_by(
                detectee_automatiquement=True
            ).filter(
                AllergieUtilisateur.created_at >= datetime.utcnow() - timedelta(days=30)
            ).count()
            
            return {
                'resume_global': {
                    'total_utilisateurs': total_users,
                    'total_reactions_enregistrees': total_reactions,
                    'total_allergies_confirmees': total_allergies,
                    'detections_automatiques_30j': detections_auto,
                    'taux_detection_auto': round((detections_auto / total_allergies * 100) if total_allergies > 0 else 0, 2)
                },
                'allergies_plus_frequentes': [
                    {'allergie': nom, 'nombre_cas': count}
                    for nom, count in allergies_frequentes
                ],
                'aliments_plus_problematiques': [
                    {'aliment': nom, 'taux_reaction_moyen': round(float(taux), 2)}
                    for nom, taux in aliments_problematiques
                ],
                'timestamp': datetime.utcnow().isoformat()
            }, 200
            
        except Exception as e:
            return {'message': f'Erreur lors du calcul des statistiques: {str(e)}'}, 500


# ============= ROUTES FLASK CLASSIQUES =============

@allergies_bp.route('/allergies/check/<int:user_id>/<int:aliment_id>')
def check_allergy_simple(user_id, aliment_id):
    """Route Flask simple pour vérification d'allergie"""
    try:
        reaction = ReactionAllergique.query.filter_by(
            utilisateur_id=user_id,
            aliment_id=aliment_id
        ).first()
        
        if reaction:
            return jsonify({
                'is_allergic': reaction.is_allergic(),
                'probabilite': reaction.probabilite_allergie(),
                'times_eaten': reaction.times_eaten,
                'times_reacted': reaction.times_reacted
            })
        else:
            return jsonify({
                'is_allergic': False,
                'probabilite': 0.0,
                'message': 'Aucune donnée disponible pour cet aliment'
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
