# Créer la table proprietes_anonymisees
import sqlite3

def create_property_table():
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

    # Créer les index
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_location ON proprietes_anonymisees (code_postal, ville)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_price_surface ON proprietes_anonymisees (prix_euros, surface_m2)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_source_session ON proprietes_anonymisees (source_collecte, date_collecte)')

    conn.commit()
    conn.close()

    print(" Table 'proprietes_anonymisees' créée avec succès!")

if __name__ == "__main__":
    create_property_table()