# Property Repository (C2)
from sqlalchemy.orm import Session
from typing import List
from src.models.property import Property
from src.repositories.base_repository import BaseRepository

class PropertyRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_city(self, city: str) -> List[Property]:
        return self.db.query(Property).filter(Property.city == city).all()

    def get_by_postal_code(self, postal_code: str) -> List[Property]:
        return self.db.query(Property).filter(Property.postal_code == postal_code).all()

    def create_property(self, property_obj: Property) -> Property:
        return self.create(property_obj)