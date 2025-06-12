from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from app.model import db, ReactionAllergique, AllergieUtilisateur, Utilisateur, Aliment, Recette, Allergie
from app.model import create_swagger_models

# Blueprint Flask pour les routes classiques
allergie_reaction_bp = Blueprint('allergie_reaction', __name__)

# Namespace Swagger pour l'API
allergie_reaction_ns = Namespace("allergie-reactions", description="🦠 Gestion avancée des allergies avec détection automatique par IA")

# ============= ROUTES FLASK SIMPLES POUR TEST =============

@allergie_reaction_bp.route('/test-allergies')
def test_allergies():
    """Route de test pour vérifier que le système d'allergies fonctionne"""
    try:
        total_users = Utilisateur.query.count()
        total_reactions = ReactionAllergique.query.count()
        
        return jsonify({
            'message': '🦠 Système d\'allergies fonctionnel!',
            'statistiques': {
                'utilisateurs': total_users,
                'reactions': total_reactions
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@allergie_reaction_bp.route('/user/<int:user_id>/allergies')
def get_user_allergies_simple(user_id):
    """Obtenir les allergies d'un utilisateur (version simple)"""
    try:
        user = Utilisateur.query.get_or_404(user_id)
        reactions = ReactionAllergique.query.filter_by(utilisateur_id=user_id).all()
        
        allergies_detectees = []
        for reaction in reactions:
            if reaction.is_allergic():
                aliment = Aliment.query.get(reaction.aliment_id) if reaction.aliment_id else None
                allergies_detectees.append({
                    'aliment': aliment.nom if aliment else 'Inconnu',
                    'probabilite': round(reaction.probabilite_allergie(), 2),
                    'times_eaten': reaction.times_eaten,
                    'times_reacted': reaction.times_reacted
                })
        
        return jsonify({
            'utilisateur': f"{user.prenom} {user.nom}",
            'total_allergies_detectees': len(allergies_detectees),
            'allergies': allergies_detectees
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@allergie_reaction_bp.route('/add-reaction', methods=['POST'])
def add_reaction_simple():
    """Ajouter une réaction allergique (version simple)"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id')
        aliment_id = data.get('aliment_id')
        times_eaten = data.get('times_eaten', 1)
        times_reacted = data.get('times_reacted', 0)
        
        if not user_id or not aliment_id:
            return jsonify({'error': 'user_id et aliment_id requis'}), 400
        
        # Vérifier si la réaction existe déjà
        reaction = ReactionAllergique.query.filter_by(
            utilisateur_id=user_id,
            aliment_id=aliment_id
        ).first()
        
        if reaction:
            # Mettre à jour
            reaction.times_eaten = times_eaten
            reaction.times_reacted = times_reacted
            action = 'mise à jour'
        else:
            # Créer nouvelle réaction
            reaction = ReactionAllergique(
                utilisateur_id=user_id,
                aliment_id=aliment_id,
                times_eaten=times_eaten,
                times_reacted=times_reacted
            )
            db.session.add(reaction)
            action = 'création'
        
        db.session.commit()
        
        # Vérifier si cela déclenche une allergie
        is_allergic = reaction.is_allergic()
        probabilite = reaction.probabilite_allergie()
        
        response = {
            'message': f'Réaction {action} avec succès',
            'reaction': {
                'times_eaten': reaction.times_eaten,
                'times_reacted': reaction.times_reacted,
                'probabilite_allergie': round(probabilite, 2),
                'is_allergic': is_allergic
            }
        }
        
        if is_allergic:
            response['alerte'] = f'🚨 ALLERGIE DÉTECTÉE! Probabilité: {round(probabilite, 2)}%'
        
        return jsonify(response), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============= ROUTES SWAGGER API AVANCÉES =============

@allergie_reaction_ns.route('/profile/<int:user_id>')
@allergie_reaction_ns.param('user_id', 'ID unique de l\'utilisateur')
class UserAllergyProfile(Resource):
    @allergie_reaction_ns.doc('get_user_allergy_profile')
    def get(self, user_id):
        """🩺 **Profil Allergique Complet** - Analyse détaillée des allergies d'un utilisateur"""
        try:
            user = Utilisateur.query.get_or_404(user_id)
            
            # Récupérer toutes les réactions de l'utilisateur
            reactions = ReactionAllergique.query.filter_by(utilisateur_id=user_id).all()
            
            # Allergies confirmées
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
                    
                    risques_aliments.append({
                        'aliment': aliment.to_dict() if aliment else None,
                        'times_eaten': reaction.times_eaten,
                        'times_reacted': reaction.times_reacted,
                        'probabilite_allergie': round(probabilite, 2),
                        'is_allergic': reaction.is_allergic(),
                    })
            
            # Statistiques globales
            total_aliments_testes = len(reactions)
            allergies_detectees = len([r for r in reactions if r.is_allergic()])
            pourcentage_allergies = (allergies_detectees / total_aliments_testes * 100) if total_aliments_testes > 0 else 0
            
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
                },
                'allergies_confirmees': [
                    {
                        'allergie': allergie_util[1].to_dict(),
                        'gravite_personnelle': allergie_util[0].gravite_personnelle,
                        'detectee_automatiquement': allergie_util[0].detectee_automatiquement,
                    }
                    for allergie_util in allergies_confirmees
                ],
                'analyse_risques_aliments': sorted(risques_aliments, 
                                                 key=lambda x: x['probabilite_allergie'], 
                                                 reverse=True),
            }
            
            return profile, 200
            
        except Exception as e:
            return {'message': f'Erreur lors de l\'analyse: {str(e)}'}, 500


@allergie_reaction_ns.route('/statistics')
class AllergyStatistics(Resource):
    @allergie_reaction_ns.doc('get_allergy_statistics')
    def get(self):
        """📊 **Statistiques Globales** - Analyse des tendances allergiques"""
        try:
            # Statistiques générales
            from sqlalchemy import func
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
            
            return {
                'resume_global': {
                    'total_utilisateurs': total_users,
                    'total_reactions_enregistrees': total_reactions,
                    'total_allergies_confirmees': total_allergies,
                },
                'allergies_plus_frequentes': [
                    {'allergie': nom, 'nombre_cas': count}
                    for nom, count in allergies_frequentes
                ],
            }, 200
            
        except Exception as e:
            return {'message': f'Erreur lors du calcul des statistiques: {str(e)}'}, 500
    """Enregistrer les routes de réactions allergiques"""
    models = create_swagger_models(api)
    
    @allergie_reaction_ns.route('/reaction')
    class AllergieReactionList(Resource):
        @allergie_reaction_ns.expect(models['reaction_allergique_input'], validate=True)
        @allergie_reaction_ns.marshal_with(models['reaction_allergique'])
        def post(self):
            """
            Enregistrer ou modifier le nombre de fois qu'un utilisateur a consommé
            un aliment/recette et le nombre de réactions allergiques observées.
            Détecte automatiquement les allergies si probabilité > 30%.
            """
            data = request.get_json()
            utilisateur_id = data['utilisateur_id']
            aliment_id = data.get('aliment_id')
            recette_id = data.get('recette_id')
            times_eaten = data['times_eaten']
            times_reacted = data['times_reacted']

            # Validation
            if not aliment_id and not recette_id:
                return {'message': 'Vous devez spécifier soit aliment_id soit recette_id'}, 400
            
            if aliment_id and recette_id:
                return {'message': 'Vous ne pouvez pas spécifier aliment_id ET recette_id en même temps'}, 400

            # Vérifier si l'utilisateur existe
            user = Utilisateur.query.get(utilisateur_id)
            if not user:
                return {'message': 'Utilisateur non trouvé'}, 404

            # Vérifier si l'enregistrement existe déjà
            if aliment_id:
                reaction = ReactionAllergique.query.filter_by(
                    utilisateur_id=utilisateur_id, 
                    aliment_id=aliment_id
                ).first()
            else:
                reaction = ReactionAllergique.query.filter_by(
                    utilisateur_id=utilisateur_id, 
                    recette_id=recette_id
                ).first()

            if not reaction:
                # Créer l'enregistrement
                reaction = ReactionAllergique(
                    utilisateur_id=utilisateur_id,
                    aliment_id=aliment_id,
                    recette_id=recette_id,
                    times_eaten=times_eaten,
                    times_reacted=times_reacted
                )
                db.session.add(reaction)
            else:
                # Mettre à jour
                reaction.times_eaten = times_eaten
                reaction.times_reacted = times_reacted

            try:
                db.session.commit()
                
                # Vérifier si l'utilisateur est allergique (probabilité > 30%)
                if reaction.is_allergic():
                    self._ajouter_allergie_automatique(reaction)
                
                return reaction.to_dict(), 200
                
            except Exception as e:
                db.session.rollback()
                return {'message': f'Erreur : {str(e)}'}, 500

        def _ajouter_allergie_automatique(self, reaction):
            """
            Ajouter automatiquement une allergie à l'utilisateur si la probabilité > 30%
            """
            try:
                # Déterminer le nom de l'allergie
                nom_allergie = None
                if reaction.aliment_id:
                    aliment = Aliment.query.get(reaction.aliment_id)
                    nom_allergie = f"Allergie à {aliment.nom}" if aliment else "Allergie inconnue"
                elif reaction.recette_id:
                    recette = Recette.query.get(reaction.recette_id)
                    nom_allergie = f"Allergie à {recette.nom}" if recette else "Allergie inconnue"
                
                if not nom_allergie:
                    return

                # Créer ou récupérer l'allergie
                allergie = Allergie.query.filter_by(nom=nom_allergie).first()
                if not allergie:
                    allergie = Allergie(
                        nom=nom_allergie,
                        description=f"Allergie détectée automatiquement (probabilité: {reaction.probabilite_allergie():.1f}%)",
                        gravite='Modéré'
                    )
                    db.session.add(allergie)
                    db.session.flush()  # Pour obtenir l'ID

                # Vérifier si l'utilisateur a déjà cette allergie
                allergie_utilisateur = AllergieUtilisateur.query.filter_by(
                    utilisateur_id=reaction.utilisateur_id,
                    allergie_id=allergie.id
                ).first()

                if not allergie_utilisateur:
                    # Ajouter l'allergie à l'utilisateur
                    allergie_utilisateur = AllergieUtilisateur(
                        utilisateur_id=reaction.utilisateur_id,
                        allergie_id=allergie.id,
                        gravite_personnelle='Modéré',
                        detectee_automatiquement=True
                    )
                    db.session.add(allergie_utilisateur)
                    db.session.commit()
                    
                    print(f"✅ Allergie automatiquement ajoutée: {nom_allergie} pour l'utilisateur {reaction.utilisateur_id}")
                
            except Exception as e:
                print(f"❌ Erreur lors de l'ajout automatique d'allergie: {e}")
                db.session.rollback()

    @allergie_reaction_ns.route('/check/<int:utilisateur_id>/<int:aliment_id>')
    class AllergieReactionCheckAliment(Resource):
        def get(self, utilisateur_id, aliment_id):
            """
            Vérifier si l'utilisateur est allergique à un aliment spécifique
            (probabilité > 30%).
            """
            reaction = ReactionAllergique.query.filter_by(
                utilisateur_id=utilisateur_id, 
                aliment_id=aliment_id
            ).first()
            
            if not reaction:
                return {
                    'message': 'Aucun historique de réactions pour cet aliment',
                    'is_allergic': False,
                    'probabilite_allergie': 0,
                    'aliment_id': aliment_id,
                    'utilisateur_id': utilisateur_id
                }, 200
            
            return {
                'is_allergic': reaction.is_allergic(),
                'probabilite_allergie': reaction.probabilite_allergie(),
                'reaction': reaction.to_dict(),
                'message': f'Probabilité d\'allergie: {reaction.probabilite_allergie():.1f}%'
            }, 200

    @allergie_reaction_ns.route('/check-recette/<int:utilisateur_id>/<int:recette_id>')
    class AllergieReactionCheckRecette(Resource):
        def get(self, utilisateur_id, recette_id):
            """
            Vérifier si l'utilisateur est allergique à une recette spécifique
            (probabilité > 30%).
            """
            reaction = ReactionAllergique.query.filter_by(
                utilisateur_id=utilisateur_id, 
                recette_id=recette_id
            ).first()
            
            if not reaction:
                return {
                    'message': 'Aucun historique de réactions pour cette recette',
                    'is_allergic': False,
                    'probabilite_allergie': 0,
                    'recette_id': recette_id,
                    'utilisateur_id': utilisateur_id
                }, 200
            
            return {
                'is_allergic': reaction.is_allergic(),
                'probabilite_allergie': reaction.probabilite_allergie(),
                'reaction': reaction.to_dict(),
                'message': f'Probabilité d\'allergie: {reaction.probabilite_allergie():.1f}%'
            }, 200

    @allergie_reaction_ns.route('/utilisateur/<int:utilisateur_id>')
    class AllergieReactionUtilisateur(Resource):
        def get(self, utilisateur_id):
            """
            Récupérer toutes les réactions allergiques d'un utilisateur
            """
            reactions = ReactionAllergique.query.filter_by(utilisateur_id=utilisateur_id).all()
            
            return {
                'utilisateur_id': utilisateur_id,
                'total_reactions': len(reactions),
                'reactions': [reaction.to_dict() for reaction in reactions],
                'allergies_detectees': [
                    reaction.to_dict() for reaction in reactions 
                    if reaction.is_allergic()
                ]
            }, 200

    @allergie_reaction_ns.route('/utilisateur/<int:utilisateur_id>/allergies')
    class AllergiesUtilisateur(Resource):
        def get(self, utilisateur_id):
            """
            Récupérer toutes les allergies confirmées d'un utilisateur
            """
            allergies_user = AllergieUtilisateur.query.filter_by(utilisateur_id=utilisateur_id).all()
            
            return {
                'utilisateur_id': utilisateur_id,
                'total_allergies': len(allergies_user),
                'allergies': [au.to_dict() for au in allergies_user]
            }, 200

    @allergie_reaction_ns.route('/stats/<int:utilisateur_id>')
    class StatistiquesAllergies(Resource):
        def get(self, utilisateur_id):
            """
            Statistiques des allergies pour un utilisateur
            """
            reactions = ReactionAllergique.query.filter_by(utilisateur_id=utilisateur_id).all()
            allergies_confirmees = AllergieUtilisateur.query.filter_by(utilisateur_id=utilisateur_id).all()
            
            stats = {
                'utilisateur_id': utilisateur_id,
                'nombre_reactions_testees': len(reactions),
                'nombre_allergies_detectees': len([r for r in reactions if r.is_allergic()]),
                'nombre_allergies_confirmees': len(allergies_confirmees),
                'allergies_automatiques': len([a for a in allergies_confirmees if a.detectee_automatiquement]),
                'probabilites': [
                    {
                        'item': f"Aliment {r.aliment_id}" if r.aliment_id else f"Recette {r.recette_id}",
                        'probabilite': r.probabilite_allergie(),
                        'is_allergic': r.is_allergic()
                    }
                    for r in reactions
                ]
            }
            
            return stats, 200

    # Enregistrer le namespace
    api.add_namespace(allergie_reaction_ns, path='/api/allergies')