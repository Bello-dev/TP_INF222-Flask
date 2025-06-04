from flask_sqlalchemy import SQLAlchemy
from app.db.db import db



# Association buffet/recette
buffet_recette = db.Table('buffet_recette',
    db.Column('buffet_id', db.Integer, db.ForeignKey('buffets.id'), primary_key=True),
    db.Column('recette_id', db.Integer, db.ForeignKey('recettes.id'), primary_key=True)
)

# Association aliment/allergie
aliment_allergie = db.Table('aliment_allergie',
    db.Column('aliment_id', db.Integer, db.ForeignKey('aliments.id'), primary_key=True),
    db.Column('allergie_id', db.Integer, db.ForeignKey('allergies.id'), primary_key=True)
)


# Utilisateurs
class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    menus = db.relationship('Menu', backref='utilisateur', lazy=True)

# Catégories d'aliments
class Categorie(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    images = db.relationship('Image', backref='categorie', lazy=True)

# Images
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    nom_fichier = db.Column(db.String(150), nullable=False)
    chemin = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

class Recette(db.Model):
    __tablename__ = 'recettes'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    duree = db.Column(db.Integer)
    menus = db.relationship('Menu', backref='recette', lazy=True)
    buffets = db.relationship('Buffet', secondary=buffet_recette, back_populates='recettes')
    aliments = db.relationship('RecetteAliment', back_populates='recette')
    
    # Ajouter cette propriété pour faciliter l'accès
    @property
    def ingredients_associes(self):
        return self.aliments
class Aliment(db.Model):
    __tablename__ = 'aliments'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer)
    proteines = db.Column(db.Float)
    glucides = db.Column(db.Float)
    lipides = db.Column(db.Float)
    type_aliment = db.Column(db.String(50))
    # Changer 'allergenes' en 'allergies' pour être cohérent
    allergies = db.relationship('Allergie', secondary=aliment_allergie, back_populates='aliments')
    recettes = db.relationship('RecetteAliment', back_populates='aliment')

# Menus journaliers par utilisateur
class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    jour = db.Column(db.String(20), nullable=False)
    recette_id = db.Column(db.Integer, db.ForeignKey('recettes.id'), nullable=False)

# Buffets
class Buffet(db.Model):
    __tablename__ = 'buffets'
    id = db.Column(db.Integer, primary_key=True)
    evenement = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    lieu = db.Column(db.String(100))
    recettes = db.relationship('Recette', secondary=buffet_recette, back_populates='buffets')

# Recommandations (personnalisées par utilisateur)
class Recommandation(db.Model):
    __tablename__ = 'recommandations'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    type_regime = db.Column(db.String(100))
    aliments_recommandes = db.Column(db.Text)
    aliments_interdits = db.Column(db.Text)
    allergenes = db.Column(db.Text)
    preferences = db.Column(db.Text)

# Allergies connues
class Allergie(db.Model):
    __tablename__ = 'allergies'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))
    aliments = db.relationship('Aliment', secondary=aliment_allergie, back_populates='allergies')

# Association entre Recette et Aliment pour les quantités
class RecetteAliment(db.Model):
    __tablename__ = 'recette_aliment'
    recette_id = db.Column(db.Integer, db.ForeignKey('recettes.id'), primary_key=True)
    aliment_id = db.Column(db.Integer, db.ForeignKey('aliments.id'), primary_key=True)
    quantite = db.Column(db.Float)

    recette = db.relationship('Recette', back_populates='aliments')
    aliment = db.relationship('Aliment', back_populates='recettes')
