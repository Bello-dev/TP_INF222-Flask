from flask import Blueprint, jsonify, request
from app.model import db, Aliment

aliments_bp = Blueprint('aliments', __name__, url_prefix='/aliments')

@aliments_bp.route('/', methods=['GET'])
@aliments_bp.route('', methods=['GET'])
def get_aliments():
    try:
        aliments = Aliment.query.all()
        result = []
        for a in aliments:
            aliment_data = {
                'id': a.id,
                'nom': a.nom,
                'calories': a.calories,
                'proteines': a.proteines,
                'glucides': a.glucides,
                'lipides': a.lipides,
                'type_aliment': a.type_aliment
            }
            
            # Gestion sécurisée des allergies
            try:
                if hasattr(a, 'allergies') and a.allergies:
                    aliment_data['allergies'] = [{'id': allergie.id, 'nom': allergie.nom} for allergie in a.allergies]
                else:
                    aliment_data['allergies'] = []
            except:
                aliment_data['allergies'] = []
            
            result.append(aliment_data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Erreur: {str(e)}'}), 500

@aliments_bp.route('/<int:id>', methods=['GET'])
def get_aliment(id):
    try:
        aliment = Aliment.query.get_or_404(id)
        return jsonify({
            'id': aliment.id,
            'nom': aliment.nom,
            'calories': aliment.calories,
            'proteines': aliment.proteines,
            'glucides': aliment.glucides,
            'lipides': aliment.lipides,
            'type_aliment': aliment.type_aliment,
            'allergies': [{'id': allergie.id, 'nom': allergie.nom} for allergie in aliment.allergies] if aliment.allergies else []
        })
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération de l\'aliment: {str(e)}'}), 500

@aliments_bp.route('/types', methods=['GET'])
def get_aliment_types():
    try:
        types = db.session.query(Aliment.type_aliment).distinct().all()
        return jsonify([t[0] for t in types])
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération des types: {str(e)}'}), 500

@aliments_bp.route('/allergies', methods=['GET'])
def get_allergenes():
    try:
        from app.model import Allergie
        allergies = Allergie.query.all()
        return jsonify([{'id': a.id, 'nom': a.nom} for a in allergies])
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération des allergies: {str(e)}'}), 500

@aliments_bp.route('/', methods=['POST'])
def create_aliment():
    try:
        data = request.json
        aliment = Aliment(**data)
        db.session.add(aliment)
        db.session.commit()
        return jsonify({'message': 'Aliment créé'}), 201
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la création: {str(e)}'}), 500

@aliments_bp.route('/<int:id>', methods=['PUT'])
def update_aliment(id):
    try:
        aliment = Aliment.get_or_404(id)
        data = request.json
        for key, value in data.items():
            setattr(aliment, key, value)
        db.session.commit()
        return jsonify({'message': 'Aliment mis à jour'})
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la mise à jour: {str(e)}'}), 500

@aliments_bp.route('/<int:id>', methods=['DELETE'])
def delete_aliment(id):
    try:
        aliment = Aliment.query.get_or_404(id)
        db.session.delete(aliment)
        db.session.commit()
        return jsonify({'message': 'Aliment supprimé'})
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la suppression: {str(e)}'}), 500