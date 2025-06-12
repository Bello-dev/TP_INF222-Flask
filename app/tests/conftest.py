import pytest
from run import create_app  # Assure-toi que run.py existe et exporte create_app
from app.model import db

@pytest.fixture
def app():
    """Fixture pour l'application Flask avec API Swagger"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def test_client(app):
    """Fixture pour le client de test"""
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Fixture pour la session de base de données"""
    with app.app_context():
        yield db.session