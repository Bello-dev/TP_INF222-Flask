from app.model import db, Utilisateur, Aliment, Recette, Menu, Buffet, Recommandation, Allergie, Categorie, ReactionAllergique, AllergieUtilisateur
from run import create_app

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
        categories = [
            Categorie(nom='Fruits', description='Fruits frais et secs'),
            Categorie(nom='Légumes', description='Légumes verts et autres'),
            Categorie(nom='Céréales', description='Céréales et féculents'),
            Categorie(nom='Protéines', description='Viandes, poissons, œufs'),
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
                description='Fruit rouge ou vert, riche en fibres',
                calories=52,
                proteines=0.3,
                glucides=14,
                lipides=0.2,
                fibres=2.4,
                type_aliment='Fruit',
                categorie_id=1
            ),
            Aliment(
                nom='Brocoli',
                description='Légume vert riche en vitamines',
                calories=34,
                proteines=2.8,
                glucides=7,
                lipides=0.4,
                fibres=2.6,
                type_aliment='Légume',
                categorie_id=2
            ),
            Aliment(
                nom='Riz complet',
                description='Céréale complète nutritive',
                calories=111,
                proteines=2.6,
                glucides=23,
                lipides=0.9,
                fibres=1.8,
                type_aliment='Céréale',
                categorie_id=3
            ),
            Aliment(
                nom='Poulet',
                description='Viande blanche riche en protéines',
                calories=165,
                proteines=31,
                glucides=0,
                lipides=3.6,
                fibres=0,
                type_aliment='Protéine',
                categorie_id=4
            ),
            Aliment(
                nom='Yaourt nature',
                description='Produit laitier fermenté',
                calories=59,
                proteines=10,
                glucides=3.6,
                lipides=0.4,
                fibres=0,
                type_aliment='Produit laitier',
                categorie_id=5
            ),
            # Aliments allergènes
            Aliment(
                nom='Arachides',
                description='Fruits à coque, allergène majeur',
                calories=567,
                proteines=25.8,
                glucides=16.1,
                lipides=49.2,
                fibres=8.5,
                type_aliment='Fruit à coque',
                categorie_id=4
            ),
            Aliment(
                nom='Lait de vache',
                description='Produit laitier, peut causer des intolérances',
                calories=42,
                proteines=3.4,
                glucides=5.0,
                lipides=1.0,
                fibres=0,
                type_aliment='Produit laitier',
                categorie_id=5
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
                description='Une délicieuse salade de fruits frais',
                instructions='Couper les fruits et mélanger délicatement',
                temps_preparation=15,
                difficulte='Facile',
                portions=4
            ),
            Recette(
                nom='Riz aux légumes',
                description='Riz complet sauté avec légumes de saison',
                instructions='Faire cuire le riz, sauté les légumes, mélanger',
                temps_preparation=30,
                difficulte='Moyen',
                portions=2
            ),
            Recette(
                nom='Salade de brocolis',
                description='Salade de brocolis croquants',
                instructions='Blanchir les brocolis, assaisonner',
                temps_preparation=20,
                difficulte='Facile',
                portions=3
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
            ),
            Utilisateur(
                nom='Durand',
                prenom='Pierre',
                email='pierre.durand@example.com',
                age=35,
                poids=80,
                taille=175
            )
        ]
        
        for utilisateur in utilisateurs:
            utilisateur.set_password('password123')
            db.session.add(utilisateur)
        db.session.commit()
        print(f"✅ {len(utilisateurs)} utilisateurs ajoutés")
        
        # Créer des menus de test
        from datetime import date, timedelta
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
            ),
            Menu(
                nom='Dîner léger',
                date=date.today() + timedelta(days=1),
                type_repas='Dîner'
            )
        ]
        
        for menu in menus:
            db.session.add(menu)
        db.session.commit()
        print(f"✅ {len(menus)} menus ajoutés")
        
        # Créer des allergies de référence
        allergies = [
            Allergie(
                nom='Arachides',
                description='Allergie aux cacahuètes et dérivés',
                gravite='Sévère'
            ),
            Allergie(
                nom='Gluten',
                description='Intolérance au gluten',
                gravite='Modéré'
            ),
            Allergie(
                nom='Lactose',
                description='Intolérance au lactose',
                gravite='Léger'
            )
        ]
        
        for allergie in allergies:
            db.session.add(allergie)
        db.session.commit()
        print(f"✅ {len(allergies)} allergies ajoutées")
        
        # Créer des exemples de réactions allergiques
        reactions_test = [
            # Jean Dupont - allergique aux arachides (50% de probabilité)
            ReactionAllergique(
                utilisateur_id=1,
                aliment_id=6,  # Arachides
                times_eaten=10,
                times_reacted=5
            ),
            # Marie Martin - pas allergique aux pommes (10% de probabilité)
            ReactionAllergique(
                utilisateur_id=2,
                aliment_id=1,  # Pomme
                times_eaten=20,
                times_reacted=2
            ),
            # Pierre Durand - allergique au lait (40% de probabilité)
            ReactionAllergique(
                utilisateur_id=3,
                aliment_id=7,  # Lait de vache
                times_eaten=15,
                times_reacted=6
            )
        ]
        
        for reaction in reactions_test:
            db.session.add(reaction)
        db.session.commit()
        print(f"✅ {len(reactions_test)} réactions allergiques de test ajoutées")
        
        # Simuler l'ajout automatique d'allergies pour les cas > 30%
        for reaction in reactions_test:
            if reaction.is_allergic():
                # Déterminer le nom de l'allergie
                aliment = Aliment.query.get(reaction.aliment_id)
                nom_allergie = f"Allergie à {aliment.nom}"
                
                # Créer l'allergie si elle n'existe pas
                allergie = Allergie.query.filter_by(nom=nom_allergie).first()
                if not allergie:
                    allergie = Allergie(
                        nom=nom_allergie,
                        description=f"Allergie détectée automatiquement (probabilité: {reaction.probabilite_allergie():.1f}%)",
                        gravite='Modéré'
                    )
                    db.session.add(allergie)
                    db.session.flush()
                
                # Ajouter à l'utilisateur
                allergie_utilisateur = AllergieUtilisateur(
                    utilisateur_id=reaction.utilisateur_id,
                    allergie_id=allergie.id,
                    gravite_personnelle='Modéré',
                    detectee_automatiquement=True
                )
                db.session.add(allergie_utilisateur)
        
        db.session.commit()
        print("✅ Allergies automatiques ajoutées")
        
        print("🎉 Seeding terminé avec succès !")
        print("\n📊 RÉSUMÉ :")
        print(f"• {len(categories)} catégories")
        print(f"• {len(aliments)} aliments")
        print(f"• {len(recettes)} recettes")
        print(f"• {len(utilisateurs)} utilisateurs")
        print(f"• {len(menus)} menus")
        print(f"• {len(allergies)} allergies de référence")
        print(f"• {len(reactions_test)} réactions allergiques de test")
        
        # Afficher les probabilités d'allergies
        print("\n🧪 PROBABILITÉS D'ALLERGIES :")
        for reaction in reactions_test:
            aliment = Aliment.query.get(reaction.aliment_id)
            utilisateur = Utilisateur.query.get(reaction.utilisateur_id)
            print(f"• {utilisateur.prenom} {utilisateur.nom} - {aliment.nom}: {reaction.probabilite_allergie():.1f}% ({'ALLERGIQUE' if reaction.is_allergic() else 'OK'})")

if __name__ == '__main__':
    seed_all()