# Analytics Routes (C5)
from fastapi import APIRouter, Depends, HTTPException
from typing import List
# from sqlalchemy.orm import Session
# from src.models.database import get_db
from src.repositories.property_repository import PropertyRepository
from src.services.property_service import PropertyService
from src.schemas.property import PropertyAnalytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_property_service() -> PropertyService:
    """Injection du service Property"""
    database_url = "sqlite:///data/immobilier_rgpd.db"
    return PropertyService(database_url)

@router.get("/city/{city}", response_model=PropertyAnalytics)
async def get_city_analytics(
    city: str,
    service: PropertyService = Depends(get_property_service)
):
    """Obtenir les statistiques par ville"""
    analytics = service.get_city_analytics(city)
    if not analytics:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    return analytics

@router.get("/cities", response_model=List[str])
async def get_available_cities(
    service: PropertyService = Depends(get_property_service)
):
    """Lister les villes disponibles dans les données"""
    cities = service.get_available_cities()
    return cities

@router.get("/overview", response_model=PropertyAnalytics)
async def get_overview_analytics(
    service: PropertyService = Depends(get_property_service)
):
    """Statistiques générales sur toutes les propriétés"""
    overview = service.get_overview_analytics()
    return overview