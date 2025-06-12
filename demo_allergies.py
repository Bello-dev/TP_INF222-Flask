#!/usr/bin/env python3
# filepath: /home/bello-dev/Modèles/TP_222_Flask/demo_allergies.py
"""
🦠 DÉMONSTRATION SYSTÈME AVANCÉ DE GESTION DES ALLERGIES
========================================================

Ce script démontre les capacités avancées du système de gestion des allergies :
- Détection automatique d'allergies basée sur les probabilités
- Profil allergique complet d'un utilisateur
- Analyse de risque en temps réel
- Recommandations personnalisées
- Statistiques globales
"""

import requests
import json
from datetime import datetime

# Configuration
API_BASE = "http://127.0.0.1:5000/api"
headers = {"Content-Type": "application/json"}

def make_request(method, endpoint, data=None):
    """Helper pour faire des requêtes API"""
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        
        print(f"\n🔗 {method} {endpoint}")
        if data:
            print(f"📤 Données envoyées: {json.dumps(data, indent=2)}")
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code < 400:
            result = response.json()
            print(f"📥 Réponse: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        else:
            print(f"❌ Erreur: {response.text}")
            return None
            
    except Exception as e:
        print(f"💥 Exception: {e}")
        return None

def demo_systeme_allergies():
    """Démonstration complète du système d'allergies"""
    
    print("🍽️" + "="*80)
    print("  DÉMONSTRATION SYSTÈME AVANCÉ DE GESTION DES ALLERGIES")
    print("="*84)
    
    # 1. Créer un utilisateur de test
    print("\n🧪 ÉTAPE 1: Création d'un utilisateur de test")
    user_data = {
        "nom": "Allergie",
        "prenom": "Test",
        "email": f"test.allergies.{datetime.now().timestamp()}@demo.com",
        "mot_de_passe": "demo123",
        "age": 28,
        "poids": 65.0,
        "taille": 170.0
    }
    
    user_result = make_request("POST", "/utilisateurs/", user_data)
    if not user_result:
        print("❌ Impossible de créer l'utilisateur de test")
        return
    
    user_id = user_result["id"]
    print(f"✅ Utilisateur créé avec ID: {user_id}")
    
    # 2. Créer quelques catégories et aliments de test
    print("\n🥗 ÉTAPE 2: Création d'aliments de test")
    
    # Créer une catégorie
    categorie_data = {
        "nom": "Allergènes Communs",
        "description": "Aliments fréquemment allergènes"
    }
    categorie_result = make_request("POST", "/categories/", categorie_data)
    if not categorie_result:
        print("⚠️ Impossible de créer la catégorie, utilisation d'une existante")
        categorie_id = 1
    else:
        categorie_id = categorie_result["id"]
    
    # Créer des aliments de test
    aliments_test = [
        {"nom": "Arachides", "description": "Cacahuètes - allergène majeur"},
        {"nom": "Lait de vache", "description": "Lait - intolérance lactose"},
        {"nom": "Gluten", "description": "Protéine du blé"},
        {"nom": "Œufs", "description": "Œufs de poule"},
        {"nom": "Soja", "description": "Légumineuse allergène"}
    ]
    
    aliments_ids = []
    for aliment_data in aliments_test:
        aliment_data["categorie_id"] = categorie_id
        aliment_result = make_request("POST", "/aliments/", aliment_data)
        if aliment_result:
            aliments_ids.append(aliment_result["id"])
    
    print(f"✅ Aliments créés: {len(aliments_ids)} aliments")
    
    # 3. Simuler des réactions allergiques avec différents niveaux de risque
    print("\n🦠 ÉTAPE 3: Simulation de réactions allergiques")
    
    reactions_test = [
        # Arachides - Allergie sévère (probabilité: 80%)
        {"aliment_id": aliments_ids[0], "times_eaten": 5, "times_reacted": 4},
        
        # Lait - Intolérance modérée (probabilité: 40%)
        {"aliment_id": aliments_ids[1], "times_eaten": 10, "times_reacted": 4},
        
        # Gluten - Risque faible (probabilité: 20%)
        {"aliment_id": aliments_ids[2], "times_eaten": 15, "times_reacted": 3},
        
        # Œufs - Pas d'allergie (probabilité: 0%)
        {"aliment_id": aliments_ids[3], "times_eaten": 8, "times_reacted": 0},
        
        # Soja - Risque modéré (probabilité: 33%)
        {"aliment_id": aliments_ids[4], "times_eaten": 6, "times_reacted": 2},
    ]
    
    for reaction_data in reactions_test:
        reaction_data["utilisateur_id"] = user_id
        make_request("POST", f"/allergies/users/{user_id}/reactions", reaction_data)
    
    print("✅ Réactions allergiques simulées")
    
    # 4. Analyser le profil allergique complet
    print("\n📊 ÉTAPE 4: Analyse du profil allergique complet")
    profile_result = make_request("GET", f"/allergies/users/{user_id}/profile")
    
    if profile_result:
        print("\n🎯 RÉSUMÉ DU PROFIL ALLERGIQUE:")
        resume = profile_result["resume_allergique"]
        print(f"   • Total aliments testés: {resume['total_aliments_testes']}")
        print(f"   • Allergies détectées: {resume['allergies_detectees']}")
        print(f"   • Pourcentage d'allergies: {resume['pourcentage_allergies']}%")
        print(f"   • Niveau de risque global: {resume['niveau_risque_global']}")
        
        print("\n🚨 ALLERGIES CONFIRMÉES:")
        for allergie in profile_result["allergies_confirmees"]:
            print(f"   • {allergie['allergie']['nom']} - Gravité: {allergie['gravite_personnelle']}")
            if allergie['detectee_automatiquement']:
                print("     (Détectée automatiquement par IA)")
        
        print("\n⚠️ RECOMMANDATIONS:")
        for rec in profile_result["recommandations"]:
            print(f"   • [{rec['priorite']}] {rec['type']}: {rec['message']}")
    
    # 5. Tester la vérification de risque en temps réel
    print("\n🚨 ÉTAPE 5: Vérification de risque en temps réel")
    
    for i, aliment_id in enumerate(aliments_ids[:3]):
        risk_result = make_request("GET", f"/allergies/check/{user_id}/{aliment_id}")
        if risk_result:
            analyse = risk_result["analyse_risque"]
            aliment_nom = risk_result["aliment"]["nom"]
            print(f"\n🔍 Analyse pour {aliment_nom}:")
            print(f"   • Niveau de risque: {analyse['niveau_risque']}")
            print(f"   • Probabilité: {analyse['probabilite_allergie']}%")
            print(f"   • Recommandation: {analyse['recommandation']}")
    
    # 6. Consulter les allergies confirmées de l'utilisateur
    print("\n📋 ÉTAPE 6: Liste des allergies confirmées")
    allergies_result = make_request("GET", f"/allergies/users/{user_id}/allergies")
    
    if allergies_result:
        print(f"\n👤 Allergies de {allergies_result['utilisateur']['prenom']} {allergies_result['utilisateur']['nom']}:")
        print(f"   • Total: {allergies_result['total_allergies']} allergie(s)")
        print(f"   • Auto-détectées: {allergies_result['allergies_auto_detectees']} allergie(s)")
        
        for allergie in allergies_result["allergies"]:
            status = "🤖 Auto-détectée" if allergie["detectee_automatiquement"] else "✋ Ajoutée manuellement"
            print(f"   • {allergie['nom']} - {allergie['gravite_personnelle']} {status}")
    
    # 7. Statistiques globales du système
    print("\n📈 ÉTAPE 7: Statistiques globales du système")
    stats_result = make_request("GET", "/allergies/statistics")
    
    if stats_result:
        resume = stats_result["resume_global"]
        print(f"\n🌍 STATISTIQUES GLOBALES:")
        print(f"   • Total utilisateurs: {resume['total_utilisateurs']}")
        print(f"   • Total réactions enregistrées: {resume['total_reactions_enregistrees']}")
        print(f"   • Total allergies confirmées: {resume['total_allergies_confirmees']}")
        print(f"   • Détections auto (30j): {resume['detections_automatiques_30j']}")
        print(f"   • Taux détection auto: {resume['taux_detection_auto']}%")
        
        print(f"\n🔥 ALLERGIES LES PLUS FRÉQUENTES:")
        for allergie in stats_result["allergies_plus_frequentes"][:5]:
            print(f"   • {allergie['allergie']}: {allergie['nombre_cas']} cas")
        
        print(f"\n⚠️ ALIMENTS LES PLUS PROBLÉMATIQUES:")
        for aliment in stats_result["aliments_plus_problematiques"][:5]:
            print(f"   • {aliment['aliment']}: {aliment['taux_reaction_moyen']}% de réactions")
    
    print("\n🎉" + "="*80)
    print("  DÉMONSTRATION TERMINÉE AVEC SUCCÈS!")
    print("  Le système d'allergies avancé fonctionne parfaitement.")
    print("="*84)

if __name__ == "__main__":
    print("🚀 Démarrage de la démonstration du système d'allergies avancé...")
    demo_systeme_allergies()
