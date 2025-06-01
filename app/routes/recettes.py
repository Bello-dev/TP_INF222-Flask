from flask import Blueprint, request, jsonify
from app.db.db import db
from app.model import Recette

recettes_bp = Blueprint('recettes', __name__, url_prefix='/recettes')

# GET toutes les recettes
@recettes_bp.route('', methods=['GET'])
def get_recettes():
    recettes = Recette.query.all()
    return jsonify([
        {
            'id': r.id,
            'nom': r.nom,
            'instructions': r.instructions,
            'duree': r.duree
        } for r in recettes
    ])

# GET une recette par ID
@recettes_bp.route('/<int:id>', methods=['GET'])
def get_recette(id):
    recette = Recette.query.get_or_404(id)
    return jsonify({
        'id': recette.id,
        'nom': recette.nom,
        'instructions': recette.instructions,
        'duree': recette.duree
    })

# POST une nouvelle recette
@recettes_bp.route('', methods=['POST'])
def create_recette():
    data = request.get_json()
    recette = Recette(
        nom=data['nom'],
        instructions=data['instructions'],
        duree=data.get('duree')
    )
    db.session.add(recette)
    db.session.commit()
    return jsonify({'message': 'Recette créée', 'id': recette.id}), 201

# PUT pour modifier une recette
@recettes_bp.route('/<int:id>', methods=['PUT'])
def update_recette(id):
    recette = Recette.query.get_or_404(id)
    data = request.get_json()
    recette.nom = data.get('nom', recette.nom)
    recette.instructions = data.get('instructions', recette.instructions)
    recette.duree = data.get('duree', recette.duree)
    db.session.commit()
    return jsonify({'message': 'Recette mise à jour'})

# DELETE une recette
@recettes_bp.route('/<int:id>', methods=['DELETE'])
def delete_recette(id):
    recette = Recette.query.get_or_404(id)
    db.session.delete(recette)
    db.session.commit()
    return jsonify({'message': 'Recette supprimée'})
