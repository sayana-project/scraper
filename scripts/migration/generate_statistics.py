# -*- coding: utf-8 -*-
"""
Script pour générer les statistiques agrégées à partir des propriétés
Nécessaire pour le bon fonctionnement de l'API Analytics (C5)
"""

import sqlite3
from datetime import datetime
from pathlib import Path

def generate_statistics():
    """
    Génère les statistiques agrégées par ville et mois
    À partir de la table proprietes_anonymisees
    """

    db_path = Path("data/immobilier_rgpd.db")

    if not db_path.exists():
        print("ERREUR: Base de données introuvable: data/immobilier_rgpd.db")
        return False

    print("=" * 70)
    print("GENERATION DES STATISTIQUES AGREGEES")
    print("=" * 70)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. Vérifier les données source
        cursor.execute("SELECT COUNT(*) FROM proprietes_anonymisees")
        nb_proprietes = cursor.fetchone()[0]
        print(f"\nProprietes disponibles: {nb_proprietes}")

        if nb_proprietes == 0:
            print("ERREUR: Aucune propriete a agreger")
            conn.close()
            return False

        # 2. Vider la table statistiques_agregees (si elle contient déjà des données)
        cursor.execute("DELETE FROM statistiques_agregees")
        print("Table statistiques_agregees videe")

        # 3. Générer les statistiques agrégées
        print("\nCalcul des statistiques par ville et mois...")

        aggregate_query = """
        INSERT INTO statistiques_agregees (
            code_postal,
            ville,
            mois_annee,
            prix_moyen_m2,
            prix_min_m2,
            prix_max_m2,
            surface_moyenne,
            surface_min,
            surface_max,
            nombre_biens,
            types_biens_distribution,
            date_calcul,
            methode_anonymisation
        )
        SELECT
            code_postal,
            ville,
            mois_annee,
            ROUND(AVG(prix_m2_euros), 2) as prix_moyen_m2,
            MIN(prix_m2_euros) as prix_min_m2,
            MAX(prix_m2_euros) as prix_max_m2,
            ROUND(AVG(surface_m2), 2) as surface_moyenne,
            MIN(surface_m2) as surface_min,
            MAX(surface_m2) as surface_max,
            COUNT(*) as nombre_biens,
            GROUP_CONCAT(DISTINCT type_bien) as types_biens_distribution,
            ? as date_calcul,
            'aggregation_mensuelle' as methode_anonymisation
        FROM proprietes_anonymisees
        GROUP BY code_postal, ville, mois_annee
        ORDER BY code_postal, ville, mois_annee
        """

        cursor.execute(aggregate_query, (datetime.now().isoformat(),))
        conn.commit()

        # 4. Vérifier le résultat
        cursor.execute("SELECT COUNT(*) FROM statistiques_agregees")
        nb_stats = cursor.fetchone()[0]

        print(f"Statistiques generees: {nb_stats} enregistrements")

        # 5. Afficher quelques exemples
        print("\nExemples de statistiques generees:")
        print("-" * 70)

        cursor.execute("""
            SELECT
                code_postal,
                ville,
                mois_annee,
                nombre_biens,
                prix_moyen_m2,
                prix_min_m2,
                prix_max_m2,
                surface_moyenne
            FROM statistiques_agregees
            ORDER BY nombre_biens DESC
            LIMIT 5
        """)

        results = cursor.fetchall()

        for row in results:
            cp, ville, mois, nb_biens, prix_moy, prix_min, prix_max, surf_moy = row
            print(f"\n{ville} ({cp}) - {mois}")
            print(f"   - Nombre de biens: {nb_biens}")
            print(f"   - Prix moyen/m2: {prix_moy:.2f} EUR")
            print(f"   - Prix min/max: {prix_min:.2f} EUR - {prix_max:.2f} EUR")
            print(f"   - Surface moyenne: {surf_moy:.2f} m2")

        # 6. Statistiques globales
        cursor.execute("""
            SELECT
                COUNT(DISTINCT ville) as nb_villes,
                COUNT(DISTINCT mois_annee) as nb_mois,
                SUM(nombre_biens) as total_biens,
                ROUND(AVG(prix_moyen_m2), 2) as prix_global_moyen
            FROM statistiques_agregees
        """)

        glob = cursor.fetchone()
        nb_villes, nb_mois, total_biens, prix_global = glob

        print("\n" + "=" * 70)
        print("RESUME GLOBAL")
        print("=" * 70)
        print(f"Villes couvertes: {nb_villes}")
        print(f"Periodes: {nb_mois} mois")
        print(f"Total biens agreges: {total_biens}")
        print(f"Prix moyen global: {prix_global:.2f} EUR/m2")

        # 7. Validation RGPD
        print("\nVALIDATION RGPD")
        print("-" * 70)

        # Vérifier qu'il n'y a pas de groupes trop petits (risque réidentification)
        cursor.execute("""
            SELECT COUNT(*)
            FROM statistiques_agregees
            WHERE nombre_biens < 5
        """)
        nb_petits_groupes = cursor.fetchone()[0]

        if nb_petits_groupes > 0:
            print(f"ATTENTION: {nb_petits_groupes} groupes avec moins de 5 biens")
            print("   -> Risque de reidentification RGPD")
            print("   -> Recommandation: Supprimer ou masquer ces groupes")
        else:
            print("Tous les groupes ont au moins 5 biens (RGPD conforme)")

        conn.close()

        print("\n" + "=" * 70)
        print("GENERATION TERMINEE AVEC SUCCES")
        print("=" * 70)
        print("\nProchaine etape: Tester l'API Analytics")
        print("   python main.py")
        print("   puis: http://localhost:8000/api/v1/analytics/overview")

        return True

    except Exception as e:
        print(f"\nERREUR: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    success = generate_statistics()
    exit(0 if success else 1)
