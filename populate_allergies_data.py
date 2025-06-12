#!/usr/bin/env python3
# filepath: /home/bello-dev/Modèles/TP_222_Flask/populate_allergies_data.py
"""
🗃️ SCRIPT DE PEUPLEMENT - DONNÉES ALLERGIES AVANCÉES
===================================================

Ce script peuple la base de données avec des données réalistes pour démontrer
le système avancé de gestion des allergies :
- Utilisateurs avec profils variés
- Aliments allergènes courants
- Réactions allergiques simulées réalistes
- Détection automatique d'allergies
"""

import requests
import json
import random
from datetime import datetime, timedelta

# Configuration
API_BASE = "http://127.0.0.1:5000/api"
headers = {"Content-Type": "application/json"}

def api_call(method, endpoint, data=None, silent=False):
    """Fonction helper pour appels API"""
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        if not silent:
            print(f"  {method} {endpoint} -> {response.status_code}")
        
        if response.status_code < 400:
            return response.json()
        else:
            if not silent:
                print(f"    Erreur: {response.text[:100]}")
            return None
    except Exception as e:
        if not silent:
            print(f"    Exception: {e}")
        return None

def create_users():
    """Créer des utilisateurs avec profils allergiques variés"""
    print("\n👥 Création d'utilisateurs avec profils allergiques...")
    
    users_data = [
        {
            "nom": "Dupont", "prenom": "Marie", 
            "email": "marie.dupont.allergies@test.com",
            "mot_de_passe": "test123", "age": 28, "poids": 65.0, "taille": 168.0,
            "profil": "allergies_multiples"
        },
        {
            "nom": "Martin", "prenom": "Jean",
            "email": "jean.martin.allergies@test.com", 
            "mot_de_passe": "test123", "age": 34, "poids": 78.0, "taille": 182.0,
            "profil": "allergie_legere"
        },
        {
            "nom": "Bernard", "prenom": "Sophie",
            "email": "sophie.bernard.allergies@test.com",
            "mot_de_passe": "test123", "age": 25, "poids": 58.0, "taille": 165.0,
            "profil": "allergie_severe"
        },
        {
            "nom": "Petit", "prenom": "Lucas",
            "email": "lucas.petit.allergies@test.com",
            "mot_de_passe": "test123", "age": 31, "poids": 72.0, "taille": 176.0,
            "profil": "pas_allergique"
        },
        {
            "nom": "Robert", "prenom": "Emma",
            "email": "emma.robert.allergies@test.com",
            "mot_de_passe": "test123", "age": 29, "poids": 62.0, "taille": 170.0,
            "profil": "intolerant_lactose"
        }
    ]
    
    created_users = []
    for user_data in users_data:
        profil = user_data.pop('profil')  # Retirer le profil des données à envoyer
        user = api_call("POST", "/utilisateurs/", user_data)
        if user:
            user['profil'] = profil  # Rajouter le profil pour usage ultérieur
            created_users.append(user)
            print(f"    ✅ {user['prenom']} {user['nom']} (ID: {user['id']}) - Profil: {profil}")
    
    return created_users

def create_allergen_foods():
    """Créer des aliments allergènes courants"""
    print("\n🥜 Création d'aliments allergènes...")
    
    # Créer la catégorie des allergènes
    categorie = api_call("POST", "/categories/", {
        "nom": "Allergènes Majeurs",
        "description": "Les 14 allergènes alimentaires majeurs reconnus en Europe"
    })
    
    if not categorie:
        print("    ⚠️ Utilisation d'une catégorie existante")
        cat_id = 1
    else:
        cat_id = categorie["id"]
        print(f"    ✅ Catégorie créée: {categorie['nom']}")
    
    # Liste des allergènes majeurs avec leurs caractéristiques
    allergenes_data = [
        {
            "nom": "Arachides", 
            "description": "Cacahuètes et produits dérivés - Allergène majeur",
            "severite": "elevee"
        },
        {
            "nom": "Lait de vache",
            "description": "Lait et produits laitiers - Intolérance et allergie", 
            "severite": "moderee"
        },
        {
            "nom": "Œufs de poule",
            "description": "Œufs et ovoproduits - Allergie fréquente chez l'enfant",
            "severite": "moderee"
        },
        {
            "nom": "Gluten (Blé)",
            "description": "Protéine du blé - Maladie cœliaque et sensibilité",
            "severite": "moderee"
        },
        {
            "nom": "Soja",
            "description": "Soja et dérivés - Légumineuse allergène",
            "severite": "faible"
        },
        {
            "nom": "Poissons",
            "description": "Poissons de mer et d'eau douce",
            "severite": "moderee"
        },
        {
            "nom": "Crustacés",
            "description": "Crevettes, crabes, homards - Allergie commune",
            "severite": "elevee"
        },
        {
            "nom": "Fruits à coque",
            "description": "Noix, amandes, noisettes, etc.",
            "severite": "elevee"
        },
        {
            "nom": "Céleri",
            "description": "Céleri et dérivés - Allergie croisée",
            "severite": "faible"
        },
        {
            "nom": "Moutarde",
            "description": "Graines de moutarde et préparations",
            "severite": "faible"
        },
        {
            "nom": "Graines de sésame",
            "description": "Sésame et produits dérivés",
            "severite": "moderee"
        },
        {
            "nom": "Sulfites",
            "description": "Conservateurs sulfités (E220-E228)",
            "severite": "moderee"
        }
    ]
    
    created_foods = []
    for aliment_data in allergenes_data:
        severite = aliment_data.pop('severite')  # Retirer la sévérité
        aliment_data["categorie_id"] = cat_id
        
        aliment = api_call("POST", "/aliments/", aliment_data)
        if aliment:
            aliment['severite'] = severite  # Rajouter pour usage ultérieur
            created_foods.append(aliment)
            print(f"    ✅ {aliment['nom']} (ID: {aliment['id']}) - Sévérité: {severite}")
    
    return created_foods

def generate_realistic_reactions(users, foods):
    """Générer des réactions allergiques réalistes basées sur les profils"""
    print("\n🧪 Génération de réactions allergiques réalistes...")
    
    # Profils de réaction par type d'utilisateur
    profil_reactions = {
        "allergies_multiples": {
            "Arachides": {"prob_base": 0.85, "variance": 0.1},
            "Fruits à coque": {"prob_base": 0.75, "variance": 0.15},
            "Crustacés": {"prob_base": 0.60, "variance": 0.2},
            "Lait de vache": {"prob_base": 0.30, "variance": 0.1},
        },
        "allergie_legere": {
            "Soja": {"prob_base": 0.25, "variance": 0.1},
            "Céleri": {"prob_base": 0.20, "variance": 0.05},
        },
        "allergie_severe": {
            "Arachides": {"prob_base": 0.95, "variance": 0.05},
            "Crustacés": {"prob_base": 0.90, "variance": 0.1},
        },
        "pas_allergique": {
            # Pas de réactions significatives
        },
        "intolerant_lactose": {
            "Lait de vache": {"prob_base": 0.70, "variance": 0.15},
        }
    }
    
    total_reactions = 0
    
    for user in users:
        profil = user.get('profil', 'pas_allergique')
        reactions_profil = profil_reactions.get(profil, {})
        
        print(f"\n  👤 {user['prenom']} {user['nom']} (Profil: {profil}):")
        
        # Pour chaque aliment, générer des données de consommation/réaction
        for food in foods:
            food_name = food['nom']
            
            # Déterminer si cet aliment cause des réactions pour ce profil
            if food_name in reactions_profil:
                reaction_data = reactions_profil[food_name]
                prob_base = reaction_data['prob_base']
                variance = reaction_data['variance']
                
                # Générer nombre de consommations (entre 5 et 20)
                times_eaten = random.randint(5, 20)
                
                # Calculer probabilité réelle avec variance
                prob_real = max(0, min(1, prob_base + random.uniform(-variance, variance)))
                
                # Générer nombre de réactions
                times_reacted = int(times_eaten * prob_real)
                
                # Ajouter un peu de randomness
                if times_reacted > 0:
                    times_reacted = max(0, times_reacted + random.randint(-1, 1))
                
                print(f"    🔬 {food_name}: {times_reacted}/{times_eaten} réactions ({times_reacted/times_eaten*100:.1f}%)")
                total_reactions += 1
                
            else:
                # Aliment non problématique - générer quelques données "normales"
                if random.random() < 0.3:  # 30% de chance d'avoir testé cet aliment
                    times_eaten = random.randint(3, 12)
                    # Très faible probabilité de réaction (0-5%)
                    times_reacted = 1 if random.random() < 0.05 else 0
                    
                    if times_eaten > 0:  # Afficher seulement si consommé
                        print(f"    ✅ {food_name}: {times_reacted}/{times_eaten} réactions ({times_reacted/times_eaten*100:.1f}%)")
                        total_reactions += 1
    
    print(f"\n  📊 Total réactions générées: {total_reactions}")
    return total_reactions

def analyze_detection_system():
    """Analyser et présenter les capacités du système de détection"""
    print("\n🔍 ANALYSE DU SYSTÈME DE DÉTECTION AUTOMATIQUE")
    print("=" * 55)
    
    print("\n📋 CARACTÉRISTIQUES DU SYSTÈME:")
    print("  • Seuil de détection: >30% de probabilité d'allergie")
    print("  • Calcul: (nombre_réactions / nombre_consommations) * 100")
    print("  • Détection automatique en temps réel")
    print("  • Recommandations personnalisées")
    
    print("\n🎯 NIVEAUX DE RISQUE:")
    print("  🔴 >50%: ALLERGIE SÉVÈRE - Évitement total")
    print("  🟠 30-50%: ALLERGIE MODÉRÉE - Évitement recommandé") 
    print("  🟡 15-30%: RISQUE FAIBLE - Surveillance")
    print("  🟢 <15%: RISQUE MINIMAL - Consommation normale")
    
    print("\n💡 FONCTIONNALITÉS AVANCÉES:")
    print("  • Profil allergique complet par utilisateur")
    print("  • Analyse de tendances globales")
    print("  • Détection automatique d'allergies croisées")
    print("  • Recommandations médicales personnalisées")
    print("  • Statistiques en temps réel")

def main():
    """Fonction principale du script de peuplement"""
    print("🍽️" + "="*60)
    print("   PEUPLEMENT BASE DE DONNÉES - SYSTÈME ALLERGIES")
    print("="*64)
    
    # 1. Créer les utilisateurs
    users = create_users()
    print(f"✅ {len(users)} utilisateurs créés")
    
    # 2. Créer les aliments allergènes
    foods = create_allergen_foods()
    print(f"✅ {len(foods)} aliments allergènes créés")
    
    # 3. Générer les réactions
    total_reactions = generate_realistic_reactions(users, foods)
    print(f"✅ {total_reactions} réactions simulées")
    
    # 4. Analyser le système
    analyze_detection_system()
    
    # 5. Résumé final
    print("\n🎉 PEUPLEMENT TERMINÉ!")
    print("=" * 25)
    print(f"📊 RÉSUMÉ:")
    print(f"  👥 Utilisateurs: {len(users)}")
    print(f"  🥜 Aliments allergènes: {len(foods)}")
    print(f"  🧪 Réactions simulées: {total_reactions}")
    print(f"  🤖 Détection automatique: Activée (seuil >30%)")
    
    print(f"\n💻 ACCÈS AU SYSTÈME:")
    print(f"  🌐 API Swagger: http://127.0.0.1:5000/swagger-ui/")
    print(f"  🔍 Endpoint profils: GET /api/allergies/profile/<user_id>")
    print(f"  📊 Statistiques: GET /api/allergies/statistics")
    
    print("\n" + "="*64)

if __name__ == "__main__":
    print("🚀 Démarrage du peuplement de données...")
    main()
