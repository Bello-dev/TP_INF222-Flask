from flask_sqlalchemy import SQLAlchemy
from flask_restx import fields
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.db.db import db

# ============= MODÈLES DE BASE DE DONNÉES =============

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    poids = db.Column(db.Float)
    taille = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    recommandations = db.relationship('Recommandation', backref='utilisateur', lazy=True)
    reactions_allergiques = db.relationship('ReactionAllergique', backref='utilisateur', lazy=True)
    allergies_utilisateur = db.relationship('AllergieUtilisateur', backref='utilisateur', lazy=True)
    
    def set_password(self, password):
        """Hasher le mot de passe"""
        self.mot_de_passe_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Vérifier le mot de passe"""
        return check_password_hash(self.mot_de_passe_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'email': self.email,
            'age': self.age,
            'poids': self.poids,
            'taille': self.taille,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_swagger_model(api):
        return api.model('Utilisateur', {
            'id': fields.Integer(required=True, description='ID unique de l\'utilisateur'),
            'nom': fields.String(required=True, description='Nom de famille', example='Martin'),
            'prenom': fields.String(required=True, description='Prénom', example='Jean'),
            'email': fields.String(required=True, description='Adresse email', example='jean.martin@example.com'),
            'age': fields.Integer(description='Âge', example=25),
            'poids': fields.Float(description='Poids en kg', example=70.5),
            'taille': fields.Float(description='Taille en cm', example=175.0),
            'created_at': fields.DateTime(description='Date de création du compte'),
            'updated_at': fields.DateTime(description='Date de dernière modification')
        })
    
    @staticmethod
    def get_swagger_input_model(api):
        return api.model('UtilisateurInput', {
            'nom': fields.String(required=True, description='Nom de famille', example='Dupont'),
            'prenom': fields.String(required=True, description='Prénom', example='Marie'),
            'email': fields.String(required=True, description='Adresse email', example='marie.dupont@example.com'),
            'mot_de_passe': fields.String(required=True, description='Mot de passe'),
            'age': fields.Integer(description='Âge', example=28),
            'poids': fields.Float(description='Poids en kg', example=65.0),
            'taille': fields.Float(description='Taille en cm', example=168.0)
        })

class Categorie(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    aliments = db.relationship('Aliment', backref='categorie', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def get_swagger_model(api):
        return api.model('Categorie', {
            'id': fields.Integer(readonly=True, description='ID'),
            'nom': fields.String(required=True, description='Nom de la catégorie'),
            'description': fields.String(description='Description de la catégorie'),
            'created_at': fields.DateTime(description='Date de création')
        })
    
    @staticmethod
    def get_swagger_input_model(api):
        return api.model('CategorieInput', {
            'nom': fields.String(required=True, description='Nom de la catégorie'),
            'description': fields.String(description='Description de la catégorie')
        })

class Aliment(db.Model):
    __tablename__ = 'aliments'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    calories = db.Column(db.Float, default=0)
    proteines = db.Column(db.Float, default=0)
    lipides = db.Column(db.Float, default=0)
    glucides = db.Column(db.Float, default=0)
    fibres = db.Column(db.Float, default=0)
    type_aliment = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    
    # Relations
    reactions_allergiques = db.relationship('ReactionAllergique', backref='aliment', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'calories': self.calories,
            'proteines': self.proteines,
            'lipides': self.lipides,
            'glucides': self.glucides,
            'fibres': self.fibres,
            'type_aliment': self.type_aliment,
            'categorie_id': self.categorie_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_swagger_model(api):
        return api.model('Aliment', {
            'id': fields.Integer(required=True, description='ID unique de l\'aliment'),
            'nom': fields.String(required=True, description='Nom de l\'aliment', example='Pomme'),
            'description': fields.String(description='Description de l\'aliment'),
            'calories': fields.Float(description='Calories pour 100g', example=52.0),
            'proteines': fields.Float(description='Protéines en grammes pour 100g', example=0.3),
            'lipides': fields.Float(description='Lipides en grammes pour 100g', example=0.2),
            'glucides': fields.Float(description='Glucides en grammes pour 100g', example=14.0),
            'fibres': fields.Float(description='Fibres en grammes pour 100g', example=2.4),
            'type_aliment': fields.String(description='Type d\'aliment'),
            'categorie_id': fields.Integer(description='ID de la catégorie'),
            'created_at': fields.DateTime(description='Date de création'),
            'updated_at': fields.DateTime(description='Date de dernière modification')
        })
    
    @staticmethod
    def get_swagger_input_model(api):
        return api.model('AlimentInput', {
            'nom': fields.String(required=True, description='Nom de l\'aliment', example='Banane'),
            'description': fields.String(description='Description de l\'aliment'),
            'calories': fields.Float(description='Calories pour 100g', example=89.0),
            'proteines': fields.Float(description='Protéines en grammes pour 100g', example=1.1),
            'lipides': fields.Float(description='Lipides en grammes pour 100g', example=0.3),
            'glucides': fields.Float(description='Glucides en grammes pour 100g', example=23.0),
            'fibres': fields.Float(description='Fibres en grammes pour 100g', example=2.6),
            'type_aliment': fields.String(description='Type d\'aliment'),
            'categorie_id': fields.Integer(description='ID de la catégorie')
        })

class Recette(db.Model):
    __tablename__ = 'recettes'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text, nullable=False)
    temps_preparation = db.Column(db.Integer, default=0)  # en minutes
    difficulte = db.Column(db.String(20), default='Facile')  # Facile, Moyen, Difficile
    portions = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    recommandations = db.relationship('Recommandation', backref='recette', lazy=True)
    reactions_allergiques = db.relationship('ReactionAllergique', backref='recette', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'instructions': self.instructions,
            'temps_preparation': self.temps_preparation,
            'difficulte': self.difficulte,
            'portions': self.portions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_swagger_model(api):
        return api.model('Recette', {
            'id': fields.Integer(required=True, description='ID unique de la recette'),
            'nom': fields.String(required=True, description='Nom de la recette', example='Salade de fruits'),
            'description': fields.String(description='Description de la recette'),
            'instructions': fields.String(description='Instructions de préparation'),
            'temps_preparation': fields.Integer(description='Temps de préparation en minutes', example=15),
            'difficulte': fields.String(description='Niveau de difficulté', enum=['Facile', 'Moyen', 'Difficile']),
            'portions': fields.Integer(description='Nombre de portions', example=4),
            'created_at': fields.DateTime(description='Date de création'),
            'updated_at': fields.DateTime(description='Date de dernière modification')
        })
    
    @staticmethod
    def get_swagger_input_model(api):
        return api.model('RecetteInput', {
            'nom': fields.String(required=True, description='Nom de la recette', example='Smoothie aux fruits'),
            'description': fields.String(description='Description de la recette'),
            'instructions': fields.String(description='Instructions détaillées de préparation'),
            'temps_preparation': fields.Integer(description='Temps de préparation en minutes', example=10),
            'difficulte': fields.String(description='Niveau de difficulté', enum=['Facile', 'Moyen', 'Difficile'], example='Facile'),
            'portions': fields.Integer(description='Nombre de portions', example=2)
        })

class Allergie(db.Model):
    __tablename__ = 'allergies'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    gravite = db.Column(db.String(20), default='Modéré')  # Léger, Modéré, Sévère
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    allergies_utilisateur = db.relationship('AllergieUtilisateur', backref='allergie', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'gravite': self.gravite,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def get_swagger_model(api):
        return api.model('Allergie', {
            'id': fields.Integer(required=True, description='ID unique de l\'allergie'),
            'nom': fields.String(required=True, description='Nom de l\'allergie', example='Arachides'),
            'description': fields.String(description='Description détaillée'),
            'gravite': fields.String(description='Niveau de gravité', enum=['Léger', 'Modéré', 'Sévère']),
            'created_at': fields.DateTime(description='Date de création')
        })
    
    @staticmethod
    def get_swagger_input_model(api):
        return api.model('AllergieInput', {
            'nom': fields.String(required=True, description='Nom de l\'allergie', example='Gluten'),
            'description': fields.String(description='Description détaillée'),
            'gravite': fields.String(description='Niveau de gravité', enum=['Léger', 'Modéré', 'Sévère'], example='Modéré')
        })

# ============= NOUVELLES TABLES POUR GESTION ALLERGIES =============

class ReactionAllergique(db.Model):
    """
    Gère l'historique des réactions allergiques d'un utilisateur 
    pour un aliment ou une recette.
    """
    __tablename__ = 'reactions_allergiques'
    
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    aliment_id = db.Column(db.Integer, db.ForeignKey('aliments.id'), nullable=True)
    recette_id = db.Column(db.Integer, db.ForeignKey('recettes.id'), nullable=True)
    
    times_eaten = db.Column(db.Integer, default=0)
    times_reacted = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'aliment_id': self.aliment_id,
            'recette_id': self.recette_id,
            'times_eaten': self.times_eaten,
            'times_reacted': self.times_reacted,
            'probabilite_allergie': self.probabilite_allergie(),
            'is_allergic': self.is_allergic(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def probabilite_allergie(self):
        """Renvoie la probabilité d'allergie (en pourcentage)."""
        if self.times_eaten == 0:
            return 0.0
        return (self.times_reacted / self.times_eaten) * 100

    def is_allergic(self):
        """Renvoie True si la probabilité d'allergie dépasse 30%."""
        return self.probabilite_allergie() > 30
    
    @staticmethod
    def get_swagger_model(api):
        return api.model('ReactionAllergique', {
            'id': fields.Integer(readonly=True, description='ID unique'),
            'utilisateur_id': fields.Integer(required=True, description='ID utilisateur'),
            'aliment_id': fields.Integer(description='ID aliment concerné'),
            'recette_id': fields.Integer(description='ID recette concernée'),
            'times_eaten': fields.Integer(description='Nombre de fois consommé'),
            'times_reacted': fields.Integer(description='Nombre de réactions allergiques'),
            'probabilite_allergie': fields.Float(description='Probabilité estimée (en %)'),
            'is_allergic': fields.Boolean(description='True si probabilité > 30 %'),
            'created_at': fields.DateTime(description='Date de création'),
            'updated_at': fields.DateTime(description='Dernière modification')
        })
    
    @staticmethod
    def get_swagger_input_model(api):
        return api.model('ReactionAllergiqueInput', {
            'utilisateur_id': fields.Integer(required=True, description='ID de l\'utilisateur'),
            'aliment_id': fields.Integer(description='ID de l\'aliment (si applicable)'),
            'recette_id': fields.Integer(description='ID de la recette (si applicable)'),
            'times_eaten': fields.Integer(required=True, description='Nombre de fois consommé'),
            'times_reacted': fields.Integer(required=True, description='Nombre de réactions allergiques')
        })

class AllergieUtilisateur(db.Model):
    """
    Table de liaison entre utilisateurs et allergies.
    Stocke les allergies confirmées d'un utilisateur.
    """
    __tablename__ = 'allergies_utilisateur'
    
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    allergie_id = db.Column(db.Integer, db.ForeignKey('allergies.id'), nullable=False)
    gravite_personnelle = db.Column(db.String(20), default='Modéré')  # Gravité spécifique à l'utilisateur
    detectee_automatiquement = db.Column(db.Boolean, default=False)  # True si détectée via probabilité
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Contrainte d'unicité
    __table_args__ = (db.UniqueConstraint('utilisateur_id', 'allergie_id'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'allergie_id': self.allergie_id,
            'gravite_personnelle': self.gravite_personnelle,
            'detectee_automatiquement': self.detectee_automatiquement,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def get_swagger_model(api):
        return api.model('AllergieUtilisateur', {
            'id': fields.Integer(readonly=True, description='ID unique'),
            'utilisateur_id': fields.Integer(required=True, description='ID utilisateur'),
            'allergie_id': fields.Integer(required=True, description='ID allergie'),
            'gravite_personnelle': fields.String(description='Gravité pour cet utilisateur', enum=['Léger', 'Modéré', 'Sévère']),
            'detectee_automatiquement': fields.Boolean(description='Détectée automatiquement via probabilité'),
            'created_at': fields.DateTime(description='Date d\'ajout')
        })
    
    @staticmethod
    def get_swagger_input_model(api):
        return api.model('AllergieUtilisateurInput', {
            'utilisateur_id': fields.Integer(required=True, description='ID de l\'utilisateur'),
            'allergie_id': fields.Integer(required=True, description='ID de l\'allergie'),
            'gravite_personnelle': fields.String(description='Gravité personnelle', enum=['Léger', 'Modéré', 'Sévère'], example='Modéré')
        })

# ============= AUTRES MODÈLES EXISTANTS =============

class Recommandation(db.Model):
    __tablename__ = 'recommandations'
    
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    recette_id = db.Column(db.Integer, db.ForeignKey('recettes.id'), nullable=False)
    score = db.Column(db.Float, default=5.0)  # Score de 0 à 10
    raison = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'recette_id': self.recette_id,
            'score': self.score,
            'raison': self.raison,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def get_swagger_model(api):
        return api.model('Recommandation', {
            'id': fields.Integer(required=True, description='ID unique de la recommandation'),
            'utilisateur_id': fields.Integer(required=True, description='ID de l\'utilisateur'),
            'recette_id': fields.Integer(required=True, description='ID de la recette recommandée'),
            'score': fields.Float(description='Score de recommandation (0-10)', example=8.5),
            'raison': fields.String(description='Raison de la recommandation'),
            'created_at': fields.DateTime(description='Date de création')
        })
    
    @staticmethod
    def get_swagger_input_model(api):
        return api.model('RecommandationInput', {
            'utilisateur_id': fields.Integer(required=True, description='ID de l\'utilisateur'),
            'recette_id': fields.Integer(required=True, description='ID de la recette'),
            'score': fields.Float(description='Score de recommandation (0-10)', example=8.5),
            'raison': fields.String(description='Raison de la recommandation', example='Correspond à vos goûts')
        })

class Menu(db.Model):
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date)
    type_repas = db.Column(db.String(50))  # Petit-déjeuner, Déjeuner, Dîner
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'date': self.date.isoformat() if self.date else None,
            'type_repas': self.type_repas,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def get_swagger_model(api):
        return api.model('Menu', {
            'id': fields.Integer(required=True, description='ID unique du menu'),
            'nom': fields.String(required=True, description='Nom du menu', example='Menu du jour'),
            'date': fields.Date(description='Date du menu'),
            'type_repas': fields.String(description='Type de repas', enum=['Petit-déjeuner', 'Déjeuner', 'Dîner']),
            'created_at': fields.DateTime(description='Date de création')
        })
    
    @staticmethod
    def get_swagger_input_model(api):
        return api.model('MenuInput', {
            'nom': fields.String(required=True, description='Nom du menu', example='Menu végétarien'),
            'date': fields.String(description='Date du menu (YYYY-MM-DD)', example='2025-06-05'),
            'type_repas': fields.String(description='Type de repas', enum=['Petit-déjeuner', 'Déjeuner', 'Dîner'], example='Déjeuner')
        })

class Buffet(db.Model):
    __tablename__ = 'buffets'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_debut = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    nb_personnes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'date_debut': self.date_debut.isoformat() if self.date_debut else None,
            'date_fin': self.date_fin.isoformat() if self.date_fin else None,
            'nb_personnes': self.nb_personnes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def get_swagger_model(api):
        return api.model('Buffet', {
            'id': fields.Integer(required=True, description='ID unique du buffet'),
            'nom': fields.String(required=True, description='Nom du buffet', example='Buffet de fête'),
            'description': fields.String(description='Description du buffet'),
            'date_debut': fields.DateTime(description='Date et heure de début'),
            'date_fin': fields.DateTime(description='Date et heure de fin'),
            'nb_personnes': fields.Integer(description='Nombre de personnes attendues'),
            'created_at': fields.DateTime(description='Date de création')
        })
    
    @staticmethod
    def get_swagger_input_model(api):
        return api.model('BuffetInput', {
            'nom': fields.String(required=True, description='Nom du buffet', example='Buffet de mariage'),
            'description': fields.String(description='Description du buffet'),
            'date_debut': fields.DateTime(description='Date et heure de début'),
            'date_fin': fields.DateTime(description='Date et heure de fin'),
            'nb_personnes': fields.Integer(description='Nombre de personnes attendues', example=50)
        })

class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    chemin = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'chemin': self.chemin,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ============= FONCTION GLOBALE POUR CRÉER TOUS LES MODÈLES SWAGGER =============

def create_swagger_models(api):
    """Créer tous les modèles Swagger pour l'API"""
    
    # Modèles de réponse générique
    message_model = api.model('Message', {
        'message': fields.String(description='Message de confirmation', example='Opération réussie'),
        'success': fields.Boolean(description='Statut de l\'opération', example=True),
        'id': fields.Integer(description='ID de l\'élément créé/modifié')
    })
    
    error_model = api.model('Error', {
        'message': fields.String(description='Message d\'erreur'),
        'error': fields.String(description='Type d\'erreur'),
        'status_code': fields.Integer(description='Code de statut HTTP')
    })
    
    return {
        # ============= MODÈLES DE SORTIE =============
        'utilisateur': Utilisateur.get_swagger_model(api),
        'aliment': Aliment.get_swagger_model(api),
        'recette': Recette.get_swagger_model(api),
        'allergie': Allergie.get_swagger_model(api),
        'recommandation': Recommandation.get_swagger_model(api),
        'menu': Menu.get_swagger_model(api),
        'buffet': Buffet.get_swagger_model(api),
        'categorie': Categorie.get_swagger_model(api),
        'reaction_allergique': ReactionAllergique.get_swagger_model(api),
        'allergie_utilisateur': AllergieUtilisateur.get_swagger_model(api),
        
        # ============= MODÈLES D'ENTRÉE =============
        'utilisateur_input': Utilisateur.get_swagger_input_model(api),
        'aliment_input': Aliment.get_swagger_input_model(api),
        'recette_input': Recette.get_swagger_input_model(api),
        'allergie_input': Allergie.get_swagger_input_model(api),
        'recommandation_input': Recommandation.get_swagger_input_model(api),
        'menu_input': Menu.get_swagger_input_model(api),
        'buffet_input': Buffet.get_swagger_input_model(api),
        'categorie_input': Categorie.get_swagger_input_model(api),
        'reaction_allergique_input': ReactionAllergique.get_swagger_input_model(api),
        'allergie_utilisateur_input': AllergieUtilisateur.get_swagger_input_model(api),
        
        # ============= MODÈLES DE RÉPONSE =============
        'message': message_model,
        'error': error_model
    }