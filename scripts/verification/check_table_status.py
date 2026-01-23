# -*- coding: utf-8 -*-
"""
Script pour verifier si les tables sont vides ou contiennent des donnees
"""

import sqlite3
from pathlib import Path

def check_table_status():
    """Verifie le contenu des tables suspectes"""

    db_path = Path("data/immobilier_rgpd.db")

    if not db_path.exists():
        print("ERREUR: Base de donnees introuvable")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tables a verifier
    tables_to_check = [
        "aggregated_properties",
        "demographic_data",
        "donnees_demographiques"
    ]

    print("=" * 70)
    print("VERIFICATION DES TABLES")
    print("=" * 70)

    for table in tables_to_check:
        try:
            # Verifier si la table existe
            cursor.execute(f"""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name=?
            """, (table,))

            exists = cursor.fetchone()

            if not exists:
                print(f"\n[X] {table:30} : TABLE N'EXISTE PAS")
                continue

            # Compter les enregistrements
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]

            if count == 0:
                status = f"VIDE (0 enregistrements)"
                symbol = "[X]"
            else:
                status = f"CONTIENT {count} enregistrements"
                symbol = "[OK]"

            print(f"\n{symbol} {table:30} : {status}")

            # Si la table contient des donnees, afficher un echantillon
            if count > 0:
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                sample = cursor.fetchall()

                # Obtenir les noms de colonnes
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [col[1] for col in cursor.fetchall()]

                print(f"\n    Colonnes: {', '.join(columns)}")
                print(f"    Echantillon (3 premiers):")
                for i, row in enumerate(sample, 1):
                    print(f"      {i}. {row[:3]}...")  # Afficher les 3 premieres colonnes

        except Exception as e:
            print(f"\n[!] {table:30} : ERREUR - {str(e)}")

    conn.close()

    print("\n" + "=" * 70)
    print("VERIFICATION TERMINEE")
    print("=" * 70)

if __name__ == "__main__":
    check_table_status()
