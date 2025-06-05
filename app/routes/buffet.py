from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource
from app.db.db import db
from app.model import Buffet, create_swagger_models  # ← Import unifié

buffet_bp = Blueprint('buffet', __name__)

buffets_ns = Namespace(
    "buffets",
    description="Gestion des buffets et événements",
    path="/buffets"
)

# Utiliser la fonction centralisée du model.py
models = create_swagger_models(buffets_ns)

@buffets_ns.route('/')
class BuffetsList(Resource):
    @buffets_ns.marshal_list_with(models['buffet'])
    def get(self):
        """📋 Liste tous les buffets"""
        try:
            buffets = Buffet.query.all()
            return [buffet.to_dict() for buffet in buffets], 200
        except Exception as e:
            buffets_ns.abort(500, f"Erreur serveur: {str(e)}")

    @buffets_ns.expect(models['buffet_input'], validate=True)
    @buffets_ns.marshal_with(models['buffet'], code=201)
    def post(self):
        """➕ Créer un buffet"""
        try:
            data = request.get_json()
            
            if not data or not data.get('nom'):
                buffets_ns.abort(400, "Le nom du buffet est requis")
            
            nouveau_buffet = Buffet(
                nom=data['nom'],
                description=data.get('description'),
                date_debut=data.get('date_debut'),
                date_fin=data.get('date_fin'),
                nb_personnes=data.get('nb_personnes')
            )
            
            db.session.add(nouveau_buffet)
            db.session.commit()
            
            return nouveau_buffet.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            buffets_ns.abort(500, f"Erreur lors de la création: {str(e)}")

@buffets_ns.route('/<int:buffet_id>')
@buffets_ns.param('buffet_id', 'ID du buffet')
class BuffetDetail(Resource):
    @buffets_ns.marshal_with(models['buffet'])
    def get(self, buffet_id):
        """🔍 Obtenir un buffet par ID"""
        buffet = Buffet.query.get_or_404(buffet_id)
        return buffet.to_dict()

    @buffets_ns.expect(models['buffet_input'], validate=True)
    @buffets_ns.marshal_with(models['buffet'])
    def put(self, buffet_id):
        """✏️ Modifier un buffet"""
        buffet = Buffet.query.get_or_404(buffet_id)
        data = request.get_json()
        
        try:
            buffet.nom = data.get('nom', buffet.nom)
            buffet.description = data.get('description', buffet.description)
            buffet.date_debut = data.get('date_debut', buffet.date_debut)
            buffet.date_fin = data.get('date_fin', buffet.date_fin)
            buffet.nb_personnes = data.get('nb_personnes', buffet.nb_personnes)
            
            db.session.commit()
            return buffet.to_dict()
            
        except Exception as e:
            db.session.rollback()
            buffets_ns.abort(500, f"Erreur lors de la modification: {str(e)}")

    @buffets_ns.marshal_with(models['message'])
    def delete(self, buffet_id):
        """🗑️ Supprimer un buffet"""
        try:
            buffet = Buffet.query.get_or_404(buffet_id)
            nom_buffet = buffet.nom
            db.session.delete(buffet)
            db.session.commit()
            return {'message': f'Buffet "{nom_buffet}" supprimé avec succès', 'success': True, 'id': buffet_id}, 200
            
        except Exception as e:
            db.session.rollback()
            buffets_ns.abort(500, f"Erreur lors de la suppression: {str(e)}")

# ============= ROUTES FLASK CLASSIQUES (inchangées) =============

@buffet_bp.route("/", methods=["GET"])
def get_all():
    """Route Flask existante - reste inchangée"""
    buffets = Buffet.query.all()
    return jsonify([buffet.to_dict() for buffet in buffets])

@buffet_bp.route("/", methods=["POST"])
def create():
    """Route Flask existante - reste inchangée"""
    data = request.get_json()
    
    if not data or not data.get('nom'):
        return jsonify({'error': 'Le nom est requis'}), 400
    
    try:
        nouveau_buffet = Buffet(
            nom=data['nom'],
            description=data.get('description'),
            date_debut=data.get('date_debut'),
            date_fin=data.get('date_fin'),
            nb_personnes=data.get('nb_personnes')
        )
        
        db.session.add(nouveau_buffet)
        db.session.commit()
        
        return jsonify(nouveau_buffet.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@buffet_bp.route("/<int:buffet_id>", methods=["GET"])
def get_buffet(buffet_id):
    """Route Flask existante - reste inchangée"""
    buffet = Buffet.query.get_or_404(buffet_id)
    return jsonify(buffet.to_dict())

@buffet_bp.route("/<int:buffet_id>", methods=["PUT"])
def update(buffet_id):
    """Route Flask existante - reste inchangée"""
    buffet = Buffet.query.get_or_404(buffet_id)
    data = request.get_json()
    
    try:
        buffet.nom = data.get('nom', buffet.nom)
        buffet.description = data.get('description', buffet.description)
        buffet.date_debut = data.get('date_debut', buffet.date_debut)
        buffet.date_fin = data.get('date_fin', buffet.date_fin)
        buffet.nb_personnes = data.get('nb_personnes', buffet.nb_personnes)
        
        db.session.commit()
        return jsonify(buffet.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@buffet_bp.route("/<int:buffet_id>", methods=["DELETE"])
def delete_buffet(buffet_id):
    """Route Flask existante - reste inchangée"""
    try:
        buffet = Buffet.query.get_or_404(buffet_id)
        db.session.delete(buffet)
        db.session.commit()
        return jsonify({'message': 'Buffet supprimé avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500