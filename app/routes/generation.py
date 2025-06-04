from flask import Blueprint, request, jsonify
from app.model import db, Utilisateur, Recommandation, Recette, Aliment, Allergie
import random

generation_bp = Blueprint("generation", __name__)

@generation_bp.route('/generate_menu/<int:user_id>', methods=['GET'])
def generate_menu(user_id):
    user_rec = Recommandation.query.filter_by(utilisateur_id=user_id).first()
    if not user_rec:
        return jsonify({'error': 'Aucune recommandation trouvée'}), 404

    # Récupère les allergènes à éviter
    allergenes = [a.strip().lower() for a in user_rec.allergenes.split(',')] if user_rec.allergenes else []

    # Aliments à éviter
    aliments_interdits = [a.strip().lower() for a in user_rec.aliments_interdits.split(',')] if user_rec.aliments_interdits else []

    # Filtrer les recettes contenant des aliments interdits ou allergènes
    recettes_valides = []
    for recette in Recette.query.all():
        nom_recette = recette.nom.lower()
        
        # Vérifier si la recette contient des ingrédients interdits
        skip = False
        for ingredient in recette.ingredients_associes:
            aliment = ingredient.aliment
            # Correction : utiliser 'allergies'
            noms_allergenes = [a.nom.lower() for a in aliment.allergies]
            
            if any(allergen in noms_allergenes for allergen in allergenes):
                skip = True
                break
            if aliment.nom.lower() in aliments_interdits:
                skip = True
                break
        
        if not skip:
            recettes_valides.append(recette)

    if not recettes_valides:
        return jsonify({'error': 'Aucune recette compatible trouvée'}), 404

    # Choix aléatoire de recettes pour 5 jours
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    menu = []
    for jour in jours:
        recette_choisie = random.choice(recettes_valides)
        menu.append({
            'jour': jour,
            'recette': recette_choisie.nom,
            'instructions': recette_choisie.instructions
        })

    return jsonify({'menu': menu})