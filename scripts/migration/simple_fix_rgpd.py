# -*- coding: utf-8 -*-
"""
Script simple pour corriger et migrer les données dans la base RGPD
Sans caractères spéciaux pour éviter les problèmes d'encodage Windows
"""

import sqlite3
import json
from pathlib import Path

def fix_and_migrate_data():
    """Corriger les problèmes de migration et insérer les données"""

    # Chemins des fichiers
    db_path = Path("data/immobilier_rgpd.db")
    properties_file = Path("data/generated_properties.json")

    print("=== CORRECTION MIGRATION BASE RGPD ===")

    # Vérifier que la base existe
    if not db_path.exists():
        print("ERREUR: Base de données RGPD introuvable")
        return

    # Vérifier que les données source existent
    if not properties_file.exists():
        print("ERREUR: Fichier properties introuvable")
        return

    # Charger les données
    with open(properties_file, 'r', encoding='utf-8') as f:
        properties = json.load(f)

    print(f"Chargement de {len(properties)} propriétés depuis le fichier JSON")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Compter les enregistrements actuels
        cursor.execute("SELECT COUNT(*) FROM proprietes_anonymisees")
        current_count = cursor.fetchone()[0]
        print(f"Nombre actuel d'enregistrements: {current_count}")

        # Préparer la requête d'insertion avec calcul correct du prix/m²
        insert_sql = """
        INSERT INTO proprietes_anonymisees
        (code_postal, ville, quartier_anonymise, surface_m2, prix_euros,
         prix_m2_euros, type_bien, source_collecte, date_collecte,
         date_anonymisation, mois_annee, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        inserted_count = 0
        errors_count = 0

        for i, prop in enumerate(properties):
            try:
                # Récupérer et valider les données
                price = int(prop.get('price', 0))
                surface = max(int(prop.get('surface', 1)), 1)  # Éviter division par zéro
                postal_code = str(prop.get('postal_code', ''))[:5]
                city = prop.get('city', '')
                title = prop.get('title', '')[:50]
                source = prop.get('source', 'generated')

                # Calculer le prix au m²
                price_per_m2 = round(price / surface, 2) if surface > 0 else 0

                # Insérer la propriété
                cursor.execute(insert_sql, (
                    postal_code,
                    city,
                    f"Quartier_{i % 20}",  # Quartier anonymisé (0-19)
                    surface,
                    price,
                    price_per_m2,  # Maintenant correctement calculé
                    title,
                    source,
                    '2025-11-30',  # Date fixe pour test
                    '2025-11-30 15:00:00',  # date_anonymisation
                    '2025-11',  # mois_annee
                    '2025-11-30 15:00:00'  # created_at
                ))

                inserted_count += 1

                # Afficher la progression toutes les 100 propriétés
                if (i + 1) % 100 == 0:
                    print(f"Progression: {i + 1}/{len(properties)} propriétés traitées")

            except Exception as e:
                errors_count += 1
                if errors_count <= 5:  # Afficher seulement les 5 premières erreurs
                    print(f"ERREUR insertion propriété {i}: {e}")
                continue

        # Commit des transactions
        conn.commit()

        # Vérifier le résultat
        cursor.execute("SELECT COUNT(*) FROM proprietes_anonymisees")
        final_count = cursor.fetchone()[0]

        print("\n=== RESULTATS MIGRATION ===")
        print(f"Propriétés traitées: {len(properties)}")
        print(f"Propriétés insérées: {inserted_count}")
        print(f"Erreurs: {errors_count}")
        print(f"Nombre avant migration: {current_count}")
        print(f"Nombre après migration: {final_count}")
        print(f"Net ajouté: {final_count - current_count}")

        # Afficher quelques exemples
        print("\n=== EXEMPLES PROPRIETES MIGREES ===")
        cursor.execute("SELECT code_postal, ville, surface_m2, prix_euros, prix_m2_euros, type_bien FROM proprietes_anonymisees LIMIT 5")
        rows = cursor.fetchall()

        for i, row in enumerate(rows):
            cp, ville, surface, prix, prix_m2, type_bien = row
            print(f"{i+1}. CP:{cp} Ville:{ville} Surface:{surface}m2 Prix:{prix}€ Prix/m2:{prix_m2}€ Type:{type_bien}")

        print("\nMigration terminée avec succès!")
        conn.close()

    except Exception as e:
        print(f"ERREUR globale: {e}")

if __name__ == "__main__":
    fix_and_migrate_data()