# Properties CRUD Routes (C5)
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
# from sqlalchemy.orm import Session
# from src.models.database import get_db
from src.repositories.property_repository import PropertyRepository
from src.services.property_service import PropertyService
from src.schemas.property import PropertyCreate, PropertyResponse, PropertyAnalytics

router = APIRouter(prefix="/properties", tags=["Propriétés"])

def get_property_service() -> PropertyService:
    """Injection du service Property"""
    database_url = "sqlite:///data/immobilier_rgpd.db"
    return PropertyService(database_url)

@router.post("/", response_model=PropertyResponse, status_code=201)
async def create_property(
    property: PropertyCreate,
    service: PropertyService = Depends(get_property_service)
):
    """Créer une nouvelle propriété"""
    try:
        created_property = service.create_property(property)
        return created_property
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[PropertyResponse])
async def get_properties(
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    service: PropertyService = Depends(get_property_service)
):
    """Lister les propriétés avec filtres optionnels"""
    try:
        properties = service.get_properties(
            skip=skip,
            limit=limit,
            city=city,
            min_price=min_price,
            max_price=max_price
        )
        return properties
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property_by_id(
    property_id: int,
    service: PropertyService = Depends(get_property_service)
):
    """Récupérer une propriété par son ID"""
    property = service.get_property_by_id(property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: int,
    property_update: PropertyCreate,
    service: PropertyService = Depends(get_property_service)
):
    """Mettre à jour une propriété"""
    try:
        updated_property = service.update_property(property_id, property_update)
        if not updated_property:
            raise HTTPException(status_code=404, detail="Property not found")
        return updated_property
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{property_id}", status_code=204)
async def delete_property(
    property_id: int,
    service: PropertyService = Depends(get_property_service)
):
    """Supprimer une propriété"""
    deleted = service.delete_property(property_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Property not found")