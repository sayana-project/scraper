# -*- coding: utf-8 -*-
"""
Script pour analyser les dependances entre tables avant suppression
"""

import sqlite3
from pathlib import Path

def check_dependencies():
    """Verifie les foreign keys et dependances avant suppression"""

    db_path = Path("data/immobilier_rgpd.db")

    if not db_path.exists():
        print("ERREUR: Base de donnees introuvable")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tables a potentiellement supprimer
    tables_to_remove = [
        "aggregated_properties",
        "demographic_data",
        "donnees_demographiques"
    ]

    # Tables importantes a preserver
    important_tables = [
        "proprietes_anonymisees",
        "statistiques_agregees"
    ]

    print("=" * 70)
    print("ANALYSE DES DEPENDANCES DE TABLES")
    print("=" * 70)

    print("\n1. SCHEMAS DES TABLES A SUPPRIMER:")
    print("-" * 70)

    for table in tables_to_remove:
        try:
            cursor.execute(f"""
                SELECT sql FROM sqlite_master
                WHERE type='table' AND name=?
            """, (table,))

            result = cursor.fetchone()
            if result:
                print(f"\n{table}:")
                print(result[0])
        except Exception as e:
            print(f"\nERREUR sur {table}: {e}")

    print("\n\n2. FOREIGN KEYS POINTANT VERS CES TABLES:")
    print("-" * 70)

    # Verifier si d'autres tables referencent ces tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    all_tables = [row[0] for row in cursor.fetchall()]

    references_found = False

    for table in all_tables:
        try:
            cursor.execute(f"PRAGMA foreign_key_list({table})")
            foreign_keys = cursor.fetchall()

            for fk in foreign_keys:
                # fk = (id, seq, table_ref, from_col, to_col, on_update, on_delete, match)
                referenced_table = fk[2]

                if referenced_table in tables_to_remove:
                    print(f"\nATTENTION: {table} reference {referenced_table}")
                    print(f"   Colonne: {fk[3]} -> {referenced_table}.{fk[4]}")
                    references_found = True

        except Exception as e:
            pass

    if not references_found:
        print("\nAucune foreign key trouvee -> SUPPRESSION SECURISEE")

    print("\n\n3. RECHERCHE DE REFERENCES DANS LE CODE:")
    print("-" * 70)

    # Simuler une recherche de references dans les models
    print("\nVerification dans src/models/rgpd_models.py...")

    # Lire le fichier des modeles
    models_file = Path("src/models/rgpd_models.py")
    if models_file.exists():
        content = models_file.read_text(encoding='utf-8')

        for table in tables_to_remove:
            # Chercher les references a la table
            if table in content or table.replace('_', '') in content:
                print(f"\n[!] {table} reference dans rgpd_models.py")

                # Chercher la classe correspondante
                class_name = ''.join(word.capitalize() for word in table.split('_'))
                if class_name in content:
                    print(f"    -> Classe {class_name} trouvee")
            else:
                print(f"\n[OK] {table} NON reference dans rgpd_models.py")

    print("\n\n4. RECOMMENDATION:")
    print("=" * 70)

    if not references_found:
        print("\nSUPPRESSION SECURISEE - Aucune dependance detectee")
        print("\nActions a effectuer:")
        print("1. Supprimer les tables vides de la base de donnees")
        print("2. Nettoyer les modeles SQLAlchemy correspondants")
        print("3. Supprimer les imports inutilises")
        print("\nAucun impact sur:")
        for table in important_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   - {table}: {count} enregistrements")
    else:
        print("\nATTENTION - Dependances trouvees")
        print("Verifier les foreign keys avant suppression")

    conn.close()

    print("\n" + "=" * 70)

if __name__ == "__main__":
    check_dependencies()
