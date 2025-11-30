# Property Service (C3)
from typing import List, Optional
from datetime import datetime
from src.models.property import Property
from src.repositories.property_repository import PropertyRepository
from src.schemas.property import PropertyCreate, PropertyAnalytics

class PropertyService:
    def __init__(self, prop_repo: PropertyRepository):
        self.prop_repo = prop_repo

    def calculate_price_per_m2(self, price: int, surface: int) -> float:
        """Calcule le prix au m²"""
        if surface <= 0:
            raise ValueError("Surface must be positive")
        return round(price / surface, 2)

    def create_property(self, property_data: PropertyCreate) -> Property:
        """Crée une nouvelle propriété avec calcul du prix au m²"""
        price_per_m2 = self.calculate_price_per_m2(property_data.price, property_data.surface)

        property_obj = Property(
            title=property_data.title,
            price=property_data.price,
            surface=property_data.surface,
            price_per_m2=price_per_m2,
            postal_code=property_data.postal_code,
            city=property_data.city,
            created_at=datetime.now()
        )

        return self.prop_repo.create_property(property_obj)

    def get_average_price_by_city(self, city: str) -> float:
        """Calcule le prix moyen au m² par ville"""
        properties = self.prop_repo.get_by_city(city)
        if not properties:
            return 0.0

        total_price_m2 = sum(prop.price_per_m2 for prop in properties)
        return round(total_price_m2 / len(properties), 2)

    def get_city_analytics(self, city: str) -> Optional[PropertyAnalytics]:
        """Génère les statistiques pour une ville"""
        properties = self.prop_repo.get_by_city(city)
        if not properties:
            return None

        prices = [prop.price for prop in properties]
        return PropertyAnalytics(
            city=city,
            average_price_per_m2=self.get_average_price_by_city(city),
            total_properties=len(properties),
            min_price=min(prices),
            max_price=max(prices)
        )