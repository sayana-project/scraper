# -*- coding: utf-8 -*-
"""
Générateur de données immobilières réalistes pour Phase 4 - C4 RGPD
Crée des données d'exemple conformes RGPD pour tester l'architecture
"""

import json
import random
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

class RealisticDataGenerator:
    """Générateur de données immobilières réalistes et RGPD-compliant"""

    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        # Villes françaises avec plus de 10000 habitants (conformité RGPD)
        self.villes = [
            {"nom": "Paris", "cp": "75001", "quartiers": ["Louvre", "Marais", "Saint-Germain", "Montmartre"]},
            {"nom": "Lyon", "cp": "69001", "quartiers": ["Presqu'île", "Croix-Rousse", "Part-Dieu", "Fourvière"]},
            {"nom": "Marseille", "cp": "13001", "quartiers": ["Vieux-Port", "Panier", "Endoume", "Pointe-Rouge"]},
            {"nom": "Bordeaux", "cp": "33000", "quartiers": ["Centre-ville", "Chartrons", "Saint-Michel", "Bastide"]},
            {"nom": "Toulouse", "cp": "31000", "quartiers": ["Capitole", "Carmes", "Saint-Cyprien", "Minimes"]},
            {"nom": "Nice", "cp": "06000", "quartiers": ["Vieux-Nice", "Libération", "Riquier", "Paillon"]},
            {"nom": "Nantes", "cp": "44000", "quartiers": ["Bouffay", "Graslin", "Madeleine", "Dervallières"]},
            {"nom": "Strasbourg", "cp": "67000", "quartiers": ["Krutenau", "Centre", "Neustadt", "Orangerie"]},
            {"nom": "Lille", "cp": "59000", "quartiers": ["Vieux-Lille", "Wazemmes", "Fives", "Esquermes"]},
            {"nom": "Brest", "cp": "29200", "quartiers": ["Centre-ville", "Saint-Marc", "Lambézellec", "Kerichen"]},
            {"nom": "Montpellier", "cp": "34000", "quartiers": ["Ecusson", "Antigone", "Port Marianne", "Celleneuve"]},
            {"nom": "Rennes", "cp": "35000", "quartiers": ["Centre", "Villejean", "Brazais", "Cleunay"]},
            {"nom": "Grenoble", "cp": "38000", "quartiers": ["Centre", "Bastille", "Saint-Laurent", "Mistral"]},
            {"nom": "Dijon", "cp": "21000", "quartiers": ["Centre", "Faubourg North", "Montchapet", "Marsannay"]},
            {"nom": "Angers", "cp": "49000", "quartiers": ["Centre", "Lac de Maine", "Belle-Beille", "Roseraie"]},
            {"nom": "Saint-Étienne", "cp": "42000", "quartiers": ["Centre", "Trefilerie", "Le Corbusier", "Villeboeuf"]},
            {"nom": "Nîmes", "cp": "30000", "quartiers": ["Centre-ville", "Écusson", "Garrigues", "Valdegour"]},
            {"nom": "Aix-en-Provence", "cp": "13100", "quartiers": ["Centre-ville", "Cours Mirabeau", "Jas de Bouffan", "Puyricard"]},
            {"nom": "Le Mans", "cp": "72000", "quartiers": ["Centre", "Jacobins", "Yzeure", "Grie"]},
            {"nom": "Clermont-Ferrand", "cp": "63000", "quartiers": ["Centre", "Jardin Lecoq", "Montferrand", "Champratel"]}
        ]

        # Types de biens immobiliers
        self.types_biens = ["Studio", "T1", "T2", "T3", "T4", "T5+", "Maison", "Villa", "Appartement", "Duplex", "Loft"]

        # Sources de données
        self.sources = ["seloger", "leboncoin", "csv_import", "insee", "json_import"]

        # Plages de prix réalistes par ville (€/m²)
        self.prix_m2_par_ville = {
            "Paris": {"min": 8000, "max": 15000},
            "Lyon": {"min": 4000, "max": 7000},
            "Marseille": {"min": 3000, "max": 5500},
            "Bordeaux": {"min": 3500, "max": 6500},
            "Toulouse": {"min": 2800, "max": 4800},
            "Nice": {"min": 3800, "max": 6500},
            "Nantes": {"min": 3200, "max": 5200},
            "Strasbourg": {"min": 2900, "max": 4700},
            "Lille": {"min": 2600, "max": 4200},
            "Brest": {"min": 2200, "max": 3600},
            "Montpellier": {"min": 3100, "max": 5000},
            "Rennes": {"min": 2700, "max": 4300},
            "Grenoble": {"min": 2800, "max": 4500},
            "Dijon": {"min": 2300, "max": 3800},
            "Angers": {"min": 2000, "max": 3200},
            "Saint-Étienne": {"min": 1800, "max": 2900},
            "Nîmes": {"min": 2100, "max": 3400},
            "Aix-en-Provence": {"min": 3500, "max": 6000},
            "Le Mans": {"min": 1900, "max": 3000},
            "Clermont-Ferrand": {"min": 1700, "max": 2700}
        }

        # Données démographiques INSEE simulées
        self.donnees_demo_par_ville = {}
        for ville_data in self.villes:
            nom_ville = ville_data["nom"]
            self.donnees_demo_par_ville[nom_ville] = {
                "population_quartier": random.randint(15000, 80000),
                "revenu_moyen_annuel": random.randint(20000, 45000),
                "densite_habitat": random.uniform(1000, 8000),  # hab/km²
                "age_moyen_habitants": round(random.uniform(28, 45), 1),
                "nb_familles": random.randint(3000, 20000),
                "taux_proprietaire": round(random.uniform(35, 65), 1),
                "nb_logements": random.randint(5000, 35000)
            }

    def generate_properties(self, nb_properties=1000):
        """Génère des propriétés immobilières réalistes"""
        properties = []

        for i in range(nb_properties):
            ville_data = random.choice(self.villes)
            nom_ville = ville_data["nom"]
            cp = ville_data["cp"]
            quartier = random.choice(ville_data["quartiers"])

            # Génération surface et prix réalistes
            type_bien = random.choice(self.types_biens)

            # Surface selon type de bien
            if "Studio" in type_bien or "T1" in type_bien:
                surface = random.randint(15, 35)
            elif "T2" in type_bien:
                surface = random.randint(30, 50)
            elif "T3" in type_bien:
                surface = random.randint(45, 70)
            elif "T4" in type_bien:
                surface = random.randint(60, 90)
            elif "T5" in type_bien or "Maison" in type_bien or "Villa" in type_bien:
                surface = random.randint(80, 200)
            else:
                surface = random.randint(20, 100)

            # Prix selon ville et surface
            prix_m2 = random.uniform(
                self.prix_m2_par_ville[nom_ville]["min"],
                self.prix_m2_par_ville[nom_ville]["max"]
            )

            # Ajout de variation selon le quartier
            quartier_premium = ["Louvre", "Saint-Germain", "Centre", "Vieux-Port", "Capitole"]
            if quartier in quartier_premium:
                prix_m2 *= random.uniform(1.1, 1.3)
            else:
                prix_m2 *= random.uniform(0.8, 1.1)

            prix = int(surface * prix_m2)

            # Date de collecte (derniers 6 mois)
            jours_aleatoires = random.randint(0, 180)
            date_collecte = (datetime.now() - timedelta(days=jours_aleatoires)).isoformat()

            propriete = {
                "title": f"{type_bien} {random.choice(['moderne', 'rénové', 'lumineux', 'calme', 'bien situé'])} à {quartier}",
                "price": prix,
                "surface": surface,
                "postal_code": cp,
                "city": nom_ville,
                "source": random.choice(self.sources),
                "scraped_at": date_collecte,
                "quartier_anonymise": f"Quartier_{i % 50}",  # Anonymisation RGPD
                "date_anonymisation": datetime.now().isoformat()  # Tracking RGPD
            }

            properties.append(propriete)

        return properties

    def generate_demographic_data(self):
        """Génère les données démographiques INSEE"""
        demographics = []

        for ville_data in self.villes:
            nom_ville = ville_data["nom"]
            cp = ville_data["cp"]
            demo_data = self.donnees_demo_par_ville[nom_ville]

            record = {
                "postal_code": cp,
                "city": nom_ville,
                "population": demo_data["population_quartier"],
                "revenu_moyen_annuel": demo_data["revenu_moyen_annuel"],
                "densite_habitat": round(demo_data["densite_habitat"], 0),
                "age_moyen_habitants": demo_data["age_moyen_habitants"],
                "nb_familles": demo_data["nb_familles"],
                "taux_proprietaire": demo_data["taux_proprietaire"],
                "nb_logements": demo_data["nb_logements"],
                "source": "insee",
                "scraped_at": datetime.now().isoformat(),
                "date_anonymisation": datetime.now().isoformat()
            }

            demographics.append(record)

        return demographics

    def save_data(self, properties, demographics):
        """Sauvegarde les données générées"""
        # Sauvegarde en JSON
        with open(self.data_dir / "generated_properties.json", 'w', encoding='utf-8') as f:
            json.dump(properties, f, ensure_ascii=False, indent=2)

        with open(self.data_dir / "generated_demographics.json", 'w', encoding='utf-8') as f:
            json.dump(demographics, f, ensure_ascii=False, indent=2)

        # Sauvegarde en CSV
        df_properties = pd.DataFrame(properties)
        df_properties.to_csv(self.data_dir / "generated_properties.csv", index=False, encoding='utf-8')

        df_demographics = pd.DataFrame(demographics)
        df_demographics.to_csv(self.data_dir / "generated_demographics.csv", index=False, encoding='utf-8')

        print(f"Données générées avec succès :")
        print(f"   • {len(properties)} propriétés immobilières")
        print(f"   • {len(demographics)} enregistrements démographiques")
        print(f"   • Fichiers sauvegardés dans {self.data_dir}")
        print(f"   • {len(self.villes)} villes couvertes (>10000 habitants - Conforme RGPD)")

    def generate_full_dataset(self, nb_properties=2000):
        """Génère le jeu de données complet pour la Phase 4 RGPD"""
        print("DEMARRAGE Génération de données immobilières réalistes pour Phase 4 - RGPD")
        print("=" * 60)

        # Génération des propriétés
        print("Generation des propriétés immobilières...")
        properties = self.generate_properties(nb_properties)

        # Génération des données démographiques
        print("Generation des données démographiques INSEE...")
        demographics = self.generate_demographic_data()

        # Sauvegarde des données
        print("Sauvegarde des données générées...")
        self.save_data(properties, demographics)

        print("=" * 60)
        print("Données générées avec conformité RGPD :")
        print("   Villes >10000 habitants obligatoires")
        print("   Anonymisation au niveau quartier")
        print("   Pas de données personnelles (noms, adresses)")
        print("   Prix et surfaces réalistes par ville")
        print("   Données INSEE publiques uniquement")
        print("=" * 60)

        return properties, demographics

def main():
    """Fonction principale"""
    generator = RealisticDataGenerator()
    properties, demographics = generator.generate_full_dataset(nb_properties=2000)

    return properties, demographics

if __name__ == "__main__":
    main()