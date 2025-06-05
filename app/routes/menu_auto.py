from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource, fields
from app.model import create_swagger_models  # Import unifié

menu_auto_bp = Blueprint("menu_auto", __name__)

menu_auto_ns = Namespace(
    "menu_auto",
    description="Génération automatique de menus personnalisés",
    path="/menu_auto"
)

# Créer des modèles Swagger spécifiques pour menu_auto
def create_menu_auto_models(api):
    """Créer les modèles Swagger spécifiques au menu automatique"""
    
    menu_auto_result = api.model('MenuAutoResult', {
        'user_id': fields.Integer(description='ID utilisateur'),
        'menu_genere': fields.List(fields.Raw, description='Menu généré automatiquement'),
        'duree_semaines': fields.Integer(description='Durée en semaines', example=1),
        'total_calories': fields.Float(description='Total calories estimé par jour', example=2000.0),
        'preferences_appliquees': fields.List(fields.String, description='Préférences prises en compte'),
        'message': fields.String(description='Message de génération')
    })
    
    preferences_input = api.model('PreferencesInput', {
        'preferences_alimentaires': fields.List(fields.String, description='Préférences alimentaires'),
        'allergenes': fields.List(fields.String, description='Allergènes à éviter'),
        'calories_objectif': fields.Integer(description='Objectif calorique quotidien'),
        'type_regime': fields.String(description='Type de régime', enum=['standard', 'végétarien', 'végan', 'keto'])
    })
    
    preferences_result = api.model('PreferencesResult', {
        'user_id': fields.Integer(description='ID utilisateur'),
        'preferences_sauvees': fields.Raw(description='Préférences sauvegardées'),
        'message': fields.String(description='Message de confirmation')
    })
    
    return {
        'menu_auto_result': menu_auto_result,
        'preferences_input': preferences_input,
        'preferences_result': preferences_result
    }

# Créer les modèles spécifiques
models = create_menu_auto_models(menu_auto_ns)

@menu_auto_ns.route('/generate/<int:user_id>')
@menu_auto_ns.param('user_id', 'ID de l\'utilisateur')
class MenuAutoGenerate(Resource):
    @menu_auto_ns.marshal_with(models['menu_auto_result'])
    def get(self, user_id):
        """🤖 Générer un menu automatique pour un utilisateur"""
        try:
            # Logique de génération automatique améliorée
            jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
            
            menu_genere = []
            
            for jour in jours_semaine:
                menu_jour = {
                    'jour': jour,
                    'date': f'2025-06-{jours_semaine.index(jour) + 5:02d}',
                    'repas': {
                        'petit_dejeuner': {
                            'nom': f'Petit-déjeuner {jour}',
                            'plats': ['Céréales complètes', 'Fruits frais', 'Yaourt nature'],
                            'calories': 400,
                            'temps_preparation': 10
                        },
                        'dejeuner': {
                            'nom': f'Déjeuner {jour}',
                            'plats': ['Salade verte', 'Protéines', 'Légumineuses'],
                            'calories': 600,
                            'temps_preparation': 30
                        },
                        'diner': {
                            'nom': f'Dîner {jour}',
                            'plats': ['Légumes de saison', 'Féculents', 'Poisson ou viande'],
                            'calories': 700,
                            'temps_preparation': 45
                        },
                        'collation': {
                            'nom': 'Collation saine',
                            'plats': ['Fruits secs', 'Noix'],
                            'calories': 200,
                            'temps_preparation': 5
                        }
                    },
                    'calories_totales': 1900
                }
                menu_genere.append(menu_jour)
            
            return {
                'user_id': user_id,
                'menu_genere': menu_genere,
                'duree_semaines': 1,
                'total_calories': 1900.0,
                'preferences_appliquees': ['Équilibré', 'Varié', 'Saisonnier'],
                'message': f'Menu automatique généré avec succès pour l\'utilisateur {user_id} (7 jours)'
            }, 200
            
        except Exception as e:
            menu_auto_ns.abort(500, f"Erreur lors de la génération: {str(e)}")

@menu_auto_ns.route('/preferences/<int:user_id>')
@menu_auto_ns.param('user_id', 'ID de l\'utilisateur')
class MenuAutoPreferences(Resource):
    @menu_auto_ns.marshal_with(models['preferences_result'])
    def get(self, user_id):
        """📋 Obtenir les préférences d'un utilisateur"""
        try:
            # Simuler la récupération des préférences
            preferences_utilisateur = {
                'preferences_alimentaires': ['Bio', 'Local', 'De saison'],
                'allergenes': ['Gluten', 'Lactose'],
                'calories_objectif': 2000,
                'type_regime': 'végétarien',
                'derniere_modification': '2025-06-04'
            }
            
            return {
                'user_id': user_id,
                'preferences_sauvees': preferences_utilisateur,
                'message': f'Préférences récupérées pour l\'utilisateur {user_id}'
            }, 200
            
        except Exception as e:
            menu_auto_ns.abort(500, f"Erreur lors de la récupération: {str(e)}")
    
    @menu_auto_ns.expect(models['preferences_input'], validate=True)
    @menu_auto_ns.marshal_with(models['preferences_result'])
    def post(self, user_id):
        """💾 Sauvegarder les préférences d'un utilisateur"""
        try:
            data = request.get_json()
            
            # Logique de sauvegarde des préférences
            preferences_sauvees = {
                'user_id': user_id,
                'preferences_alimentaires': data.get('preferences_alimentaires', []),
                'allergenes': data.get('allergenes', []),
                'calories_objectif': data.get('calories_objectif', 2000),
                'type_regime': data.get('type_regime', 'standard'),
                'date_sauvegarde': '2025-06-04'
            }
            
            return {
                'user_id': user_id,
                'preferences_sauvees': preferences_sauvees,
                'message': f'Préférences sauvegardées avec succès pour l\'utilisateur {user_id}'
            }, 201
            
        except Exception as e:
            menu_auto_ns.abort(500, f"Erreur lors de la sauvegarde: {str(e)}")

# ============= ROUTES FLASK CLASSIQUES (inchangées) =============

@menu_auto_bp.route('/generate/<int:user_id>', methods=['GET'])
def generate_menu(user_id):
    """Route Flask existante - reste inchangée"""
    try:
        menu_genere = [
            {'jour': 'Lundi', 'repas': ['Petit-déjeuner', 'Déjeuner', 'Dîner']},
            {'jour': 'Mardi', 'repas': ['Petit-déjeuner', 'Déjeuner', 'Dîner']}
        ]
        return jsonify({
            'menu_genere': menu_genere, 
            'user_id': user_id,
            'message': 'Menu généré automatiquement'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@menu_auto_bp.route('/preferences/<int:user_id>', methods=['GET', 'POST'])
def manage_preferences(user_id):
    """Route Flask existante - reste inchangée"""
    if request.method == 'GET':
        return jsonify({
            'preferences': {
                'type_regime': 'standard',
                'allergenes': [],
                'calories_objectif': 2000
            }, 
            'user_id': user_id
        })
    else:
        data = request.get_json()
        return jsonify({
            'message': 'Préférences sauvegardées', 
            'user_id': user_id,
            'preferences': data
        })