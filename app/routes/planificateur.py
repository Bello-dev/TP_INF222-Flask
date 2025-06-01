from flask import Blueprint, request, jsonify
from app.model import db, Aliment, Recette

planificateur_bp = Blueprint('planificateur', __name__)

@planificateur_bp.route('/planificateur/filtrer', methods=['POST'])
def filtrer_par_allergies():
    data = request.json
    allergies = data.get('allergies', [])
    if not allergies:
        return jsonify({'error': 'Aucune allergie fournie'}), 400

    aliments_filtrés = Aliment.query.filter(
        ~Aliment.allergenes.op('&&')(allergies)
    ).all()

    return jsonify([
        {
            'id': a.id,
            'nom': a.nom,
            'calories': a.calories,
            'type_aliment': a.type_aliment
        } for a in aliments_filtrés
    ])

