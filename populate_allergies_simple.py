#!/usr/bin/env python3
"""
🗃️ SCRIPT DE PEUPLEMENT SIMPLE - DONNÉES ALLERGIES
==================================================

Script simplifié pour peupler la base de données avec des données d'allergies
sans dépendances externes.
"""

from run import app
from app.model import (db, Utilisateur, Aliment, Categorie, Allergie, 
                      ReactionAllergique, AllergieUtilisateur)
from datetime import datetime, timedelta
import random

def populate_basic_allergies():
    """Peuple la base de données avec des données d'allergies de base"""
    
    with app.app_context():
        print("🚀 Démarrage du peuplement des données d'allergies...")
        
        # 1. Créer la catégorie allergènes si elle n'existe pas
        categorie_allergenes = Categorie.query.filter_by(nom="Allergènes").first()
        if not categorie_allergenes:
            categorie_allergenes = Categorie(
                nom="Allergènes",
                description="Aliments allergènes courants"
            )
            db.session.add(categorie_allergenes)
            db.session.commit()
            print("✅ Catégorie 'Allergènes' créée")
        
        # 2. Créer les allergènes principaux
        allergenes_data = [
            {"nom": "Arachides", "description": "Cacahuètes et dérivés"},
            {"nom": "Lait", "description": "Lactose et protéines laitières"},
            {"nom": "Oeufs", "description": "Protéines d'œuf"},
            {"nom": "Gluten", "description": "Protéines de blé, orge, seigle"},
            {"nom": "Soja", "description": "Protéines de soja"},
            {"nom": "Fruits à coque", "description": "Noix, amandes, noisettes"},
            {"nom": "Poisson", "description": "Protéines de poisson"},
            {"nom": "Crustacés", "description": "Crevettes, crabes, homards"}
        ]
        
        allergenes_crees = []
        for allergen_info in allergenes_data:
            aliment = Aliment.query.filter_by(nom=allergen_info["nom"]).first()
            if not aliment:
                aliment = Aliment(
                    nom=allergen_info["nom"],
                    description=allergen_info["description"],
                    categorie_id=categorie_allergenes.id,
                    calories=200,  # Valeur par défaut
                    proteines=10.0,
                    glucides=20.0,
                    lipides=15.0
                )
                db.session.add(aliment)
                allergenes_crees.append(aliment)
        
        db.session.commit()
        print(f"✅ {len(allergenes_crees)} aliments allergènes créés")
        
        # 3. Créer les allergies de base
        allergies_data = [
            {"nom": "Allergie aux arachides", "description": "Réaction aux cacahuètes", "gravite": "Sévère"},
            {"nom": "Intolérance au lactose", "description": "Difficulté à digérer le lactose", "gravite": "Modérée"},
            {"nom": "Allergie aux œufs", "description": "Réaction aux protéines d'œuf", "gravite": "Modérée"},
            {"nom": "Maladie cœliaque", "description": "Intolérance au gluten", "gravite": "Sévère"},
            {"nom": "Allergie au soja", "description": "Réaction aux protéines de soja", "gravite": "Modérée"}
        ]
        
        allergies_creees = []
        for allergie_info in allergies_data:
            allergie = Allergie.query.filter_by(nom=allergie_info["nom"]).first()
            if not allergie:
                allergie = Allergie(
                    nom=allergie_info["nom"],
                    description=allergie_info["description"],
                    gravite=allergie_info["gravite"]
                )
                db.session.add(allergie)
                allergies_creees.append(allergie)
        
        db.session.commit()
        print(f"✅ {len(allergies_creees)} allergies créées")
        
        # 4. Récupérer les utilisateurs existants
        utilisateurs = Utilisateur.query.limit(5).all()
        if not utilisateurs:
            print("❌ Aucun utilisateur trouvé. Veuillez d'abord créer des utilisateurs.")
            return
        
        print(f"👥 {len(utilisateurs)} utilisateurs trouvés")
        
        # 5. Récupérer les aliments allergènes
        aliments_allergenes = Aliment.query.filter_by(categorie_id=categorie_allergenes.id).all()
        print(f"🥜 {len(aliments_allergenes)} aliments allergènes disponibles")
        
        # 6. Créer des réactions allergiques réalistes
        reactions_creees = 0
        for utilisateur in utilisateurs:
            print(f"📊 Création de réactions pour {utilisateur.prenom} {utilisateur.nom}")
            
            # Chaque utilisateur teste entre 3 et 6 aliments
            aliments_testes = random.sample(aliments_allergenes, min(random.randint(3, 6), len(aliments_allergenes)))
            
            for aliment in aliments_testes:
                # Simuler des données réalistes
                times_eaten = random.randint(5, 25)
                
                # Probabilité de réaction basée sur l'aliment
                if "arachides" in aliment.nom.lower():
                    prob_reaction = 0.8  # 80% chance de réaction aux arachides
                elif "lait" in aliment.nom.lower():
                    prob_reaction = 0.4  # 40% chance de réaction au lait
                elif "gluten" in aliment.nom.lower():
                    prob_reaction = 0.3  # 30% chance de réaction au gluten
                else:
                    prob_reaction = 0.2  # 20% chance pour les autres
                
                times_reacted = 0
                for _ in range(times_eaten):
                    if random.random() < prob_reaction:
                        times_reacted += 1
                
                # Créer la réaction allergique
                reaction = ReactionAllergique(
                    utilisateur_id=utilisateur.id,
                    aliment_id=aliment.id,
                    times_eaten=times_eaten,
                    times_reacted=times_reacted,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
                    updated_at=datetime.utcnow()
                )
                
                db.session.add(reaction)
                reactions_creees += 1
                
                # Si probabilité > 30%, créer une allergie automatique
                probabilite = (times_reacted / times_eaten * 100) if times_eaten > 0 else 0
                if probabilite > 30:
                    # Trouver l'allergie correspondante
                    allergie = None
                    if "arachides" in aliment.nom.lower():
                        allergie = Allergie.query.filter_by(nom="Allergie aux arachides").first()
                    elif "lait" in aliment.nom.lower():
                        allergie = Allergie.query.filter_by(nom="Intolérance au lactose").first()
                    elif "gluten" in aliment.nom.lower():
                        allergie = Allergie.query.filter_by(nom="Maladie cœliaque").first()
                    
                    if allergie:
                        # Vérifier si l'allergie n'existe pas déjà
                        allergie_existante = AllergieUtilisateur.query.filter_by(
                            utilisateur_id=utilisateur.id,
                            allergie_id=allergie.id
                        ).first()
                        
                        if not allergie_existante:
                            allergie_utilisateur = AllergieUtilisateur(
                                utilisateur_id=utilisateur.id,
                                allergie_id=allergie.id,
                                gravite_personnelle="Sévère" if probabilite > 60 else "Modérée",
                                detectee_automatiquement=True,
                                created_at=datetime.utcnow()
                            )
                            db.session.add(allergie_utilisateur)
                            print(f"  🚨 Allergie automatiquement détectée: {allergie.nom} ({probabilite:.1f}%)")
        
        db.session.commit()
        print(f"✅ {reactions_creees} réactions allergiques créées")
        
        # 7. Afficher un résumé
        print("\n📊 RÉSUMÉ DU PEUPLEMENT:")
        print(f"👥 Utilisateurs: {len(utilisateurs)}")
        print(f"🥜 Aliments allergènes: {len(aliments_allergenes)}")
        print(f"🤧 Réactions allergiques: {reactions_creees}")
        
        allergies_utilisateur = AllergieUtilisateur.query.all()
        print(f"🚨 Allergies détectées automatiquement: {len(allergies_utilisateur)}")
        
        print("\n🎯 DONNÉES PRÊTES POUR DÉMONSTRATION!")
        print("Vous pouvez maintenant tester l'API d'allergies avancées.")

if __name__ == "__main__":
    populate_basic_allergies()
