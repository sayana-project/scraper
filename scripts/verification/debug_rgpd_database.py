# -*- coding: utf-8 -*-
"""
Debug et vérification de la base de données RGPD
Pour vérifier pourquoi les données ne sont pas insérées
"""

import sqlite3
import json
from pathlib import Path

def check_database():
    """Vérifie l'état de la base de données RGPD"""
    db_path = Path("data/immobilier_rgpd.db")

    if not db_path.exists():
        print(" Base de données RGPD introuvable")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("🔍 Vérification base de données RGPD")
        print("=" * 50)

        # Lister les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f" Tables créées : {[t[0] for t in tables]}")

        # Vérifier chaque table
        for table_name in [t[0] for t in tables if not t[0].startswith('sqlite_')]:
            print(f"\n Table : {table_name}")

            # Compter les enregistrements
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   • Nombre d'enregistrements : {count}")

            # Voir la structure
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"   • Colonnes : {[col[1] for col in columns]}")

            # Afficher quelques enregistrements s'il y en a
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                rows = cursor.fetchall()
                for i, row in enumerate(rows):
                    print(f"   • Exemple {i+1} : {row}")
            else:
                print(f"Table vide")

        print("\n" + "=" * 50)

        # Charger les données source
        data_dir = Path("data")
        properties_file = data_dir / "generated_properties.json"
        demographics_file = data_dir / "generated_demographics.json"

        source_data = {'properties': [], 'demographics': []}

        if properties_file.exists():
            with open(properties_file, 'r', encoding='utf-8') as f:
                source_data['properties'] = json.load(f)
            print(f"Fichier propriétés : {len(source_data['properties'])} enregistrements")
        else:
            print("Fichier properties.json introuvable")

        if demographics_file.exists():
            with open(demographics_file, 'r', encoding='utf-8') as f:
                source_data['demographics'] = json.load(f)
            print(f"Fichier démographiques : {len(source_data['demographics'])} enregistrements")
        else:
            print("Fichier demographics.json introuvable")

        # Diagnostic du problème
        if source_data['properties'] and 'proprietes_anonymisees' in [t[0] for t in tables]:
            print("\n🔧 Diagnostic du problème d'insertion")

            # Prendre un exemple de propriété
            sample_prop = source_data['properties'][0]
            print(f" Exemple propriété source :")
            for key, value in sample_prop.items():
                print(f"   • {key}: {value} (type: {type(value)})")

            # Vérifier les colonnes requises
            required_fields = ['title', 'price', 'surface', 'postal_code', 'city']
            missing_fields = [field for field in required_fields if field not in sample_prop]
            if missing_fields:
                print(f" Champs manquants : {missing_fields}")
            else:
                print(" Tous les champs requis présents")

            # Vérifier les valeurs NULL
            null_fields = [field for field, value in sample_prop.items() if value is None]
            if null_fields:
                print(f" Champs NULL : {null_fields}")

            # Préparer la requête d'insertion manuelle
            print("\n🔧 Test d'insertion manuelle :")
            try:
                insert_sql = """
                INSERT INTO proprietes_anonymisees
                (code_postal, ville, quartier_anonymise, surface_m2, prix_euros,
                 prix_m2_euros, type_bien, source_collecte, date_collecte,
                 mois_annee, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

                cursor.execute(insert_sql, (
                    str(sample_prop.get('postal_code', ''))[:5],  # CP 5 chiffres
                    sample_prop.get('city', ''),
                    f"Quartier_anonymise",
                    int(sample_prop.get('surface', 1)),
                    int(sample_prop.get('price', 0)),
                    round(int(sample_prop.get('price', 0)) / int(sample_prop.get('surface', 1)), 2),
                    sample_prop.get('title', '')[:50],  # Type de bien
                    sample_prop.get('source', 'generated'),
                    '2025-11-30',  # Date fixe pour test
                    '2025-11',  # Mois
                    '2025-11-30 14:30:00'  # created_at
                ))

                conn.commit()
                print(" Insertion manuelle réussie !")

                # Vérifier le résultat
                cursor.execute("SELECT COUNT(*) FROM proprietes_anonymisees")
                new_count = cursor.fetchone()[0]
                print(f" Nouveau nombre d'enregistrements : {new_count}")

            except Exception as e:
                print(f" Erreur insertion manuelle : {e}")
                conn.rollback()

        conn.close()

    except Exception as e:
        print(f" Erreur connexion base de données : {e}")

if __name__ == "__main__":
    check_database()