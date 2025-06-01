from flask import Blueprint, request, jsonify
from app.db.db import db
from app.model import Recommandation

recommandations_bp = Blueprint('recommandations', __name__, url_prefix='/recommandations')

# GET toutes les recommandations
@recommandations_bp.route('', methods=['GET'])
def get_recommandations():
    recommandations = Recommandation.query.all()
    return jsonify([
        {
            'id': r.id,
            'utilisateur_id': r.utilisateur_id,
            'type_regime': r.type_regime,
            'aliments_recommandes': r.aliments_recommandes,
            'aliments_interdits': r.aliments_interdits,
            'allergenes': r.allergenes,
            'preferences': r.preferences
        } for r in recommandations
    ])

# GET une recommandation par ID
@recommandations_bp.route('/<int:id>', methods=['GET'])
def get_recommandation(id):
    r = Recommandation.query.get_or_404(id)
    return jsonify({
        'id': r.id,
        'utilisateur_id': r.utilisateur_id,
        'type_regime': r.type_regime,
        'aliments_recommandes': r.aliments_recommandes,
        'aliments_interdits': r.aliments_interdits,
        'allergenes': r.allergenes,
        'preferences': r.preferences
    })

# POST une nouvelle recommandation
@recommandations_bp.route('', methods=['POST'])
def create_recommandation():
    data = request.get_json()
    r = Recommandation(
        utilisateur_id=data['utilisateur_id'],
        type_regime=data.get('type_regime'),
        aliments_recommandes=data.get('aliments_recommandes'),
        aliments_interdits=data.get('aliments_interdits'),
        allergenes=data.get('allergenes'),
        preferences=data.get('preferences')
    )
    db.session.add(r)
    db.session.commit()
    return jsonify({'message': 'Recommandation enregistrée', 'id': r.id}), 201

# PUT pour modifier une recommandation
@recommandations_bp.route('/<int:id>', methods=['PUT'])
def update_recommandation(id):
    r = Recommandation.query.get_or_404(id)
    data = request.get_json()
    r.type_regime = data.get('type_regime', r.type_regime)
    r.aliments_recommandes = data.get('aliments_recommandes', r.aliments_recommandes)
    r.aliments_interdits = data.get('aliments_interdits', r.aliments_interdits)
    r.allergenes = data.get('allergenes', r.allergenes)
    r.preferences = data.get('preferences', r.preferences)
    db.session.commit()
    return jsonify({'message': 'Recommandation mise à jour'})

# DELETE une recommandation
@recommandations_bp.route('/<int:id>', methods=['DELETE'])
def delete_recommandation(id):
    r = Recommandation.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Recommandation supprimée'})
