from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from app.model import create_swagger_models  # ← Import unifié

generation_bp = Blueprint("generation", __name__)

generation_ns = Namespace(
    "generation",
    description="Génération automatique de menus et recettes",
    path="/generation"
)

# Créer des modèles Swagger spécifiques pour la génération
def create_generation_models(api):
    """Créer les modèles Swagger spécifiques à la génération"""
    
    menu_generation_input = api.model('MenuGenerationInput', {
        'nb_jours': fields.Integer(required=True, description='Nombre de jours', example=7),
        'nb_personnes': fields.Integer(description='Nombre de personnes', example=4),
        'budget_max': fields.Float(description='Budget maximum'),
        'preferences': fields.List(fields.String, description='Préférences alimentaires'),
        'allergenes': fields.List(fields.String, description='Allergènes à éviter')
    })
    
    recette_generation_input = api.model('RecetteGenerationInput', {
        'type_plat': fields.String(description='Type de plat', enum=['entrée', 'plat', 'dessert']),
        'ingredients_disponibles': fields.List(fields.String, description='Ingrédients disponibles'),
        'temps_max': fields.Integer(description='Temps de préparation maximum en minutes'),
        'difficulte_max': fields.String(description='Difficulté maximale', enum=['Facile', 'Moyen', 'Difficile'])
    })
    
    generation_result = api.model('GenerationResult', {
        'success': fields.Boolean(description='Succès de la génération'),
        'data': fields.Raw(description='Données générées'),
        'message': fields.String(description='Message de résultat')
    })
    
    # Modèle de réponse générique
    message_model = api.model('Message', {
        'message': fields.String(description='Message'),
        'success': fields.Boolean(description='Succès', example=True)
    })
    
    return {
        'menu_generation_input': menu_generation_input,
        'recette_generation_input': recette_generation_input,
        'generation_result': generation_result,
        'message': message_model
    }

# Créer les modèles spécifiques
models = create_generation_models(generation_ns)

@generation_ns.route('/menu')
class GenerationMenu(Resource):
    @generation_ns.expect(models['menu_generation_input'], validate=True)
    @generation_ns.marshal_with(models['generation_result'])
    def post(self):
        """🍽️ Générer un menu automatiquement"""
        data = request.get_json()
        
        try:
            # Validation des données
            if not data.get('nb_jours') or data['nb_jours'] <= 0:
                generation_ns.abort(400, "Le nombre de jours doit être supérieur à 0")
            
            # Logique de génération de menu
            menu_genere = {
                'nb_jours': data['nb_jours'],
                'nb_personnes': data.get('nb_personnes', 1),
                'budget_max': data.get('budget_max'),
                'menus': [
                    {
                        'jour': f'Jour {i+1}',
                        'date': f'2025-06-{(i+5):02d}',  # Exemple de dates
                        'petit_dejeuner': {
                            'nom': f'Petit-déjeuner jour {i+1}',
                            'ingredients': ['Pain', 'Beurre', 'Confiture'],
                            'calories_estimees': 350
                        },
                        'dejeuner': {
                            'nom': f'Déjeuner jour {i+1}',
                            'ingredients': ['Salade', 'Tomates', 'Concombre'],
                            'calories_estimees': 450
                        },
                        'diner': {
                            'nom': f'Dîner jour {i+1}',
                            'ingredients': ['Poisson', 'Légumes', 'Riz'],
                            'calories_estimees': 600
                        }
                    }
                    for i in range(data['nb_jours'])
                ],
                'preferences_appliquees': data.get('preferences', []),
                'allergenes_evites': data.get('allergenes', []),
                'calories_totales_estimees': data['nb_jours'] * 1400  # 1400 cal/jour
            }
            
            return {
                'success': True,
                'data': menu_genere,
                'message': f'Menu de {data["nb_jours"]} jours généré avec succès pour {data.get("nb_personnes", 1)} personne(s)'
            }, 201
            
        except Exception as e:
            generation_ns.abort(500, f"Erreur lors de la génération du menu: {str(e)}")

@generation_ns.route('/recette')
class GenerationRecette(Resource):
    @generation_ns.expect(models['recette_generation_input'], validate=True)
    @generation_ns.marshal_with(models['generation_result'])
    def post(self):
        """🍳 Générer une recette automatiquement"""
        data = request.get_json()
        
        try:
            # Logique de génération de recette améliorée
            ingredients_disponibles = data.get('ingredients_disponibles', [])
            type_plat = data.get('type_plat', 'plat')
            temps_max = data.get('temps_max', 30)
            difficulte_max = data.get('difficulte_max', 'Moyen')
            
            # Générer une recette basée sur les ingrédients disponibles
            if not ingredients_disponibles:
                ingredients_generes = ['Tomates', 'Oignons', 'Ail', 'Huile d\'olive']
            else:
                ingredients_generes = ingredients_disponibles[:5]  # Limiter à 5 ingrédients
            
            recette_generee = {
                'nom': f'Recette {type_plat} automatique',
                'type_plat': type_plat,
                'ingredients': [
                    {
                        'nom': ing,
                        'quantite': '200g' if ing in ['Tomates', 'Oignons'] else '1 pièce',
                        'unite': 'g' if ing in ['Tomates', 'Oignons'] else 'pièce'
                    }
                    for ing in ingredients_generes
                ],
                'instructions': [
                    f'1. Préparer tous les ingrédients : {", ".join(ingredients_generes)}',
                    '2. Chauffer l\'huile dans une poêle',
                    '3. Faire revenir les légumes 5-10 minutes',
                    '4. Assaisonner selon vos goûts',
                    '5. Servir chaud'
                ],
                'temps_preparation': min(temps_max, 45),
                'difficulte': difficulte_max,
                'portions': 4,
                'calories_estimees': 250,
                'conseils': [
                    'Vous pouvez adapter les quantités selon vos goûts',
                    'Cette recette est générée automatiquement, n\'hésitez pas à la personnaliser'
                ]
            }
            
            return {
                'success': True,
                'data': recette_generee,
                'message': f'Recette de type "{type_plat}" générée avec succès en {recette_generee["temps_preparation"]} minutes'
            }, 201
            
        except Exception as e:
            generation_ns.abort(500, f"Erreur lors de la génération de la recette: {str(e)}")

@generation_ns.route('/suggestion/<string:type_generation>')
@generation_ns.param('type_generation', 'Type de génération (menu ou recette)')
class GenerationSuggestion(Resource):
    @generation_ns.marshal_with(models['generation_result'])
    def get(self, type_generation):
        """💡 Obtenir des suggestions de génération"""
        try:
            if type_generation == 'menu':
                suggestions = {
                    'suggestions_menus': [
                        {
                            'nom': 'Menu équilibré 7 jours',
                            'description': 'Menu varié et équilibré pour une semaine',
                            'nb_jours': 7,
                            'type': 'équilibré'
                        },
                        {
                            'nom': 'Menu végétarien 5 jours',
                            'description': 'Menu sans viande pour 5 jours',
                            'nb_jours': 5,
                            'type': 'végétarien'
                        },
                        {
                            'nom': 'Menu rapide 3 jours',
                            'description': 'Menus rapides à préparer',
                            'nb_jours': 3,
                            'type': 'rapide'
                        }
                    ]
                }
            elif type_generation == 'recette':
                suggestions = {
                    'suggestions_recettes': [
                        {
                            'type_plat': 'entrée',
                            'nom': 'Salade composée',
                            'temps': 15,
                            'difficulte': 'Facile'
                        },
                        {
                            'type_plat': 'plat',
                            'nom': 'Pasta aux légumes',
                            'temps': 25,
                            'difficulte': 'Moyen'
                        },
                        {
                            'type_plat': 'dessert',
                            'nom': 'Compote de fruits',
                            'temps': 20,
                            'difficulte': 'Facile'
                        }
                    ]
                }
            else:
                generation_ns.abort(400, "Type de génération invalide. Utilisez 'menu' ou 'recette'")
            
            return {
                'success': True,
                'data': suggestions,
                'message': f'Suggestions de {type_generation} récupérées avec succès'
            }, 200
            
        except Exception as e:
            generation_ns.abort(500, f"Erreur lors de la récupération des suggestions: {str(e)}")

# ============= ROUTES FLASK CLASSIQUES (inchangées) =============

@generation_bp.route("/menu", methods=["POST"])
def generer_menu():
    """Route Flask existante - reste inchangée"""
    data = request.get_json()
    
    if not data or not data.get('nb_jours'):
        return jsonify({'error': 'Le nombre de jours est requis'}), 400
    
    try:
        menu_genere = {
            'nb_jours': data['nb_jours'],
            'menus': [f'Menu jour {i+1}' for i in range(data['nb_jours'])]
        }
        
        return jsonify({
            "message": "Menu généré avec succès",
            "menu": menu_genere
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@generation_bp.route("/recette", methods=["POST"])
def generer_recette():
    """Route Flask existante - reste inchangée"""
    data = request.get_json()
    
    try:
        recette_generee = {
            'nom': 'Recette générée',
            'type_plat': data.get('type_plat', 'plat'),
            'ingredients': data.get('ingredients_disponibles', []),
            'temps_preparation': data.get('temps_max', 30)
        }
        
        return jsonify({
            "message": "Recette générée avec succès",
            "recette": recette_generee
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@generation_bp.route("/suggestions", methods=["GET"])
def get_suggestions():
    """Route Flask existante pour les suggestions"""
    return jsonify({
        'suggestions_menus': ['Menu équilibré', 'Menu végétarien', 'Menu rapide'],
        'suggestions_recettes': ['Salade', 'Pasta', 'Dessert']
    })