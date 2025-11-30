# Models Package (C4) - Base de données RGPD
from sqlalchemy import Column, Integer, String, Float, DateTime, Index, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Property(Base):
    """Modèle principal pour les propriétés immobilières (C4)"""
    __tablename__ = 'properties'

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # Informations essentielles
    title = Column(String(255), nullable=False, index=True)
    price = Column(Integer, nullable=False, index=True)
    surface = Column(Integer, nullable=False, index=True)

    # Localisation (anonymisée quartier pour RGPD)
    postal_code = Column(String(5), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)

    # Métadonnées
    source = Column(String(50), nullable=False)  # seloger, leboncoin, csv, insee
    scraped_at = Column(DateTime, nullable=False)
    scraping_session = Column(String(50))

    # Contraintes
    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_positive'),
        CheckConstraint('surface > 0', name='check_surface_positive'),
        Index('idx_location', 'postal_code', 'city'),
        Index('idx_price_surface', 'price', 'surface'),
        Index('idx_source_session', 'source', 'scraping_session'),
    )

    @property
    def price_per_m2(self) -> float:
        """Calcule le prix au mètre carré"""
        if self.surface > 0:
            return self.price / self.surface
        return 0.0

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'surface': self.surface,
            'price_per_m2': round(self.price_per_m2, 2),
            'postal_code': self.postal_code,
            'city': self.city,
            'source': self.source,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
        }

class DemographicData(Base):
    """Modèle pour les données démographiques INSEE (C4)"""
    __tablename__ = 'demographic_data'

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # Localisation
    postal_code = Column(String(5), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)

    # Données démographiques
    population = Column(Integer, nullable=True, index=True)

    # Métadonnées
    source = Column(String(50), nullable=False, default='insee')
    scraped_at = Column(DateTime, nullable=False)

    # Contraintes
    __table_args__ = (
        CheckConstraint('population >= 0', name='check_population_positive'),
        Index('idx_demo_location', 'postal_code', 'city'),
        Index('idx_demo_population', 'population'),
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'postal_code': self.postal_code,
            'city': self.city,
            'population': self.population,
            'source': self.source,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
        }

class AggregatedProperty(Base):
    """Modèle pour les données agrégées (C3)"""
    __tablename__ = 'aggregated_properties'

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # Localisation agrégée
    postal_code = Column(String(5), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)

    # Statistiques agrégées
    total_properties = Column(Integer, nullable=False, index=True)
    avg_price = Column(Float, nullable=False, index=True)
    min_price = Column(Integer, nullable=False)
    max_price = Column(Integer, nullable=False)
    avg_surface = Column(Float, nullable=False)
    avg_price_per_m2 = Column(Float, nullable=False)

    # Sources agrégées
    sources_count = Column(Integer, nullable=False)
    sources_list = Column(String(255))  # CSV des sources

    # Métadonnées
    aggregation_date = Column(DateTime, nullable=False, index=True)
    data_period_start = Column(DateTime, nullable=False)
    data_period_end = Column(DateTime, nullable=False)

    # Contraintes
    __table_args__ = (
        CheckConstraint('total_properties >= 0', name='check_total_properties'),
        CheckConstraint('avg_price >= 0', name='check_avg_price'),
        CheckConstraint('sources_count >= 0', name='check_sources_count'),
        Index('idx_aggregated_location', 'postal_code', 'city'),
        Index('idx_aggregated_stats', 'avg_price', 'avg_price_per_m2'),
        Index('idx_aggregated_date', 'aggregation_date'),
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'postal_code': self.postal_code,
            'city': self.city,
            'total_properties': self.total_properties,
            'avg_price': round(self.avg_price, 2),
            'min_price': self.min_price,
            'max_price': self.max_price,
            'avg_surface': round(self.avg_surface, 2),
            'avg_price_per_m2': round(self.avg_price_per_m2, 2),
            'sources_count': self.sources_count,
            'sources_list': self.sources_list.split(',') if self.sources_list else [],
            'aggregation_date': self.aggregation_date.isoformat() if self.aggregation_date else None,
        }