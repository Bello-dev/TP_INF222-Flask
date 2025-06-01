from flask import Blueprint, request, jsonify
from app.model import db, Buffet, Recette

buffet_bp = Blueprint('buffet', __name__)

@buffet_bp.route('/buffets', methods=['GET'])
def get_buffets():
    return jsonify([{
        'id': b.id,
        'evenement': b.evenement,
        'date': b.date,
        'lieu': b.lieu
    } for b in Buffet.query.all()])

@buffet_bp.route('/buffets/<int:id>', methods=['GET'])
def get_buffet(id):
    b = Buffet.query.get_or_404(id)
    return jsonify({'id': b.id, 'evenement': b.evenement, 'date': b.date, 'lieu': b.lieu})

@buffet_bp.route('/buffets', methods=['POST'])
def create_buffet():
    data = request.get_json()
    buffet = Buffet(
        evenement=data['evenement'],
        date=data['date'],
        lieu=data.get('lieu')
    )
    if 'recette_ids' in data:
        recettes = Recette.query.filter(Recette.id.in_(data['recette_ids'])).all()
        buffet.recettes.extend(recettes)
    db.session.add(buffet)
    db.session.commit()
    return jsonify({'message': 'Buffet créé', 'id': buffet.id}), 201



@buffet_bp.route('/buffets/<int:id>', methods=['PUT'])
def update_buffet(id):
    b = Buffet.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(b, key, value)
    db.session.commit()
    return jsonify({'message': 'Buffet mis à jour'})

@buffet_bp.route('/buffets/<int:id>', methods=['DELETE'])
def delete_buffet(id):
    b = Buffet.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    return jsonify({'message': 'Buffet supprimé'})
