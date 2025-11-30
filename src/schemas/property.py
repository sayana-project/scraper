# Property DTOs (C5)
from pydantic import BaseModel, validator
from datetime import datetime

class PropertyBase(BaseModel):
    title: str
    price: int
    surface: int
    postal_code: str
    city: str

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

    @validator('surface')
    def surface_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Surface must be positive')
        return v

class PropertyCreate(PropertyBase):
    """DTO pour créer une propriété"""
    pass

class PropertyResponse(PropertyBase):
    """DTO pour retourner une propriété"""
    id: int
    price_per_m2: float
    created_at: datetime

    class Config:
        from_attributes = True

class PropertyAnalytics(BaseModel):
    """DTO pour les statistiques"""
    city: str
    average_price_per_m2: float
    total_properties: int
    min_price: int
    max_price: int