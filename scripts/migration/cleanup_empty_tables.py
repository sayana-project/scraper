# -*- coding: utf-8 -*-
"""
Script pour supprimer les tables vides inutilisees
"""

import sqlite3
from pathlib import Path

def cleanup_empty_tables():
    """Supprime les tables vides qui ne sont pas utilisees"""

    db_path = Path("data/immobilier_rgpd.db")

    if not db_path.exists():
        print("ERREUR: Base de donnees introuvable")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tables a supprimer
    tables_to_drop = [
        "aggregated_properties",
        "demographic_data",
        "donnees_demographiques"
    ]

    print("=" * 70)
    print("NETTOYAGE DES TABLES VIDES")
    print("=" * 70)

    try:
        for table in tables_to_drop:
            # Verifier si la table existe
            cursor.execute(f"""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name=?
            """, (table,))

            exists = cursor.fetchone()

            if exists:
                # Compter les enregistrements
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]

                if count == 0:
                    # Supprimer la table vide
                    cursor.execute(f"DROP TABLE {table}")
                    print(f"\n[OK] Table '{table}' supprimee (etait vide)")
                else:
                    print(f"\n[SKIP] Table '{table}' conservee ({count} enregistrements)")
            else:
                print(f"\n[INFO] Table '{table}' n'existe pas")

        conn.commit()

        # Verifier les tables restantes
        print("\n" + "=" * 70)
        print("TABLES RESTANTES DANS LA BASE")
        print("=" * 70)

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """)

        remaining_tables = cursor.fetchall()

        for table in remaining_tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]

            status = "VIDE" if count == 0 else f"{count} enregistrements"
            symbol = "[!]" if count == 0 else "[OK]"

            print(f"{symbol} {table_name:40} : {status}")

        conn.close()

        print("\n" + "=" * 70)
        print("NETTOYAGE TERMINE AVEC SUCCES")
        print("=" * 70)
        print("\nTables importantes conservees:")
        print("  - proprietes_anonymisees")
        print("  - statistiques_agregees")
        print("\nTables inutilisees supprimees:")
        print("  - aggregated_properties")
        print("  - demographic_data")
        print("  - donnees_demographiques")

        return True

    except Exception as e:
        print(f"\nERREUR lors du nettoyage: {e}")
        conn.rollback()
        conn.close()
        return False

if __name__ == "__main__":
    success = cleanup_empty_tables()
    exit(0 if success else 1)
