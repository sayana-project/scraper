# Models Package (C4) - Base de données RGPD
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Index, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Property(Base):
    """Modèle principal pour les propriétés immobilières (C4)"""
    __tablename__ = 'proprietes_anonymisees'

    # Clé primaire
    id_prop = Column(Integer, primary_key=True, index=True)

    # Informations essentielles (noms réels des colonnes)
    surface_m2 = Column(Integer, nullable=False, index=True)
    prix_euros = Column(Integer, nullable=False, index=True)
    prix_m2_euros = Column(Float, nullable=False, index=True)

    # Localisation (anonymisée quartier pour RGPD)
    code_postal = Column(String(5), nullable=False, index=True)
    ville = Column(String(100), nullable=False, index=True)
    quartier_anonymise = Column(String(50), nullable=True, index=True)

    # Métadonnées
    type_bien = Column(String(50), nullable=False)
    source_collecte = Column(String(20), nullable=False)  # seloger, leboncoin, csv, insee
    date_collecte = Column(Date, nullable=False)
    date_anonymisation = Column(DateTime, nullable=True)
    mois_annee = Column(String(7), nullable=False)
    created_at = Column(DateTime, nullable=False)

    # Contraintes
    __table_args__ = (
        CheckConstraint('prix_euros >= 0', name='check_price_positive'),
        CheckConstraint('surface_m2 > 0', name='check_surface_positive'),
        Index('idx_location', 'code_postal', 'ville'),
        Index('idx_price_surface', 'prix_euros', 'surface_m2'),
        Index('idx_source_session', 'source_collecte', 'date_collecte'),
    )

    @property
    def price_per_m2(self) -> float:
        """Calcule le prix au mètre carré"""
        if self.surface_m2 > 0:
            return self.prix_euros / self.surface_m2
        return 0.0

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour l'API"""
        return {
            'id': self.id_prop,
            'title': self.quartier_anonymise,
            'price': self.prix_euros,
            'surface': self.surface_m2,
            'price_per_m2': round(self.price_per_m2, 2),
            'postal_code': self.code_postal,
            'city': self.ville,
            'source': self.source_collecte,
            'scraped_at': self.date_anonymisation.isoformat() if self.date_anonymisation else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
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