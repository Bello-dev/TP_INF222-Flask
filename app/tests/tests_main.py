import pytest
from datetime import date, datetime
from app.model import (
    db, Utilisateur, Aliment, Categorie, Recette, Menu, Buffet, 
    Recommandation, Allergie, ReactionAllergique, AllergieUtilisateur
)

# ============= TESTS DES MODÈLES DE BASE =============

def test_create_user(test_client):
    """Test de création d'un utilisateur"""
    response = test_client.post('/api/utilisateurs', json={
        'nom': 'Dupont',
        'prenom': 'Jean',
        'email': 'jean.dupont@test.com',
        'age': 30,
        'poids': 75.0,
        'taille': 180.0
        # Retire 'mot_de_passe' - utilise set_password() séparément
    })
    assert response.status_code in [200, 201]

def test_get_users(test_client):
    """Test de récupération des utilisateurs"""
    response = test_client.get('/api/utilisateurs')
    assert response.status_code == 200

def test_user_model_creation():
    """Test de création directe du modèle Utilisateur"""
    user = Utilisateur(
        nom='Martin',
        prenom='Marie', 
        email='marie.martin@test.com',
        age=25,
        poids=60.0,
        taille=165.0
    )
    user.set_password('password123')  # Utilise la méthode
    
    assert user.nom == 'Martin'
    assert user.prenom == 'Marie'
    assert user.email == 'marie.martin@test.com'
    assert user.check_password('password123') is True
    assert user.check_password('wrongpassword') is False

def test_create_categorie(test_client):
    """Test de création d'une catégorie"""
    response = test_client.post('/api/categories', json={
        'nom': 'Fruits',
        'description': 'Fruits frais et secs'
    })
    assert response.status_code in [200, 201]

def test_get_categories(test_client):
    """Test de récupération des catégories"""
    response = test_client.get('/api/categories')
    assert response.status_code == 200

def test_categorie_model_creation(db_session):
    """Test de création directe du modèle Categorie"""
    categorie = Categorie(
        nom='Légumes',
        description='Légumes verts et colorés'
    )
    db_session.add(categorie)
    db_session.commit()
    
    assert categorie.id is not None
    assert categorie.nom == 'Légumes'
    assert categorie.description == 'Légumes verts et colorés'

def test_create_aliment(test_client):
    """Test de création d'un aliment"""
    # Créer d'abord une catégorie
    cat_response = test_client.post('/api/categories', json={
        'nom': 'Fruits',
        'description': 'Fruits frais'
    })
    
    response = test_client.post('/api/aliments', json={
        'nom': 'Banane',
        'description': 'Fruit jaune riche en potassium',
        'calories': 89.0,
        'proteines': 1.1,
        'glucides': 22.8,
        'lipides': 0.3,
        'fibres': 2.6,
        'type_aliment': 'fruit',
        'categorie_id': 1
    })
    assert response.status_code in [200, 201]

def test_get_aliments(test_client):
    """Test de récupération des aliments"""
    response = test_client.get('/api/aliments')
    assert response.status_code == 200

def test_aliment_model_creation(db_session):
    """Test de création directe du modèle Aliment"""
    categorie = Categorie(nom='Fruits', description='Fruits frais')
    db_session.add(categorie)
    db_session.flush()
    
    aliment = Aliment(
        nom='Pomme',
        description='Fruit rouge ou vert',
        calories=52.0,
        proteines=0.3,
        glucides=14.0,
        lipides=0.2,
        fibres=2.4,
        type_aliment='fruit',
        categorie_id=categorie.id
    )
    db_session.add(aliment)
    db_session.commit()
    
    assert aliment.id is not None
    assert aliment.nom == 'Pomme'
    assert aliment.calories == 52.0

def test_create_recette(test_client):
    """Test de création d'une recette"""
    response = test_client.post('/api/recettes', json={
        'nom': 'Salade de fruits',
        'description': 'Une délicieuse salade de fruits frais',
        'instructions': 'Couper les fruits et mélanger délicatement',
        'temps_preparation': 15,  # Pas 'duree' mais 'temps_preparation'
        'difficulte': 'Facile',
        'portions': 4
    })
    assert response.status_code in [200, 201]

def test_get_recettes(test_client):
    """Test de récupération des recettes"""
    response = test_client.get('/api/recettes')
    assert response.status_code == 200

def test_recette_model_creation(db_session):
    """Test de création directe du modèle Recette"""
    recette = Recette(
        nom='Riz aux légumes',
        description='Riz complet sauté avec légumes',
        instructions='Faire cuire le riz, sauté les légumes, mélanger',
        temps_preparation=30,  # Pas 'duree'
        difficulte='Moyen',
        portions=2
    )
    db_session.add(recette)
    db_session.commit()
    
    assert recette.id is not None
    assert recette.nom == 'Riz aux légumes'
    assert recette.temps_preparation == 30
    assert recette.difficulte == 'Moyen'

def test_create_menu(test_client):
    """Test de création d'un menu"""
    response = test_client.post('/api/menus', json={
        'nom': 'Menu du jour',
        'date': '2025-06-12',
        'type_repas': 'Déjeuner'
    })
    assert response.status_code in [200, 201]

def test_menu_model_creation(db_session):
    """Test de création directe du modèle Menu"""
    menu = Menu(
        nom='Menu équilibré',
        date=date.today(),
        type_repas='Dîner'
    )
    db_session.add(menu)
    db_session.commit()
    
    assert menu.id is not None
    assert menu.nom == 'Menu équilibré'
    assert menu.type_repas == 'Dîner'

def test_create_buffet(test_client):
    """Test de création d'un buffet"""
    response = test_client.post('/api/buffets', json={
        'nom': 'Buffet de mariage',
        'description': 'Buffet pour 100 personnes',
        'date_debut': '2025-08-15T18:00:00',
        'date_fin': '2025-08-15T23:00:00',
        'nb_personnes': 100
    })
    assert response.status_code in [200, 201]

def test_buffet_model_creation(db_session):
    """Test de création directe du modèle Buffet"""
    buffet = Buffet(
        nom='Buffet anniversaire',
        description='Buffet pour fête d\'anniversaire',
        date_debut=datetime(2025, 7, 20, 19, 0),
        date_fin=datetime(2025, 7, 20, 23, 0),
        nb_personnes=50
    )
    db_session.add(buffet)
    db_session.commit()
    
    assert buffet.id is not None
    assert buffet.nom == 'Buffet anniversaire'
    assert buffet.nb_personnes == 50

# ============= TESTS DES ALLERGIES =============

def test_create_allergie(test_client):
    """Test de création d'une allergie"""
    response = test_client.post('/api/allergies', json={
        'nom': 'Arachides',
        'description': 'Allergie aux cacahuètes et dérivés',
        'gravite': 'Sévère'
    })
    assert response.status_code in [200, 201]

def test_allergie_model_creation(db_session):
    """Test de création directe du modèle Allergie"""
    allergie = Allergie(
        nom='Gluten',
        description='Intolérance au gluten',
        gravite='Modéré'
    )
    db_session.add(allergie)
    db_session.commit()
    
    assert allergie.id is not None
    assert allergie.nom == 'Gluten'
    assert allergie.gravite == 'Modéré'

def test_reaction_allergique_model_creation(db_session):
    """Test de création directe du modèle ReactionAllergique"""
    user = Utilisateur(
        nom='Test',
        prenom='User',
        email='test@example.com',
        age=30
    )
    user.set_password('password')
    
    categorie = Categorie(nom='Test', description='Test category')
    db_session.add_all([user, categorie])
    db_session.flush()
    
    aliment = Aliment(
        nom='Test Aliment',
        calories=100,
        categorie_id=categorie.id
    )
    db_session.add(aliment)
    db_session.flush()
    
    reaction = ReactionAllergique(
        utilisateur_id=user.id,
        aliment_id=aliment.id,
        times_eaten=10,
        times_reacted=4
    )
    db_session.add(reaction)
    db_session.commit()
    
    assert reaction.id is not None
    assert reaction.times_eaten == 10
    assert reaction.times_reacted == 4
    assert reaction.probabilite_allergie() == 40.0
    assert reaction.is_allergic() is True

def test_reaction_allergique_probabilite():
    """Test du calcul de probabilité d'allergie"""
    reaction_allergique = ReactionAllergique(
        utilisateur_id=1,
        aliment_id=1,
        times_eaten=10,
        times_reacted=4
    )
    assert reaction_allergique.probabilite_allergie() == 40.0
    assert reaction_allergique.is_allergic() is True
    
    reaction_normale = ReactionAllergique(
        utilisateur_id=1,
        aliment_id=2,
        times_eaten=20,
        times_reacted=2
    )
    assert reaction_normale.probabilite_allergie() == 10.0
    assert reaction_normale.is_allergic() is False

def test_allergie_utilisateur_model_creation(db_session):
    """Test de création directe du modèle AllergieUtilisateur"""
    user = Utilisateur(
        nom='Allergique',
        prenom='User',
        email='allergique@example.com',
        age=25
    )
    user.set_password('password')
    
    allergie = Allergie(
        nom='Lactose',
        description='Intolérance au lactose',
        gravite='Léger'
    )
    
    db_session.add_all([user, allergie])
    db_session.flush()
    
    allergie_user = AllergieUtilisateur(
        utilisateur_id=user.id,
        allergie_id=allergie.id,
        gravite_personnelle='Modéré',
        detectee_automatiquement=True
    )
    db_session.add(allergie_user)
    db_session.commit()
    
    assert allergie_user.id is not None
    assert allergie_user.detectee_automatiquement is True

def test_create_reaction_allergique_via_api(test_client, db_session):
    """Test de création d'une réaction allergique via l'API"""
    # Créer un utilisateur et un aliment d'abord
    user = Utilisateur(
        nom='TestAPI',
        prenom='User',
        email='testapi@example.com',
        age=30
    )
    user.set_password('password')
    
    categorie = Categorie(nom='Test API', description='Test category')
    db_session.add_all([user, categorie])
    db_session.flush()
    
    aliment = Aliment(
        nom='Aliment API Test',
        calories=50,
        categorie_id=categorie.id
    )
    db_session.add(aliment)
    db_session.commit()
    
    # Tester l'API de réaction allergique
    response = test_client.post('/api/allergie-reactions/reaction', json={
        'utilisateur_id': user.id,
        'aliment_id': aliment.id,
        'times_eaten': 8,
        'times_reacted': 3
    })
    assert response.status_code == 200
    
    # Vérifier que la probabilité est calculée
    data = response.get_json()
    assert 'probabilite_allergie' in data
    assert data['probabilite_allergie'] == 37.5  # 3/8 * 100
    assert data['is_allergic'] is True  # 37.5% > 30%

def test_check_allergie_via_api(test_client, db_session):
    """Test de vérification d'allergie via l'API"""
    # Créer les données de test
    user = Utilisateur(
        nom='CheckAPI',
        prenom='User',
        email='checkapi@example.com',
        age=30
    )
    user.set_password('password')
    
    categorie = Categorie(nom='Check API', description='Check category')
    db_session.add_all([user, categorie])
    db_session.flush()
    
    aliment = Aliment(
        nom='Aliment Check Test',
        calories=80,
        categorie_id=categorie.id
    )
    db_session.add(aliment)
    db_session.flush()
    
    # Créer une réaction allergique
    reaction = ReactionAllergique(
        utilisateur_id=user.id,
        aliment_id=aliment.id,
        times_eaten=15,
        times_reacted=6
    )
    db_session.add(reaction)
    db_session.commit()
    
    # Tester l'API de vérification
    response = test_client.get(f'/api/allergie-reactions/check/{user.id}/{aliment.id}')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['is_allergic'] is True  # 40% > 30%
    assert data['probabilite_allergie'] == 40.0

def test_create_recommandation(db_session):
    """Test de création d'une recommandation"""
    user = Utilisateur(
        nom='Recommand',
        prenom='User',
        email='recommand@example.com',
        age=28
    )
    user.set_password('password')
    
    recette = Recette(
        nom='Recette recommandée',
        instructions='Instructions test',
        temps_preparation=20,
        difficulte='Facile',
        portions=2
    )
    
    db_session.add_all([user, recette])
    db_session.flush()
    
    recommandation = Recommandation(
        utilisateur_id=user.id,
        recette_id=recette.id,
        score=8.5,
        raison='Correspond à vos goûts'
    )
    db_session.add(recommandation)
    db_session.commit()
    
    assert recommandation.id is not None
    assert recommandation.score == 8.5
    assert recommandation.raison == 'Correspond à vos goûts'

# ============= TESTS DE VALIDATION =============

def test_to_dict_methods():
    """Test des méthodes to_dict() de tous les modèles"""
    user = Utilisateur(nom='Dict', prenom='Test', email='dict@test.com', age=25)
    user_dict = user.to_dict()
    assert 'nom' in user_dict
    assert 'email' in user_dict
    assert user_dict['nom'] == 'Dict'
    
    aliment = Aliment(nom='Test Aliment', calories=100)
    aliment_dict = aliment.to_dict()
    assert 'nom' in aliment_dict
    assert 'calories' in aliment_dict
    assert aliment_dict['calories'] == 100
    
    reaction = ReactionAllergique(
        utilisateur_id=1,
        aliment_id=1,
        times_eaten=10,
        times_reacted=3
    )
    reaction_dict = reaction.to_dict()
    assert 'probabilite_allergie' in reaction_dict
    assert 'is_allergic' in reaction_dict
    assert reaction_dict['probabilite_allergie'] == 30.0
    assert reaction_dict['is_allergic'] is False

def test_workflow_detection_allergie_complete(db_session):
    """Test du workflow complet de détection d'allergie"""
    user = Utilisateur(
        nom='Workflow',
        prenom='Test',
        email='workflow@example.com',
        age=35
    )
    user.set_password('password')
    
    categorie = Categorie(nom='Workflow Cat', description='Test')
    db_session.add_all([user, categorie])
    db_session.flush()
    
    aliment = Aliment(
        nom='Aliment Workflow',
        calories=100,
        categorie_id=categorie.id
    )
    db_session.add(aliment)
    db_session.flush()
    
    reaction = ReactionAllergique(
        utilisateur_id=user.id,
        aliment_id=aliment.id,
        times_eaten=12,
        times_reacted=5  # 41.67% > 30%
    )
    db_session.add(reaction)
    db_session.commit()
    
    assert reaction.is_allergic() is True
    assert reaction.probabilite_allergie() > 30

def test_stats_allergies_utilisateur(db_session):
    """Test des statistiques d'allergies pour un utilisateur"""
    user = Utilisateur(
        nom='Stats',
        prenom='User',
        email='stats@example.com',
        age=30
    )
    user.set_password('password')
    
    categorie = Categorie(nom='Stats Cat', description='Test')
    db_session.add_all([user, categorie])
    db_session.flush()
    
    # Créer plusieurs aliments et réactions
    aliments_reactions = [
        ('Aliment 1', 10, 5),  # 50% - allergique
        ('Aliment 2', 20, 2),  # 10% - pas allergique
        ('Aliment 3', 15, 6),  # 40% - allergique
    ]
    
    reactions = []
    for nom_aliment, times_eaten, times_reacted in aliments_reactions:
        aliment = Aliment(
            nom=nom_aliment,
            calories=100,
            categorie_id=categorie.id
        )
        db_session.add(aliment)
        db_session.flush()
        
        reaction = ReactionAllergique(
            utilisateur_id=user.id,
            aliment_id=aliment.id,
            times_eaten=times_eaten,
            times_reacted=times_reacted
        )
        reactions.append(reaction)
        db_session.add(reaction)
    
    db_session.commit()
    
    # Vérifier les statistiques
    total_reactions = len(reactions)
    allergies_detectees = [r for r in reactions if r.is_allergic()]
    
    assert total_reactions == 3
    assert len(allergies_detectees) == 2  # Aliment 1 et 3
    assert allergies_detectees[0].probabilite_allergie() == 50.0
    assert allergies_detectees[1].probabilite_allergie() == 40.0