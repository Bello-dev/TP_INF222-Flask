from flask import Blueprint, jsonify
from app.model import Utilisateur, Recommandation, Recette, Aliment
import random

menu_auto_bp = Blueprint("menu_auto", __name__, url_prefix='/menu-auto')

@menu_auto_bp.route('/generate/<int:user_id>', methods=['GET'])
def generate_menu(user_id):
    try:
        user = Utilisateur.query.get_or_404(user_id)
        reco = Recommandation.query.filter_by(utilisateur_id=user_id).first()

        if not reco:
            return jsonify({'error': 'Aucune recommandation trouvée pour cet utilisateur'}), 404

        # Gestion des cas où les champs sont None
        allergenes = []
        if reco.allergenes:
            allergenes = [a.strip().lower() for a in reco.allergenes.split(',')]
        
        interdits = []
        if reco.aliments_interdits:
            interdits = [a.strip().lower() for a in reco.aliments_interdits.split(',')]

        recettes_possibles = []

        for recette in Recette.query.all():
            # Vérifier si la recette a des ingrédients
            if not hasattr(recette, 'ingredients_associes') or not recette.ingredients_associes:
                continue
                
            ingredients = recette.ingredients_associes
            skip = False

            for ri in ingredients:
                if not ri.aliment:
                    continue
                    
                aliment = ri.aliment
                
                # Vérifier les allergies (si elles existent)
                if hasattr(aliment, 'allergies') and aliment.allergies:
                    noms_allergenes = [a.nom.lower() for a in aliment.allergies]
                    
                    # Vérifier les allergènes
                    if any(allergen in noms_allergenes for allergen in allergenes):
                        skip = True
                        break
                
                # Vérifier les aliments interdits
                if aliment.nom.lower() in interdits:
                    skip = True
                    break

            if not skip:
                recettes_possibles.append(recette)

        if not recettes_possibles:
            return jsonify({'error': 'Aucune recette compatible trouvée'}), 404

        # Générer un menu pour 5 jours
        jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
        menu_genere = []

        for jour in jours:
            recette_choisie = random.choice(recettes_possibles)
            menu_genere.append({
                'jour': jour,
                'recette': recette_choisie.nom,
                'instructions': recette_choisie.instructions,
                'duree': recette_choisie.duree
            })

        return jsonify({'menu_genere': menu_genere})
    
    except Exception as e:
        # Log de l'erreur pour debugging
        print(f"Erreur dans generate_menu: {str(e)}")
        return jsonify({'error': f'Erreur interne: {str(e)}'}), 500