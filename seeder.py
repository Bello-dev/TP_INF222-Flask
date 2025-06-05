from app.model import db, Utilisateur, Aliment, Recette, Menu, Buffet, Recommandation, Allergie
from run import create_app  # Utiliser le create_app principal

app = create_app()

def seed_all():
    """Peupler la base de données avec des données de test"""
    with app.app_context():
        print("🌱 Début du seeding...")
        
        # Supprimer et recréer les tables
        db.drop_all()
        db.create_all()
        print("✅ Tables recréées")
        
        # Créer des catégories
        from app.model import Categorie
        categories = [
            Categorie(nom='Fruits', description='Fruits frais et de saison'),
            Categorie(nom='Légumes', description='Légumes variés'),
            Categorie(nom='Céréales', description='Céréales et graines'),
            Categorie(nom='Protéines', description='Sources de protéines'),
            Categorie(nom='Produits laitiers', description='Lait, fromages, yaourts')
        ]
        
        for cat in categories:
            db.session.add(cat)
        db.session.commit()
        print(f"✅ {len(categories)} catégories ajoutées")
        
        # Créer des aliments de test
        aliments = [
            Aliment(
                nom='Pomme',
                description='Fruit croquant et sucré',
                calories_pour_100g=52,
                proteines=0.3,
                glucides=14,
                lipides=0.2,
                fibres=2.4,
                categorie_id=1
            ),
            Aliment(
                nom='Brocoli',
                description='Légume vert riche en vitamines',
                calories_pour_100g=34,
                proteines=2.8,
                glucides=7,
                lipides=0.4,
                fibres=2.6,
                categorie_id=2
            ),
            Aliment(
                nom='Riz complet',
                description='Céréale complète',
                calories_pour_100g=111,
                proteines=2.6,
                glucides=23,
                lipides=0.9,
                fibres=1.8,
                categorie_id=3
            )
        ]
        
        for aliment in aliments:
            db.session.add(aliment)
        db.session.commit()
        print(f"✅ {len(aliments)} aliments ajoutés")
        
        # Créer des recettes de test
        recettes = [
            Recette(
                nom='Salade de fruits',
                description='Mélange de fruits frais de saison',
                instructions='Couper les fruits et mélanger délicatement',
                temps_preparation=15,
                difficulte='Facile',
                portions=4
            ),
            Recette(
                nom='Riz aux légumes',
                description='Plat équilibré avec riz et légumes',
                instructions='Faire cuire le riz, sauté les légumes, mélanger',
                temps_preparation=30,
                difficulte='Moyen',
                portions=2
            )
        ]
        
        for recette in recettes:
            db.session.add(recette)
        db.session.commit()
        print(f"✅ {len(recettes)} recettes ajoutées")
        
        # Créer des utilisateurs de test
        utilisateurs = [
            Utilisateur(
                nom='Dupont',
                prenom='Jean',
                email='jean.dupont@example.com',
                age=30,
                poids=75,
                taille=180
            ),
            Utilisateur(
                nom='Martin',
                prenom='Marie',
                email='marie.martin@example.com',
                age=25,
                poids=60,
                taille=165
            )
        ]
        
        for utilisateur in utilisateurs:
            utilisateur.set_password('password123')
            db.session.add(utilisateur)
        db.session.commit()
        print(f"✅ {len(utilisateurs)} utilisateurs ajoutés")
        
        # Créer des menus de test
        from datetime import date
        menus = [
            Menu(
                nom='Menu équilibré du jour',
                date=date.today(),
                type_repas='Déjeuner'
            ),
            Menu(
                nom='Petit-déjeuner énergique',
                date=date.today(),
                type_repas='Petit-déjeuner'
            )
        ]
        
        for menu in menus:
            db.session.add(menu)
        db.session.commit()
        print(f"✅ {len(menus)} menus ajoutés")
        
        print("🎉 Seeding terminé avec succès !")
        print("\n📊 RÉSUMÉ :")
        print(f"• {len(categories)} catégories")
        print(f"• {len(aliments)} aliments")
        print(f"• {len(recettes)} recettes")
        print(f"• {len(utilisateurs)} utilisateurs")
        print(f"• {len(menus)} menus")

if __name__ == '__main__':
    seed_all()