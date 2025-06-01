from flask import Blueprint, jsonify, request
from app.db.db import db
from app.model import Categorie

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

@categories_bp.route("/", methods=["GET"])
def get_all():
    return jsonify([{"id": c.id, "nom": c.nom} for c in Categorie.query.all()])

@categories_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    c = Categorie(nom=data["nom"])
    db.session.add(c)
    db.session.commit()
    return jsonify({"message": "Catégorie ajoutée", "id": c.id})

@categories_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    c = Categorie.query.get_or_404(id)
    data = request.get_json()
    c.nom = data["nom"]
    db.session.commit()
    return jsonify({"message": "Catégorie modifiée"})

@categories_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    c = Categorie.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": "Catégorie supprimée"})
