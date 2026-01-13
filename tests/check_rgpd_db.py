# -*- coding: utf-8 -*-
"""
Script simple pour vérifier la base de données RGPD
"""

import sqlite3
import json
from pathlib import Path

def check_database():
    """Vérifier l'état de la base RGPD"""
    db_path = Path("data/immobilier_rgpd.db")

    if not db_path.exists():
        print("Base de données RGPD introuvable")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("Verification base de donnees RGPD")
        print("=" * 50)

        # Lister les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables creees: {[t[0] for t in tables]}")

        # Vérifier chaque table
        for table_name in [t[0] for t in tables if not t[0].startswith('sqlite_')]:
            print(f"\nTable: {table_name}")

            # Compter les enregistrements
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  Nombre d'enregistrements: {count}")

            # Voir la structure
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"  Colonnes: {[col[1] for col in columns]}")

            # Si données, montrer quelques exemples
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                rows = cursor.fetchall()
                print(f"  Exemples:")
                for i, row in enumerate(rows):
                    print(f"    {i+1}: {row}")
            else:
                print("  Table vide")

        print("\n" + "=" * 50)
        print("Diagnostic des donnees source")

        # Vérifier les fichiers sources
        data_dir = Path("data")
        properties_file = data_dir / "generated_properties.json"
        demographics_file = data_dir / "generated_demographics.json"

        source_data = {"properties": [], "demographics": []}

        if properties_file.exists():
            with open(properties_file, 'r', encoding='utf-8') as f:
                source_data["properties"] = json.load(f)
            print(f"Fichier properties: {len(source_data['properties'])} enregistrements")

            # Vérifier un exemple
            if source_data["properties"]:
                sample = source_data["properties"][0]
                print(f"Exemple propriete: {sample}")
        else:
            print("Fichier properties introuvable")

        if demographics_file.exists():
            with open(demographics_file, 'r', encoding='utf-8') as f:
                source_data["demographics"] = json.load(f)
            print(f"Fichier demographics: {len(source_data['demographics'])} enregistrements")

            # Vérifier un exemple
            if source_data["demographics"]:
                sample = source_data["demographics"][0]
                print(f"Exemple demographic: {sample}")
        else:
            print("Fichier demographics introuvable")

        print("\n" + "=" * 50)
        print("DIAGNOSTIC:")

        if source_data["properties"] and any("proprietes_anonymisees" in str(t) for t in tables):
            print("OK: Tables RGPD crees et donnees source disponibles")

            # Problème potentiel: prix_m2_euros NOT NULL mais calculé
            sample_prop = source_data["properties"][0]
            print(f"\nProbleme potentiel detecte:")
            print(f"  Propriete exemple - Prix: {sample_prop.get('price')}")
            print(f"  Propriete exemple - Surface: {sample_prop.get('surface')}")
            print(f"  Calcul prix/m2: {sample_prop.get('price') / sample_prop.get('surface') if sample_prop.get('surface') else 0}")
            print(f"  La table requiert prix_m2_euros NOT NULL")

        else:
            print("ERREUR: Tables ou donnees manquantes")

        conn.close()

    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    check_database()