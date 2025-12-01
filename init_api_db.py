# Initialiser la base de données pour l'API
import sqlite3

def init_database():
    """Créer la table proprietes_anonymisees si elle n'existe pas"""

    conn = sqlite3.connect('data/immobilier_rgpd.db')
    cursor = conn.cursor()

    # Créer la table proprietes_anonymisees
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS proprietes_anonymisees (
        id_prop INTEGER PRIMARY KEY AUTOINCREMENT,
        surface_m2 INTEGER NOT NULL,
        prix_euros INTEGER NOT NULL,
        prix_m2_euros REAL NOT NULL,
        code_postal VARCHAR(5) NOT NULL,
        ville VARCHAR(100) NOT NULL,
        quartier_anonymise VARCHAR(50),
        type_bien VARCHAR(50) NOT NULL,
        source_collecte VARCHAR(20) NOT NULL,
        date_collecte DATE NOT NULL,
        date_anonymisation DATETIME,
        mois_annee VARCHAR(7) NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

    print("✅ Table 'proprietes_anonymisees' créée dans data/immobilier_rgpd.db!")

if __name__ == "__main__":
    init_database()