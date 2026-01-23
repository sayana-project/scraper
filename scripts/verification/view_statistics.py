# -*- coding: utf-8 -*-
"""
Script pour visualiser les statistiques agregees
"""

import sqlite3
from pathlib import Path

def view_statistics():
    """Affiche les statistiques de la table statistiques_agregees"""

    db_path = Path("data/immobilier_rgpd.db")

    if not db_path.exists():
        print("ERREUR: Base de donnees introuvable")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 70)
    print("CONTENU DE LA TABLE statistiques_agregees")
    print("=" * 70)

    # Compter les enregistrements
    cursor.execute("SELECT COUNT(*) FROM statistiques_agregees")
    count = cursor.fetchone()[0]

    print(f"\nTotal: {count} enregistrements")

    if count == 0:
        print("La table est vide!")
        conn.close()
        return

    # Afficher toutes les statistiques
    print("\nDETAIL PAR VILLE:")
    print("-" * 70)

    cursor.execute("""
        SELECT
            ville,
            code_postal,
            mois_annee,
            nombre_biens,
            ROUND(prix_moyen_m2, 2) as prix_moy,
            ROUND(prix_min_m2, 2) as prix_min,
            ROUND(prix_max_m2, 2) as prix_max,
            ROUND(surface_moyenne, 2) as surf_moy
        FROM statistiques_agregees
        ORDER BY nombre_biens DESC
    """)

    results = cursor.fetchall()

    for i, row in enumerate(results, 1):
        ville, cp, mois, nb, prix_moy, prix_min, prix_max, surf_moy = row
        print(f"\n{i}. {ville} ({cp}) - {mois}")
        print(f"   Nombre de biens: {nb}")
        print(f"   Prix moyen/m2: {prix_moy:.2f} EUR")
        print(f"   Prix min/max: {prix_min:.2f} - {prix_max:.2f} EUR")
        print(f"   Surface moyenne: {surf_moy:.2f} m2")

    # Statistiques globales
    cursor.execute("""
        SELECT
            COUNT(DISTINCT ville) as nb_villes,
            SUM(nombre_biens) as total_biens,
            ROUND(AVG(prix_moyen_m2), 2) as prix_global_moyen
        FROM statistiques_agregees
    """)

    nb_villes, total_biens, prix_global = cursor.fetchone()

    print("\n" + "=" * 70)
    print("RESUME GLOBAL")
    print("=" * 70)
    print(f"Villes: {nb_villes}")
    print(f"Total biens: {total_biens}")
    print(f"Prix moyen global: {prix_global:.2f} EUR/m2")

    conn.close()

    print("\n" + "=" * 70)
    print("La table statistiques_agregees existe et contient des donnees!")
    print("Si vous ne la voyez pas dans votre outil, rafraichissez-le.")
    print("=" * 70)

if __name__ == "__main__":
    view_statistics()
