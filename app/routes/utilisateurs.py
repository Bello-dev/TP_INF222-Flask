from flask import Blueprint, request, jsonify
from app.model import db, Utilisateur

utilisateurs_bp = Blueprint('utilisateurs', __name__)

@utilisateurs_bp.route('/utilisateurs', methods=['GET'])
def get_utilisateurs():
    return jsonify([{
        'id': u.id,
        'nom': u.nom,
        'email': u.email
    } for u in Utilisateur.query.all()])

@utilisateurs_bp.route('/utilisateurs/<int:id>', methods=['GET'])
def get_utilisateur(id):
    u = Utilisateur.query.get_or_404(id)
    return jsonify({'id': u.id, 'nom': u.nom, 'email': u.email})

@utilisateurs_bp.route('/utilisateurs', methods=['POST'])
def create_utilisateur():
    data = request.json
    u = Utilisateur(**data)
    db.session.add(u)
    db.session.commit()
    return jsonify({'message': 'Utilisateur créé'}), 201

@utilisateurs_bp.route('/utilisateurs/<int:id>', methods=['PUT'])
def update_utilisateur(id):
    u = Utilisateur.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(u, key, value)
    db.session.commit()
    return jsonify({'message': 'Utilisateur mis à jour'})

@utilisateurs_bp.route('/utilisateurs/<int:id>', methods=['DELETE'])
def delete_utilisateur(id):
    u = Utilisateur.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({'message': 'Utilisateur supprimé'})
