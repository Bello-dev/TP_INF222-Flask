from flask import Blueprint, request, jsonify
from app.model import db, Aliment

aliments_bp = Blueprint('aliments', __name__)

@aliments_bp.route('/aliments', methods=['GET'])
def get_aliments():
    aliments = Aliment.query.all()
    return jsonify([{
        'id': a.id,
        'nom': a.nom,
        'calories': a.calories,
        'proteines': a.proteines,
        'glucides': a.glucides,
        'lipides': a.lipides,
        'type_aliment': a.type_aliment,
        'allergies': a.allergies
    } for a in aliments])
    

@aliments_bp.route('/aliments/<int:id>', methods=['GET'])
def get_aliment(id):
    aliment = Aliment.query.get_or_404(id)
    return jsonify({
        'id': aliment.id,
        'nom': aliment.nom,
        'calories': aliment.calories,
        'proteines': aliment.proteines,
        'glucides': aliment.glucides,
        'lipides': aliment.lipides,
        'type_aliment': aliment.type_aliment,
        'allergies': aliment.allergies
    })
    

@aliments_bp.route('/aliments', methods=['POST'])
def create_aliment():
    data = request.json
    aliment = Aliment(**data)
    db.session.add(aliment)
    db.session.commit()
    return jsonify({'message': 'Aliment créé'}), 201


@aliments_bp.route('/aliments/<int:id>', methods=['PUT'])
def update_aliment(id):
    aliment = Aliment.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(aliment, key, value)
    db.session.commit()
    return jsonify({'message': 'Aliment mis à jour'})


@aliments_bp.route('/aliments/<int:id>', methods=['DELETE'])
def delete_aliment(id):
    aliment = Aliment.query.get_or_404(id)
    db.session.delete(aliment)
    db.session.commit()
    return jsonify({'message': 'Aliment supprimé'})


@aliments_bp.route('/aliments/search', methods=['GET'])
def search_aliments():
    query = request.args.get('query', '')
    aliments = Aliment.query.filter(Aliment.nom.ilike(f'%{query}%')).all()
    return jsonify([{
        'id': a.id,
        'nom': a.nom,
        'calories': a.calories,
        'proteines': a.proteines,
        'glucides': a.glucides,
        'lipides': a.lipides,
        'type_aliment': a.type_aliment,
        'allergies': a.allergies
    } for a in aliments])
    
    
@aliments_bp.route('/aliments/types', methods=['GET'])
def get_aliment_types():
    types = db.session.query(Aliment.type_aliment).distinct().all()
    return jsonify([t[0] for t in types])


@aliments_bp.route('/aliments/allergies', methods=['GET']) 
def get_allergenes():
    allergies = db.session.query(Aliment.allergies).distinct().all()
    return jsonify([a[0] for a in allergies if a[0]])


@aliments_bp.route('/aliments/types/<string:type_aliment>', methods=['GET'])  
def get_aliments_by_type(type_aliment):
    aliments = Aliment.query.filter_by(type_aliment=type_aliment).all()
    return jsonify([{
        'id': a.id,
        'nom': a.nom,
        'calories': a.calories,
        'proteines': a.proteines,
        'glucides': a.glucides,
        'lipides': a.lipides,
        'type_aliment': a.type_aliment,
        'allergies': a.allergies
    } for a in aliments]) 
