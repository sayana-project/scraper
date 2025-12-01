# Initialisation Base de Données pour l'API REST (C5)
from fastapi import APIRouter
from src.repositories.property_repository import PropertyRepository

router = APIRouter()

@router.post("/init-database", status_code=201)
async def init_database():
    """Initialiser la base de données avec les tables manquantes (C5)"""
    try:
        # Créer le repository et les tables
        repo = PropertyRepository()
        repo.create_tables()

        return {
            "message": "Base de données initialisée avec succès",
            "tables_created": [
                "proprietes_anonymisees",
                "demographic_data",
                "aggregated_properties"
            ]
        }
    except Exception as e:
        return {
            "message": f"Erreur lors de l'initialisation: {str(e)}",
            "status": "error"
        }