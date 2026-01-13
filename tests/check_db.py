# Vérifier la base de données avec SQLAlchemy
from src.repositories.property_repository import PropertyRepository

def check_database():
    """Vérifier les tables dans la base de données"""

    repo = PropertyRepository()

    # Créer les tables avec SQLAlchemy (qui gère les conflits)
    try:
        repo.create_tables()
        print("Tables créées ou vérifiées avec SQLAlchemy")
    except Exception as e:
        print(f"Erreur lors de la création des tables: {e}")

    # Vérifier si la table existe
    from sqlalchemy import text
    with repo.get_session() as session:
        try:
            # Essayer une requête simple avec text()
            result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result.fetchall()]
            print(f"Tables found: {tables}")

            # Vérifier si la table proprietes_anonymisees existe
            if 'proprietes_anonymisees' in tables:
                count = session.execute(text("SELECT COUNT(*) FROM proprietes_anonymisees")).scalar()
                print(f"Properties in database: {count}")
            else:
                print("Table 'proprietes_anonymisees' does not exist")

        except Exception as e:
            print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_database()