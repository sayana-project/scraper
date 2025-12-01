# Health Check Route (C5)
from fastapi import APIRouter
from src.repositories.property_repository import PropertyRepository

router = APIRouter()

@router.get("/health")
async def health_check():
    """Vérification de santé de l'API"""

    # Initialiser la base de données si nécessaire
    try:
        repo = PropertyRepository()
        repo.create_tables()
        db_status = "initialized"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {"status": "healthy", "version": "1.0.0", "database": db_status}# Force restart
