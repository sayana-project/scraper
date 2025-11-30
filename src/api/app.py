# FastAPI Application (C5)
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models.database import get_db
from src.repositories.property_repository import PropertyRepository
from src.services.property_service import PropertyService
from src.schemas.property import PropertyCreate, PropertyResponse, PropertyAnalytics
from sqlalchemy.orm import Session

app = FastAPI(
    title="Observatoire Immobilier API",
    description="API REST pour l'observatoire immobilier public",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection
def get_property_service(db: Session = Depends(get_db)) -> PropertyService:
    repository = PropertyRepository(db)
    return PropertyService(repository)

@app.post("/properties/", response_model=PropertyResponse)
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

@app.get("/analytics/{city}", response_model=PropertyAnalytics)
async def get_city_analytics(
    city: str,
    service: PropertyService = Depends(get_property_service)
):
    """Obtenir les statistiques par ville"""
    analytics = service.get_city_analytics(city)
    if not analytics:
        raise HTTPException(status_code=404, detail="City not found")
    return analytics

@app.get("/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)