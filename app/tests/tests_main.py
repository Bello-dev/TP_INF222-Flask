import pytest
from app.model import db, Utilisateur, Aliment, Categorie, Recette, Menu, Buffet, Recommandation

def test_create_user(test_client):
    response = test_client.post('/utilisateurs', json={
        'nom': 'Test User',
        'email': 'testuser@example.com',
        'mot_de_passe': 'testpass'
    })
    assert response.status_code == 201
    assert 'Utilisateur créé' in response.json['message']

def test_get_users(test_client):
    response = test_client.get('/utilisateurs')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_aliment(test_client):
    response = test_client.post('/aliments', json={
        'nom': 'Banane',
        'calories': 89,
        'proteines': 1.1,
        'glucides': 22.8,
        'lipides': 0.3,
        'type_aliment': 'fruit'
    })
    assert response.status_code == 201
    assert 'Aliment créé' in response.json['message']

def test_get_aliments(test_client):
    response = test_client.get('/aliments')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_categorie(test_client):
    response = test_client.post('/categories/', json={'nom': 'Fruits'})
    assert response.status_code == 200 or response.status_code == 201

def test_get_categories(test_client):
    response = test_client.get('/categories/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_recette(test_client):
    # Attention : les ID doivent exister
    response = test_client.post('/recettes', json={
        'nom': 'Salade simple',
        'instructions': 'Mélanger légumes et sauce.',
        'duree': 10
    })
    assert response.status_code in [200, 201]

def test_create_menu(test_client):
    # Crée un utilisateur et une recette avant
    u = Utilisateur(nom='MenuUser', email='menu@example.com', mot_de_passe='pass')
    r = Recette(nom='Test Recette', instructions='Test instr.', duree=10)
    db.session.add_all([u, r])
    db.session.commit()

    response = test_client.post('/menu', json={
        'utilisateur_id': u.id,
        'jour': 'Mercredi',
        'recette_id': r.id
    })
    assert response.status_code in [200, 201]

def test_create_buffet(test_client):
    # Crée une recette
    r = Recette(nom='Buffet Recette', instructions='Cuire.', duree=20)
    db.session.add(r)
    db.session.commit()

    response = test_client.post('/buffets', json={
        'evenement': 'Mariage',
        'date': '2025-08-12',
        'lieu': 'Douala',
        'recette_ids': [r.id]
    })
    assert response.status_code == 201 or response.status_code == 200

def test_create_recommandation(test_client):
    # Crée un utilisateur
    u = Utilisateur(nom='RecUser', email='rec@example.com', mot_de_passe='pass')
    db.session.add(u)
    db.session.commit()

    response = test_client.post('/recommandations', json={
        'utilisateur_id': u.id,
        'type_regime': 'sans gluten',
        'aliments_recommandes': 'Carotte',
        'aliments_interdits': 'Pain',
        'allergenes': 'gluten',
        'preferences': 'léger'
    })
    assert response.status_code in [200, 201]
