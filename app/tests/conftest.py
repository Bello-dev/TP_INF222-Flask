import pytest
from app.app import create_app
from app.db.db import db

TEST_DATABASE_URI = (
    "postgresql://tp222_flask:INF222@localhost:5432/aliments_test_db"
)

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI

    with app.app_context():
        db.drop_all()       # Nettoyage avant test
        db.create_all()     # Création des tables pour les tests

        yield app.test_client()  # ⚠️ ici, on fournit un client Flask de test

        db.session.remove()
        db.drop_all()       # Nettoyage après les tests
