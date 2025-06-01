from app.model import db, Utilisateur, Aliment, Recette, Menu, Buffet, Recommandation, Allergie
from app.app import create_app

app = create_app()

def seed_all():
    print("📥 Suppression des anciennes données...")
    db.session.query(Menu).delete()
    db.session.query(Buffet).delete()
    db.session.query(Recette).delete()
    db.session.query(Aliment).delete()
    db.session.query(Utilisateur).delete()
    db.session.query(Recommandation).delete()
    db.session.query(Allergie).delete()
    db.session.commit()

    print("📥 Insertion des données en cours...")

    # 1. Utilisateurs
    u1 = Utilisateur(nom='Alice', email='alice@mail.com', mot_de_passe='pass123')
    u2 = Utilisateur(nom='Bob', email='bob@mail.com', mot_de_passe='secret')
    db.session.add_all([u1, u2])
    db.session.commit()

    # 2. Allergies
    gluten = Allergie(nom='gluten', description='Présent dans le blé')
    lactose = Allergie(nom='lactose', description='Présent dans le lait')
    db.session.add_all([gluten, lactose])
    db.session.commit()

    # 3. Aliments
    aliments_data = [
        {'nom': 'Pomme', 'calories': 52, 'proteines': 0.3, 'glucides': 14, 'lipides': 0.2, 'type_aliment': 'fruit', 'allergies': []},
        {'nom': 'Pain', 'calories': 265, 'proteines': 9, 'glucides': 49, 'lipides': 3.2, 'type_aliment': 'féculent', 'allergies': [gluten]},
        {'nom': 'Lait', 'calories': 42, 'proteines': 3.4, 'glucides': 5, 'lipides': 1, 'type_aliment': 'produit laitier', 'allergies': [lactose]},
        {'nom': 'Carotte', 'calories': 41, 'proteines': 0.9, 'glucides': 10, 'lipides': 0.2, 'type_aliment': 'légume', 'allergies': []},
        {'nom': 'Poulet rôti', 'calories': 165, 'proteines': 31, 'glucides': 0, 'lipides': 3.6, 'type_aliment': 'viande', 'allergies': []}
    ]
    aliments = [Aliment(**data) for data in aliments_data]
    db.session.add_all(aliments)
    db.session.commit()

    # 4. Recettes
    r1 = Recette(nom='Salade de carottes', instructions='Râper les carottes, ajouter du citron.', duree=10)
    r2 = Recette(nom='Poulet rôti au four', instructions='Cuire le poulet avec des épices au four.', duree=60)
    db.session.add_all([r1, r2])
    db.session.commit()

    # 5. Menus
    m1 = Menu(utilisateur_id=u1.id, jour='Lundi', recette_id=r1.id)
    m2 = Menu(utilisateur_id=u1.id, jour='Mardi', recette_id=r2.id)
    db.session.add_all([m1, m2])
    db.session.commit()

    # 6. Buffets
    buffet = Buffet(evenement='Anniversaire', date='2025-07-10', lieu='Douala')
    buffet.recettes.extend([r1, r2])
    db.session.add(buffet)
    db.session.commit()

    # 7. Recommandation
    rec = Recommandation(
        utilisateur_id=u1.id,
        type_regime='végétarien',
        aliments_recommandes='Pomme, Carotte',
        aliments_interdits='Poulet rôti',
        allergenes='gluten, lactose',
        preferences='repas rapide'
    )
    db.session.add(rec)
    db.session.commit()

    print("✅ Base de données peuplée avec succès.")

if __name__ == '__main__':
    with app.app_context():
        seed_all()
