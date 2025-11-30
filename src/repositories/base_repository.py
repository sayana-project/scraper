# Base Repository (C2)
from sqlalchemy.orm import Session
from typing import List, Type, TypeVar

ModelType = TypeVar("ModelType")

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, model: Type[ModelType], id: int):
        return self.db.query(model).filter(model.id == id).first()

    def get_all(self, model: Type[ModelType]) -> List[ModelType]:
        return self.db.query(model).all()

    def create(self, obj: ModelType):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj