# Initialize Database - Phase 5 C5
from src.repositories.property_repository import PropertyRepository

def main():
    """Créer les tables de la base de données"""
    print("Création des tables de la base de données...")

    # Créer le repository et les tables
    repo = PropertyRepository()
    repo.create_tables()

    print(" Tables créées avec succès!")
    print(" Base de données prête pour l'API REST")

if __name__ == "__main__":
    main()