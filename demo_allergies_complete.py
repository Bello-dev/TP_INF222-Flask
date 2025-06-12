#!/usr/bin/env python3
"""
🎯 DÉMONSTRATION COMPLÈTE - SYSTÈME AVANCÉ DE GESTION DES ALLERGIES
================================================================

Ce script démontre toutes les fonctionnalités avancées du système de gestion
des allergies avec intelligence artificielle.

Fonctionnalités démontrées :
- 🔍 Analyse de profil allergique complet
- ⚠️ Vérification de risque en temps réel
- 📊 Statistiques globales et tendances
- 🤖 Détection automatique d'allergies (>30% probabilité)
- 💡 Recommandations personnalisées
"""

import requests
import json
from time import sleep
from datetime import datetime

API_BASE = "http://localhost:5000/api"

def print_section(title):
    """Affiche une section formatée"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_subsection(title):
    """Affiche une sous-section formatée"""
    print(f"\n📋 {title}")
    print("-" * 40)

def test_api_endpoint(endpoint, description):
    """Teste un endpoint API et affiche le résultat"""
    try:
        response = requests.get(f"{API_BASE}{endpoint}")
        print(f"🌐 {description}")
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return None

def demo_user_profile(user_id, nom_utilisateur):
    """Démontre l'analyse de profil allergique"""
    print_subsection(f"Profil Allergique - {nom_utilisateur}")
    
    data = test_api_endpoint(f"/allergies/users/{user_id}/profile", 
                           f"Analyse complète du profil allergique")
    
    if data:
        utilisateur = data.get("utilisateur", {})
        resume = data.get("resume_allergique", {})
        allergies = data.get("allergies_confirmees", [])
        risques = data.get("analyse_risques_aliments", [])
        recommandations = data.get("recommandations", [])
        
        print(f"👤 Utilisateur: {utilisateur.get('nom_complet', 'N/A')}")
        print(f"📧 Email: {utilisateur.get('email', 'N/A')}")
        print(f"🧪 Aliments testés: {resume.get('total_aliments_testes', 0)}")
        print(f"🚨 Allergies détectées: {resume.get('allergies_detectees', 0)}")
        print(f"📊 Pourcentage d'allergies: {resume.get('pourcentage_allergies', 0)}%")
        print(f"⚠️ Niveau de risque global: {resume.get('niveau_risque_global', 'N/A')}")
        
        if allergies:
            print(f"\n🩺 Allergies confirmées ({len(allergies)}):")
            for allergie in allergies:
                auto_detect = "🤖 AUTO" if allergie.get("detectee_automatiquement") else "👨‍⚕️ MANUELLE"
                print(f"  - {allergie['allergie']['nom']} ({allergie['gravite_personnelle']}) {auto_detect}")
        
        if risques:
            print(f"\n📈 Analyse des risques par aliment:")
            for risque in risques[:3]:  # Top 3
                aliment = risque.get("aliment", {})
                prob = risque.get("probabilite_allergie", 0)
                niveau = risque.get("niveau_risque", "N/A")
                reactions = f"{risque.get('times_reacted', 0)}/{risque.get('times_eaten', 0)}"
                print(f"  - {aliment.get('nom', 'N/A')}: {prob}% ({niveau}) [{reactions}]")
        
        if recommandations:
            print(f"\n💡 Recommandations ({len(recommandations)}):")
            for rec in recommandations:
                priorite = rec.get("priorite", "N/A")
                message = rec.get("message", "N/A")
                print(f"  - [{priorite}] {message}")

def demo_risk_check(user_id, aliment_id, nom_utilisateur, nom_aliment):
    """Démontre la vérification de risque en temps réel"""
    print_subsection(f"Vérification Risque - {nom_utilisateur} + {nom_aliment}")
    
    data = test_api_endpoint(f"/allergies/check/{user_id}/{aliment_id}", 
                           f"Analyse de risque en temps réel")
    
    if data:
        utilisateur = data.get("utilisateur", {})
        aliment = data.get("aliment", {})
        analyse = data.get("analyse_risque", {})
        historique = analyse.get("historique_reactions", {})
        
        print(f"👤 Utilisateur: {utilisateur.get('nom_complet', 'N/A')}")
        print(f"🥜 Aliment: {aliment.get('nom', 'N/A')}")
        print(f"⚠️ Niveau de risque: {analyse.get('niveau_risque', 'N/A')}")
        print(f"📊 Probabilité d'allergie: {analyse.get('probabilite_allergie', 0)}%")
        print(f"💡 Recommandation: {analyse.get('recommandation', 'N/A')}")
        print(f"🔬 Allergie confirmée: {'✅ Oui' if analyse.get('allergie_confirmee') else '❌ Non'}")
        
        if historique:
            eaten = historique.get("times_eaten", 0)
            reacted = historique.get("times_reacted", 0)
            print(f"📝 Historique: {reacted} réactions sur {eaten} consommations")

def demo_global_statistics():
    """Démontre les statistiques globales"""
    print_subsection("Statistiques Globales du Système")
    
    data = test_api_endpoint("/allergies/statistics", 
                           "Statistiques et tendances globales")
    
    if data:
        resume = data.get("resume_global", {})
        allergies_freq = data.get("allergies_plus_frequentes", [])
        aliments_prob = data.get("aliments_plus_problematiques", [])
        
        print(f"👥 Total utilisateurs: {resume.get('total_utilisateurs', 0)}")
        print(f"🧪 Réactions enregistrées: {resume.get('total_reactions_enregistrees', 0)}")
        print(f"🚨 Allergies confirmées: {resume.get('total_allergies_confirmees', 0)}")
        print(f"🤖 Détections automatiques (30j): {resume.get('detections_automatiques_30j', 0)}")
        print(f"📊 Taux de détection auto: {resume.get('taux_detection_auto', 0)}%")
        
        if allergies_freq:
            print(f"\n🏆 Allergies les plus fréquentes:")
            for allergie in allergies_freq:
                nom = allergie.get("allergie", "N/A")
                cas = allergie.get("nombre_cas", 0)
                print(f"  - {nom}: {cas} cas")
        
        if aliments_prob:
            print(f"\n⚠️ Aliments les plus problématiques:")
            for aliment in aliments_prob:
                nom = aliment.get("aliment", "N/A")
                taux = aliment.get("taux_reaction_moyen", 0)
                print(f"  - {nom}: {taux:.1f}% de taux de réaction")

def main():
    """Fonction principale de démonstration"""
    print_section("DÉMONSTRATION SYSTÈME AVANCÉ DE GESTION DES ALLERGIES")
    print("🤖 Intelligence Artificielle pour la détection automatique d'allergies")
    print("🎯 Seuil de détection: >30% de probabilité de réaction")
    print(f"⏰ Démonstration exécutée le: {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    
    # 1. Profil utilisateur à faible risque
    demo_user_profile(2, "Jean Martin (Faible Risque)")
    sleep(1)
    
    # 2. Profil utilisateur à haut risque avec allergies détectées
    demo_user_profile(3, "Marie Dupont (Haut Risque)")
    sleep(1)
    
    # 3. Vérification de risque en temps réel - cas à risque élevé
    demo_risk_check(3, 16, "Marie Dupont", "Lait")
    sleep(1)
    
    # 4. Vérification de risque en temps réel - cas normal
    demo_risk_check(2, 19, "Jean Martin", "Poisson")
    sleep(1)
    
    # 5. Statistiques globales
    demo_global_statistics()
    
    # 6. Résumé des fonctionnalités
    print_section("RÉSUMÉ DES FONCTIONNALITÉS AVANCÉES")
    print("✅ 🔍 Analyse de profil allergique complet avec IA")
    print("✅ ⚠️ Vérification de risque en temps réel")
    print("✅ 🤖 Détection automatique d'allergies (>30% probabilité)")
    print("✅ 📊 Calcul de probabilités basé sur l'historique")
    print("✅ 💡 Recommandations personnalisées intelligentes")
    print("✅ 🏥 Classification automatique des niveaux de risque")
    print("✅ 📈 Statistiques globales et tendances")
    print("✅ 🦠 Gestion multi-allergènes avec gravité personnalisée")
    print("✅ 📱 API REST complète avec Swagger UI")
    print("✅ 🐳 Déploiement Docker avec PostgreSQL")
    
    print("\n🎯 SYSTÈME PRÊT POUR PRODUCTION!")
    print("📖 Documentation Swagger: http://localhost:5000/swagger-ui/")
    print("🔗 API Base URL: http://localhost:5000/api/allergies/")

if __name__ == "__main__":
    main()
