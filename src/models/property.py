# Property SQLAlchemy Model (C4)
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    surface = Column(Integer, nullable=False)
    price_per_m2 = Column(Float, nullable=False)
    postal_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)