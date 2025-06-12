# 🍽️ TP_INF222-Flask - Système Avancé de Gestion Alimentaire

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![Swagger](https://img.shields.io/badge/API-Swagger-orange.svg)](http://localhost:5000/swagger-ui/)

> **Projet de Travaux Pratiques - Développement Backend**  
> Système intelligent de gestion des aliments, recettes et **détection automatique d'allergies** avec Intelligence Artificielle

## 🌟 Vue d'Ensemble

Ce projet est une API REST complète développée avec **Flask** pour la gestion avancée des aliments, recettes et recommandations nutritionnelles. La **fonctionnalité phare** est un système d'intelligence artificielle qui **détecte automatiquement les allergies** basé sur l'historique de consommation des utilisateurs.

### 🎯 Objectifs Pédagogiques
- Développement d'API REST avec Flask-RESTX
- Gestion de base de données relationnelle avec SQLAlchemy
- Implémentation d'algorithmes d'Intelligence Artificielle
- Containerisation avec Docker
- Documentation API avec Swagger
- Tests unitaires et d'intégration

## 🚀 Fonctionnalités Principales

### 🤖 **Système d'Allergies Avancé avec IA** ⭐ *FONCTIONNALITÉ PHARE*
- **Détection automatique d'allergies** quand probabilité >30%
- **Calcul intelligent des probabilités** basé sur l'historique
- **Vérification de risque en temps réel** pour utilisateur + aliment
- **Recommandations personnalisées** (évitement, consultation médicale)
- **Classification automatique** des niveaux de risque (FAIBLE → TRÈS ÉLEVÉ)
- **Statistiques globales** et tendances allergiques

### 🍎 **Gestion des Aliments**
- CRUD complet des aliments avec valeurs nutritionnelles
- Catégorisation automatique des aliments
- Recherche et filtrage avancés

### 🍳 **Gestion des Recettes**
- Création et modification de recettes complexes
- Calcul automatique des valeurs nutritionnelles
- Gestion des ingrédients et portions

### 👤 **Gestion des Utilisateurs**
- Profils utilisateurs avec préférences alimentaires
- Historique de consommation et réactions
- Système de recommandations personnalisées

### 🍽️ **Planification de Menus**
- Génération automatique de menus équilibrés
- Planificateur de repas intelligent
- Organisation d'événements et buffets

## 🏗️ Architecture Technique

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   Swagger UI    │◄───┤   Flask API     │◄───┤   PostgreSQL    │
│   Postman       │    │   + SQLAlchemy  │    │   + Migrations  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │              ┌─────────────────┐                │
         └──────────────┤   Docker        │────────────────┘
                        │   Compose       │
                        └─────────────────┘
```

### 🛠️ Stack Technologique
- **Backend** : Flask 2.3.3 + Flask-RESTX + SQLAlchemy
- **Base de données** : PostgreSQL 15
- **Containerisation** : Docker + Docker Compose
- **Documentation** : Swagger UI automatique
- **Tests** : Pytest + Coverage
- **IA** : Algorithmes de détection de patterns allergiques

## 📋 Prérequis

- **Docker** et **Docker Compose** installés
- **Python 3.11+** (pour développement local)
- **Git** pour cloner le projet

## 🚀 Installation et Démarrage

### 1️⃣ Cloner le Projet
```bash
git clone <votre-repo-url>
cd TP_222_Flask
```

### 2️⃣ Démarrage avec Docker (Recommandé)
```bash
# Construire et démarrer les conteneurs
docker-compose up -d --build

# Vérifier que les services sont démarrés
docker-compose ps
```

### 3️⃣ Initialiser les Données de Démonstration
```bash
# Peupler la base avec des données réalistes d'allergies
docker-compose exec web python populate_allergies_simple.py
```

### 4️⃣ Accéder à l'Application
- **🌐 API Swagger** : http://localhost:5000/swagger-ui/
- **🔗 API Base** : http://localhost:5000/api/
- **🗄️ Base de données** : PostgreSQL sur port 5432

## 📖 Documentation API Interactive

### 🎮 Interface Swagger (Recommandée)
Accédez à **http://localhost:5000/swagger-ui/** pour une interface graphique complète :

![Swagger Interface](https://via.placeholder.com/800x400/1e293b/ffffff?text=Swagger+UI+Interface)

1. **Explorez les endpoints** organisés par catégories
2. **Testez directement** dans l'interface
3. **Visualisez les schémas** de données
4. **Copiez les exemples** de requêtes

## 🧪 Guide de Test des APIs

### 🤖 **Tests du Système d'Allergies** (Fonctionnalité Phare)

#### 1. Profil Allergique Complet
```bash
# Curl
curl -X GET "http://localhost:5000/api/allergies/users/3/profile" \
     -H "accept: application/json"

# Réponse attendue
{
  "utilisateur": {
    "id": 3,
    "nom_complet": "Marie Dupont",
    "email": "marie.dupont@example.com"
  },
  "resume_allergique": {
    "total_aliments_testes": 4,
    "allergies_detectees": 1,
    "pourcentage_allergies": 25.0,
    "niveau_risque_global": "PROFIL À HAUT RISQUE"
  },
  "allergies_confirmees": [
    {
      "allergie": {"nom": "Intolérance au lactose"},
      "detectee_automatiquement": true,
      "gravite_personnelle": "Modérée"
    }
  ],
  "recommandations": [
    {
      "type": "ÉVITEMENT",
      "priorite": "HAUTE",
      "message": "Évitez les 2 aliment(s) à risque identifié(s)"
    }
  ]
}
```

#### 2. Vérification de Risque en Temps Réel
```bash
# Curl - Test Marie Dupont + Lait (risque élevé)
curl -X GET "http://localhost:5000/api/allergies/check/3/16" \
     -H "accept: application/json"

# Réponse attendue
{
  "analyse_risque": {
    "niveau_risque": "TRÈS ÉLEVÉ",
    "probabilite_allergie": 30.77,
    "recommandation": "ÉVITEMENT FORTEMENT RECOMMANDÉ",
    "allergie_confirmee": true
  },
  "historique_reactions": {
    "times_eaten": 13,
    "times_reacted": 4
  }
}
```

#### 3. Statistiques Globales
```bash
# Curl
curl -X GET "http://localhost:5000/api/allergies/statistics" \
     -H "accept: application/json"

# Réponse attendue
{
  "resume_global": {
    "total_utilisateurs": 9,
    "total_reactions_enregistrees": 19,
    "total_allergies_confirmees": 5,
    "taux_detection_auto": 100.0
  },
  "allergies_plus_frequentes": [
    {"allergie": "Intolérance au lactose", "nombre_cas": 4}
  ],
  "aliments_plus_problematiques": [
    {"aliment": "Lait", "taux_reaction_moyen": 36.08}
  ]
}
```

### 🍎 **Tests des Autres Fonctionnalités**

#### Gestion des Aliments
```bash
# Lister tous les aliments
curl -X GET "http://localhost:5000/api/aliments/" \
     -H "accept: application/json"

# Créer un nouvel aliment
curl -X POST "http://localhost:5000/api/aliments/" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "nom": "Pomme Bio",
       "description": "Pomme biologique locale",
       "calories": 52,
       "proteines": 0.3,
       "glucides": 14,
       "lipides": 0.2,
       "categorie_id": 1
     }'
```

#### Gestion des Utilisateurs
```bash
# Créer un utilisateur
curl -X POST "http://localhost:5000/api/utilisateurs/" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "nom": "Dubois",
       "prenom": "Sophie",
       "email": "sophie.dubois@example.com",
       "mot_de_passe": "motdepasse123"
     }'

# Obtenir un utilisateur
curl -X GET "http://localhost:5000/api/utilisateurs/1" \
     -H "accept: application/json"
```

## 🧪 Tests avec Postman

### 📁 Collection Postman
Importez la collection suivante dans Postman :

```json
{
  "info": {
    "name": "TP_INF222_Flask_API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Allergies - Profil Utilisateur",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5000/api/allergies/users/3/profile",
          "host": ["localhost"],
          "port": "5000",
          "path": ["api", "allergies", "users", "3", "profile"]
        }
      }
    },
    {
      "name": "Allergies - Vérification Risque",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5000/api/allergies/check/3/16",
          "host": ["localhost"],
          "port": "5000",
          "path": ["api", "allergies", "check", "3", "16"]
        }
      }
    }
  ]
}
```

### 🎯 Scénarios de Test Recommandés

1. **Test du Système d'Allergies**
   - Profil utilisateur à haut risque (ID: 3)
   - Profil utilisateur à faible risque (ID: 2)
   - Vérification risque temps réel
   - Statistiques globales

2. **Test CRUD Aliments**
   - Créer → Lire → Modifier → Supprimer

3. **Test Gestion Utilisateurs**
   - Inscription → Connexion → Profil

## 🎮 Démonstration Interactive

### 🚀 Script de Démonstration Automatique
```bash
# Lancer la démonstration complète
python demo_allergies_complete.py
```

Cette démonstration présente :
- ✅ Analyse de profils allergiques
- ✅ Détection automatique d'allergies IA
- ✅ Vérification de risques en temps réel
- ✅ Statistiques et tendances
- ✅ Recommandations personnalisées

## 📊 Endpoints API Principaux

### 🤖 Allergies (Fonctionnalité Phare)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/allergies/users/{id}/profile` | Profil allergique complet avec IA |
| `GET` | `/api/allergies/check/{user_id}/{aliment_id}` | Vérification risque temps réel |
| `GET` | `/api/allergies/statistics` | Statistiques globales et tendances |

### 🍎 Aliments
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/aliments/` | Liste tous les aliments |
| `POST` | `/api/aliments/` | Créer un nouvel aliment |
| `GET` | `/api/aliments/{id}` | Détails d'un aliment |
| `PUT` | `/api/aliments/{id}` | Modifier un aliment |
| `DELETE` | `/api/aliments/{id}` | Supprimer un aliment |

### 👤 Utilisateurs
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/utilisateurs/` | Liste tous les utilisateurs |
| `POST` | `/api/utilisateurs/` | Créer un utilisateur |
| `GET` | `/api/utilisateurs/{id}` | Profil utilisateur |
| `PUT` | `/api/utilisateurs/{id}` | Modifier un utilisateur |

### 🍳 Recettes
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/recettes/` | Liste toutes les recettes |
| `POST` | `/api/recettes/` | Créer une recette |
| `GET` | `/api/recettes/{id}` | Détails d'une recette |

## 🗄️ Structure de la Base de Données

### 📋 Modèles Principaux

```mermaid
erDiagram
    Utilisateur ||--o{ ReactionAllergique : "a des réactions"
    Utilisateur ||--o{ AllergieUtilisateur : "a des allergies"
    Aliment ||--o{ ReactionAllergique : "provoque des réactions"
    Allergie ||--o{ AllergieUtilisateur : "est attribuée à"
    Categorie ||--o{ Aliment : "contient"
    
    Utilisateur {
        int id PK
        string nom
        string prenom
        string email
        string mot_de_passe_hash
        datetime created_at
    }
    
    ReactionAllergique {
        int id PK
        int utilisateur_id FK
        int aliment_id FK
        int times_eaten
        int times_reacted
        datetime created_at
        datetime updated_at
    }
    
    AllergieUtilisateur {
        int id PK
        int utilisateur_id FK
        int allergie_id FK
        string gravite_personnelle
        boolean detectee_automatiquement
        datetime created_at
    }
```

### 🧠 Intelligence Artificielle - Algorithme de Détection

```python
def probabilite_allergie(self):
    """Calcule la probabilité d'allergie basée sur l'historique"""
    if self.times_eaten == 0:
        return 0
    return (self.times_reacted / self.times_eaten) * 100

def is_allergic(self):
    """Détection automatique d'allergie (seuil IA : 30%)"""
    return self.probabilite_allergie() > 30
```

## 🔧 Développement

### 🛠️ Installation pour Développement Local
```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Variables d'environnement
export FLASK_APP=run.py
export FLASK_ENV=development
export DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Démarrer en mode développement
flask run --debug
```

### 🧪 Exécution des Tests
```bash
# Tests unitaires
pytest app/tests/

# Tests avec couverture
pytest --cov=app --cov-report=html

# Tests spécifiques aux allergies
pytest app/tests/test_allergies.py -v
```

### 📁 Structure du Projet
```
TP_222_Flask/
├── 📄 README.md                 # Documentation complète
├── 🐳 docker-compose.yml        # Configuration Docker
├── 🐳 Dockerfile               # Image Flask
├── ⚙️ requirements.txt          # Dépendances Python
├── 🚀 run.py                    # Point d'entrée application
├── 🎮 demo_allergies_complete.py # Démonstration complète
├── 🗃️ populate_allergies_simple.py # Population données
├── 🧪 test_allergies_system.py  # Tests système allergies
├── app/
│   ├── 📱 model.py              # Modèles SQLAlchemy
│   ├── ⚙️ initialize_functions.py # Configuration blueprints
│   ├── config/
│   │   └── ⚙️ config.py         # Configuration application
│   ├── routes/
│   │   ├── 🤖 allergies_advanced.py # API allergies IA ⭐
│   │   ├── 🍎 aliments.py       # API aliments
│   │   ├── 👤 utilisateurs.py   # API utilisateurs
│   │   ├── 🍳 recettes.py       # API recettes
│   │   └── 📊 recommandations.py # API recommandations
│   └── tests/
│       ├── 🧪 test_allergies.py # Tests allergies
│       ├── 🧪 test_aliments.py  # Tests aliments
│       └── 🧪 test_utilisateurs.py # Tests utilisateurs
└── migrations/                  # Migrations base de données
```

## 🎯 Cas d'Usage Démonstrables

### 🔥 **Scénario 1 : Détection Automatique d'Allergie**
```bash
# Marie Dupont consomme du lait 13 fois et réagit 4 fois
# → Probabilité = 30.77% > 30%
# → Allergie automatiquement détectée ✅
curl -X GET "http://localhost:5000/api/allergies/users/3/profile"
```

### ⚠️ **Scénario 2 : Alerte Risque Temps Réel**
```bash
# Marie veut consommer du lait
# → Système alerte : "ÉVITEMENT FORTEMENT RECOMMANDÉ"
curl -X GET "http://localhost:5000/api/allergies/check/3/16"
```

### 📊 **Scénario 3 : Analyse Populationnelle**
```bash
# Vue d'ensemble : 100% des allergies détectées automatiquement
# Lait = aliment le plus problématique (36% de taux de réaction)
curl -X GET "http://localhost:5000/api/allergies/statistics"
```

## 🚀 Déploiement en Production

### 🐳 Docker Production
```bash
# Construction pour production
docker-compose -f docker-compose.prod.yml up -d --build

# Monitoring
docker-compose logs -f web
```

### 🔒 Sécurité
- Hashage des mots de passe avec Werkzeug
- Validation des données d'entrée
- Protection CORS configurée
- Variables d'environnement sécurisées

## 🤝 Contribution

### 📋 Guidelines
1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Commiter** les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. **Pousser** la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. **Créer** une Pull Request

### 🧪 Avant de Contribuer
```bash
# Vérifier les tests
pytest

# Vérifier le code style
flake8 app/

# Vérifier la couverture
pytest --cov=app --cov-report=term-missing
```

## 📞 Support et Contact

### 🆘 Problèmes Courants

#### Docker ne démarre pas
```bash
# Nettoyer et redémarrer
docker-compose down -v
docker-compose up -d --build
```

#### Base de données vide
```bash
# Repeupler les données
docker-compose exec web python populate_allergies_simple.py
```

#### API non accessible
```bash
# Vérifier les conteneurs
docker-compose ps
docker-compose logs web
```

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 🏆 Fonctionnalités Mises en Avant

### 🎯 **Pourquoi ce Projet se Distingue**

1. **🤖 Intelligence Artificielle Réelle**
   - Algorithme de détection automatique d'allergies
   - Seuil intelligent à 30% de probabilité
   - Classification automatique des risques

2. **📊 Analyse de Données Avancée**
   - Calculs de probabilités en temps réel
   - Statistiques populationnelles
   - Tendances et patterns allergiques

3. **🏗️ Architecture Moderne**
   - API REST avec documentation Swagger
   - Containerisation Docker complète
   - Base de données relationnelle complexe

4. **🧪 Qualité Logicielle**
   - Tests unitaires et d'intégration
   - Couverture de code
   - Documentation exhaustive

---

**🎓 Projet réalisé dans le cadre du TP INF222 - Développement Backend par Bell Aqil alias Bello-dev**  
**✨ Démonstration des compétences en développement d'API REST avancées avec Intelligence Artificielle**
