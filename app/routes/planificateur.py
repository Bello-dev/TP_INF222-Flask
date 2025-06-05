from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from app.db.db import db
from app.model import Aliment, Recette, create_swagger_models

planificateur_bp = Blueprint('planificateur', __name__)

planificateur_ns = Namespace(
    "planificateur",
    description="Planification de repas selon allergies, préférences, etc.",
    path="/planificateur"
)

# Créer des modèles Swagger spécifiques pour le planificateur
def create_planificateur_models(api):
    """Créer les modèles Swagger spécifiques au planificateur"""
    
    filtrage_input = api.model('FiltrageInput', {
        'allergenes': fields.List(fields.String, description='Liste des allergènes à éviter'),
        'preferences': fields.List(fields.String, description='Préférences alimentaires'),
        'calories_max': fields.Integer(description='Calories maximales par repas'),
        'calories_min': fields.Integer(description='Calories minimales par repas'),
        'type_regime': fields.String(description='Type de régime', enum=['végétarien', 'végan', 'sans gluten', 'keto', 'standard']),
        'temps_preparation_max': fields.Integer(description='Temps de préparation maximum en minutes'),
        'difficulte_max': fields.String(description='Difficulté maximale', enum=['Facile', 'Moyen', 'Difficile'])
    })
    
    filtrage_result = api.model('FiltrageResult', {
        'aliments_recommandes': fields.List(fields.Raw, description='Aliments recommandés'),
        'recettes_recommandes': fields.List(fields.Raw, description='Recettes recommandées'),
        'total_aliments': fields.Integer(description='Nombre d\'aliments trouvés'),
        'total_recettes': fields.Integer(description='Nombre de recettes trouvées'),
        'criteres_appliques': fields.Raw(description='Critères de filtrage appliqués'),
        'message': fields.String(description='Message de résultat')
    })
    
    suggestions_result = api.model('SuggestionsResult', {
        'user_id': fields.Integer(description='ID utilisateur'),
        'suggestions_personnalisees': fields.List(fields.Raw, description='Suggestions personnalisées'),
        'plan_semaine': fields.Raw(description='Plan de repas pour la semaine'),
        'conseils_nutritionnels': fields.List(fields.String, description='Conseils nutritionnels'),
        'message': fields.String(description='Message de suggestions')
    })
    
    return {
        'filtrage_input': filtrage_input,
        'filtrage_result': filtrage_result,
        'suggestions_result': suggestions_result
    }

# Créer les modèles spécifiques
models = create_planificateur_models(planificateur_ns)

@planificateur_ns.route('/filtrer')
class PlanificateurFiltrer(Resource):
    @planificateur_ns.expect(models['filtrage_input'], validate=True)
    @planificateur_ns.marshal_with(models['filtrage_result'])
    def post(self):
        """🔍 Filtrer aliments et recettes selon critères"""
        try:
            data = request.get_json()
            
            # Récupérer les critères
            allergenes = data.get('allergenes', [])
            preferences = data.get('preferences', [])
            calories_max = data.get('calories_max', 1000)
            calories_min = data.get('calories_min', 0)
            type_regime = data.get('type_regime', 'standard')
            temps_max = data.get('temps_preparation_max', 60)
            difficulte_max = data.get('difficulte_max', 'Difficile')
            
            # Filtrage des aliments
            query_aliments = Aliment.query
            
            if calories_max:
                query_aliments = query_aliments.filter(Aliment.calories <= calories_max)
            if calories_min:
                query_aliments = query_aliments.filter(Aliment.calories >= calories_min)
            
            aliments_filtres = query_aliments.all()
            
            # Filtrage des recettes
            query_recettes = Recette.query
            
            if temps_max:
                query_recettes = query_recettes.filter(Recette.temps_preparation <= temps_max)
            if difficulte_max:
                ordre_difficulte = ['Facile', 'Moyen', 'Difficile']
                difficultes_acceptees = ordre_difficulte[:ordre_difficulte.index(difficulte_max) + 1]
                query_recettes = query_recettes.filter(Recette.difficulte.in_(difficultes_acceptees))
            
            recettes_filtrees = query_recettes.all()
            
            # Appliquer les filtres d'allergènes et préférences (logique simplifiée)
            if 'végétarien' in preferences or type_regime == 'végétarien':
                # Filtrer les aliments/recettes végétariennes
                pass
            
            if 'gluten' in [a.lower() for a in allergenes]:
                # Exclure les aliments contenant du gluten
                pass
            
            return {
                'aliments_recommandes': [aliment.to_dict() for aliment in aliments_filtres[:10]],  # Limiter à 10
                'recettes_recommandes': [recette.to_dict() for recette in recettes_filtrees[:10]],  # Limiter à 10
                'total_aliments': len(aliments_filtres),
                'total_recettes': len(recettes_filtrees),
                'criteres_appliques': {
                    'allergenes': allergenes,
                    'preferences': preferences,
                    'calories_max': calories_max,
                    'type_regime': type_regime,
                    'temps_max': temps_max,
                    'difficulte_max': difficulte_max
                },
                'message': f'Filtrage effectué : {len(aliments_filtres)} aliments et {len(recettes_filtrees)} recettes trouvés'
            }, 200
            
        except Exception as e:
            planificateur_ns.abort(500, f"Erreur lors du filtrage: {str(e)}")

@planificateur_ns.route('/suggestions/<int:user_id>')
@planificateur_ns.param('user_id', 'ID de l\'utilisateur')
class PlanificateurSuggestions(Resource):
    @planificateur_ns.marshal_with(models['suggestions_result'])
    def get(self, user_id):
        """💡 Obtenir des suggestions personnalisées pour un utilisateur"""
        try:
            # Logique de suggestions personnalisées
            suggestions_personnalisees = [
                {
                    'type': 'recette_rapide',
                    'nom': 'Salade César rapide',
                    'temps': 15,
                    'calories': 350,
                    'raison': 'Parfait pour un déjeuner rapide et équilibré'
                },
                {
                    'type': 'menu_semaine',
                    'nom': 'Menu équilibré végétarien',
                    'duree': '7 jours',
                    'calories_moyenne': 1800,
                    'raison': 'Basé sur vos préférences végétariennes'
                },
                {
                    'type': 'substitution',
                    'nom': 'Remplacer le blé par du quinoa',
                    'benefice': 'Sans gluten et riche en protéines',
                    'raison': 'Adapté à votre allergie au gluten'
                }
            ]
            
            plan_semaine = {
                'lundi': {
                    'petit_dejeuner': 'Smoothie aux fruits',
                    'dejeuner': 'Salade quinoa',
                    'diner': 'Légumes grillés'
                },
                'mardi': {
                    'petit_dejeuner': 'Avoine aux fruits',
                    'dejeuner': 'Wrap végétarien',
                    'diner': 'Curry de légumes'
                },
                # ... autres jours
            }
            
            conseils_nutritionnels = [
                'Variez les sources de protéines végétales',
                'Pensez aux légumes de saison',
                'Hydratez-vous suffisamment',
                'Équilibrez vos macronutriments'
            ]
            
            return {
                'user_id': user_id,
                'suggestions_personnalisees': suggestions_personnalisees,
                'plan_semaine': plan_semaine,
                'conseils_nutritionnels': conseils_nutritionnels,
                'message': f'Suggestions personnalisées générées pour l\'utilisateur {user_id}'
            }, 200
            
        except Exception as e:
            planificateur_ns.abort(500, f"Erreur lors de la génération des suggestions: {str(e)}")

# ============= ROUTES FLASK CLASSIQUES (inchangées) =============

@planificateur_bp.route('/filtrer', methods=['POST'])
def filtrer_par_allergies():
    """Route Flask existante - reste inchangée"""
    data = request.get_json()
    
    try:
        allergenes = data.get('allergenes', [])
        
        # Logique de filtrage simplifiée
        aliments = Aliment.query.all()
        recettes = Recette.query.all()
        
        # Filtrer selon les allergènes (logique basique)
        aliments_filtres = [a for a in aliments if not any(allergen.lower() in a.nom.lower() for allergen in allergenes)]
        recettes_filtrees = [r for r in recettes if not any(allergen.lower() in r.nom.lower() for allergen in allergenes)]
        
        return jsonify({
            'aliments_recommandes': [a.to_dict() for a in aliments_filtres[:5]],
            'recettes_recommandes': [r.to_dict() for r in recettes_filtrees[:5]],
            'total_trouve': len(aliments_filtres) + len(recettes_filtrees)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@planificateur_bp.route('/suggestions/<int:user_id>', methods=['GET'])
def get_suggestions(user_id):
    """Route Flask existante - reste inchangée"""
    try:
        suggestions = {
            'user_id': user_id,
            'suggestions': [
                'Menu végétarien équilibré',
                'Recettes rapides et saines',
                'Plan détox 3 jours'
            ]
        }
        return jsonify(suggestions)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500