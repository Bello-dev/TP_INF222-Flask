from flask import Blueprint, request, jsonify
from app.model import db, Menu

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menus', methods=['GET'])
def get_menus():
    menus = Menu.query.all()
    return jsonify([{
        'id': m.id,
        'utilisateur_id': m.utilisateur_id,
        'jour': m.jour,
        'recette_id': m.recette_id
    } for m in menus])

@menu_bp.route('/menus/<int:id>', methods=['GET'])
def get_menu(id):
    m = Menu.query.get_or_404(id)
    return jsonify({'id': m.id, 'utilisateur_id': m.utilisateur_id, 'jour': m.jour, 'recette_id': m.recette_id})

@menu_bp.route('/menus', methods=['POST'])
def create_menu():
    data = request.json
    m = Menu(**data)
    db.session.add(m)
    db.session.commit()
    return jsonify({'message': 'Menu créé'}), 201

@menu_bp.route('/menus/<int:id>', methods=['PUT'])
def update_menu(id):
    m = Menu.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(m, key, value)
    db.session.commit()
    return jsonify({'message': 'Menu mis à jour'})

@menu_bp.route('/menus/<int:id>', methods=['DELETE'])
def delete_menu(id):
    m = Menu.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': 'Menu supprimé'})
