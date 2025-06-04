from app.model import db, Utilisateur, Aliment, Recette, Menu, Buffet, Recommandation, Allergie, RecetteAliment
from app.app import create_app

app = create_app()

def seed_all():
    print("📥 Suppression des anciennes données...")
    
    # Supprimer dans l'ordre CORRECT des dépendances (tables dépendantes d'abord)
    db.session.query(Menu).delete()
    db.session.query(RecetteAliment).delete()
    db.session.query(Recommandation).delete()  # AVANT Utilisateur !
    
    # Supprimer les associations many-to-many
    db.session.execute(db.text("DELETE FROM buffet_recette"))
    db.session.execute(db.text("DELETE FROM aliment_allergie"))
    
    db.session.query(Buffet).delete()
    db.session.query(Recette).delete()
    db.session.query(Aliment).delete()
    db.session.query(Utilisateur).delete()  # APRÈS Recommandation !
    db.session.query(Allergie).delete()
    db.session.commit()
    
    print("📥 Réinitialisation des séquences...")
    # Réinitialiser les séquences pour avoir des IDs à partir de 1
    sequences = [
        'utilisateurs_id_seq',
        'aliments_id_seq', 
        'recettes_id_seq',
        'allergies_id_seq',
        'recommandations_id_seq',
        'menus_id_seq',
        'buffets_id_seq'
    ]
    
    for seq_name in sequences:
        try:
            db.session.execute(db.text(f"ALTER SEQUENCE {seq_name} RESTART WITH 1"))
            db.session.commit()  # ← COMMIT après chaque séquence
            print(f"   ✅ Séquence {seq_name} réinitialisée")
        except Exception as e:
            db.session.rollback()  # ← ROLLBACK en cas d'erreur
            print(f"   ⚠️  Séquence {seq_name} non trouvée: {e}")

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
    pomme = Aliment(nom='Pomme', calories=52, proteines=0.3, glucides=14, lipides=0.2, type_aliment='fruit')
    pain = Aliment(nom='Pain', calories=265, proteines=9, glucides=49, lipides=3.2, type_aliment='féculent')
    lait = Aliment(nom='Lait', calories=42, proteines=3.4, glucides=5, lipides=1, type_aliment='produit laitier')
    carotte = Aliment(nom='Carotte', calories=41, proteines=0.9, glucides=10, lipides=0.2, type_aliment='légume')
    poulet = Aliment(nom='Poulet rôti', calories=165, proteines=31, glucides=0, lipides=3.6, type_aliment='viande')
    
    db.session.add_all([pomme, pain, lait, carotte, poulet])
    db.session.commit()

    # 3.1 Associer les allergies aux aliments
    pain.allergies.append(gluten)
    lait.allergies.append(lactose)
    db.session.commit()

    # 4. Recettes (plus de variété)
    r1 = Recette(nom='Salade de carottes', instructions='Râper les carottes, ajouter du citron.', duree=10)
    r2 = Recette(nom='Poulet rôti au four', instructions='Cuire le poulet avec des épices au four.', duree=60)
    r3 = Recette(nom='Salade de fruits', instructions='Couper les pommes, mélanger.', duree=5)
    r4 = Recette(nom='Soupe de carotte', instructions='Faire bouillir les carottes, mixer.', duree=30)

    db.session.add_all([r1, r2, r3, r4])
    db.session.commit()

    # 4.1 Associer plus d'aliments aux recettes
    ra1 = RecetteAliment(recette_id=r1.id, aliment_id=carotte.id, quantite=150.0)
    ra2 = RecetteAliment(recette_id=r1.id, aliment_id=pomme.id, quantite=50.0)
    ra3 = RecetteAliment(recette_id=r2.id, aliment_id=poulet.id, quantite=200.0)
    ra4 = RecetteAliment(recette_id=r3.id, aliment_id=pomme.id, quantite=200.0)  # Salade de fruits
    ra5 = RecetteAliment(recette_id=r4.id, aliment_id=carotte.id, quantite=300.0)  # Soupe

    db.session.add_all([ra1, ra2, ra3, ra4, ra5])
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

    # 7. Recommandations
    rec1 = Recommandation(
        utilisateur_id=u1.id,
        type_regime='végétarien',
        aliments_recommandes='Pomme, Carotte',
        aliments_interdits='Poulet rôti',
        allergenes='gluten, lactose',
        preferences='repas rapide'
    )
    
    rec2 = Recommandation(
        utilisateur_id=u2.id,
        type_regime='omnivore',
        aliments_recommandes='Poulet, Carotte',
        aliments_interdits='',
        allergenes='',
        preferences='repas consistant'
    )
    
    db.session.add_all([rec1, rec2])
    db.session.commit()

    print("✅ Base de données peuplée avec succès.")
    print(f"   - 2 utilisateurs créés")
    print(f"   - 2 allergies créées")
    print(f"   - 5 aliments créés")
    print(f"   - 4 recettes créées")
    print(f"   - 5 associations recette-aliment créées")
    print(f"   - 2 recommandations créées")

if __name__ == '__main__':
    with app.app_context():
        seed_all()