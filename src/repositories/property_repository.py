# Property Repository (C2) - Requêtes SQL optimisées
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, func, and_, or_, desc, asc, text
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
import statistics

from src.models import Property, DemographicData, AggregatedProperty

logger = logging.getLogger(__name__)

class PropertyRepository:
    """Repository Pattern pour les requêtes SQL optimisées (C2)"""

    def __init__(self, database_url: str = "sqlite:///data/immobilier.db"):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        """Crée une session de base de données"""
        return self.SessionLocal()

    def create_tables(self):
        """Crée les tables de la base de données"""
        from src.models import Base
        Base.metadata.create_all(bind=self.engine)
        logger.info("Tables créées avec succès")

    # ===== REQUÊTES SIMPLES (C2) =====

    def get_by_id(self, property_id: int) -> Optional[Property]:
        """Récupère une propriété par ID (requête simple)"""
        with self.get_session() as session:
            return session.query(Property).filter(Property.id == property_id).first()

    def get_all(self, limit: int = 100) -> List[Property]:
        """Récupère toutes les propriétés (requête simple)"""
        with self.get_session() as session:
            return session.query(Property).limit(limit).all()

    # ===== REQUÊTES AVEC FILTRAGE (C2) =====

    def get_by_city(self, city: str, limit: int = 50) -> List[Property]:
        """Requête optimisée pour les propriétés par ville"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(Property.city.ilike(f'%{city}%'))\
                .order_by(desc(Property.price))\
                .limit(limit)\
                .all()

    def get_by_postal_code(self, postal_code: str, limit: int = 50) -> List[Property]:
        """Requête optimisée pour les propriétés par code postal"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(Property.postal_code == postal_code)\
                .order_by(desc(Property.price))\
                .limit(limit)\
                .all()

    def get_by_price_range(self, min_price: int, max_price: int, limit: int = 50) -> List[Property]:
        """Requête optimisée pour les propriétés par plage de prix"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(and_(Property.price >= min_price, Property.price <= max_price))\
                .order_by(asc(Property.price))\
                .limit(limit)\
                .all()

    def get_by_surface_range(self, min_surface: int, max_surface: int, limit: int = 50) -> List[Property]:
        """Requête optimisée pour les propriétés par plage de surface"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(and_(Property.surface >= min_surface, Property.surface <= max_surface))\
                .order_by(desc(Property.surface))\
                .limit(limit)\
                .all()

    # ===== REQUÊTES COMPLEXES (C2) =====

    def get_by_location_and_price(self, city: str, min_price: int, max_price: int,
                                limit: int = 50) -> List[Property]:
        """Requête complexe avec localisation et prix (JOINTURES INDEX)"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(and_(
                    Property.city.ilike(f'%{city}%'),
                    Property.price >= min_price,
                    Property.price <= max_price
                ))\
                .order_by(desc(Property.price))\
                .limit(limit)\
                .all()

    def get_properties_with_demographics(self, city: str = None) -> List[Dict[str, Any]]:
        """Requête complexe avec jointure sur données démographiques (JOIN)"""
        with self.get_session() as session:
            query = session.query(
                Property,
                DemographicData.population,
                (Property.price / Property.surface).label('price_per_m2')
            ).outerjoin(
                DemographicData,
                and_(
                    Property.postal_code == DemographicData.postal_code,
                    Property.city == DemographicData.city
                )
            )

            if city:
                query = query.filter(Property.city.ilike(f'%{city}%'))

            results = query.order_by(desc(Property.price)).limit(100).all()

            return [
                {
                    'property': prop.to_dict(),
                    'population': demo,
                    'price_per_m2': round(price_m2, 2)
                }
                for prop, demo, price_m2 in results
            ]

    # ===== REQUÊTES AVEC AGRÉGATION (C2) =====

    def get_statistics_by_city(self, city: str = None) -> List[Dict[str, Any]]:
        """Requête avec agrégation GROUP BY par ville (C2)"""
        with self.get_session() as session:
            query = session.query(
                Property.city,
                Property.postal_code,
                func.count(Property.id).label('total_properties'),
                func.avg(Property.price).label('avg_price'),
                func.min(Property.price).label('min_price'),
                func.max(Property.price).label('max_price'),
                func.avg(Property.surface).label('avg_surface')
            )

            if city:
                query = query.filter(Property.city.ilike(f'%{city}%'))

            results = query.group_by(Property.city, Property.postal_code).all()

            return [
                {
                    'city': city_name,
                    'postal_code': postal_code,
                    'total_properties': total,
                    'avg_price': round(float(avg_price), 2),
                    'min_price': min_price,
                    'max_price': max_price,
                    'avg_surface': round(float(avg_surface), 2)
                }
                for city_name, postal_code, total, avg_price, min_price, max_price, avg_surface in results
            ]

    def get_price_per_m2_distribution(self, city: str = None) -> List[Dict[str, Any]]:
        """Requête complexe pour distribution prix/m² par ville"""
        with self.get_session() as session:
            query = session.query(
                Property.city,
                func.avg(Property.price / Property.surface).label('avg_price_per_m2'),
                func.count(Property.id).label('property_count')
            )

            if city:
                query = query.filter(Property.city.ilike(f'%{city}%'))

            results = query.group_by(Property.city).order_by(desc('avg_price_per_m2')).all()

            return [
                {
                    'city': city_name,
                    'avg_price_per_m2': round(float(avg_price_m2), 2),
                    'property_count': count
                }
                for city_name, avg_price_m2, count in results
            ]

    # ===== REQUÊTES AVEC SOUS-REQUÊTES (C2) =====

    def get_properties_above_avg_price(self, city: str = None) -> List[Property]:
        """Requête avec sous-requête pour propriétés au-dessus moyenne"""
        with self.get_session() as session:
            avg_price_subquery = session.query(func.avg(Property.price))
            if city:
                avg_price_subquery = avg_price_subquery.filter(Property.city.ilike(f'%{city}%'))

            return session.query(Property)\
                .filter(and_(
                    Property.price > avg_price_subquery,
                    Property.city.ilike(f'%{city}%') if city else True
                ))\
                .order_by(desc(Property.price))\
                .all()

    # ===== MÉTHODES DE MANIPULATION (C2) =====

    def insert_properties(self, properties: List[Dict[str, Any]]) -> int:
        """Insertion en masse optimisée (BULK INSERT)"""
        with self.get_session() as session:
            property_objects = [
                Property(
                    title=prop.get('title'),
                    price=prop.get('price', 0),
                    surface=prop.get('surface', 1),
                    postal_code=prop.get('postal_code'),
                    city=prop.get('city'),
                    source=prop.get('source'),
                    scraped_at=datetime.fromisoformat(prop.get('scraped_at', datetime.now().isoformat()))
                )
                for prop in properties
                if prop.get('title') and prop.get('price') and prop.get('surface')
            ]

            session.bulk_save_objects(property_objects)
            session.commit()

            logger.info(f"Inséré {len(property_objects)} propriétés")
            return len(property_objects)

    def insert_demographic_data(self, demo_data: List[Dict[str, Any]]) -> int:
        """Insertion en masse de données démographiques"""
        with self.get_session() as session:
            demo_objects = [
                DemographicData(
                    postal_code=record.get('postal_code'),
                    city=record.get('city'),
                    population=record.get('population', 0),
                    source=record.get('source', 'insee'),
                    scraped_at=datetime.fromisoformat(record.get('scraped_at', datetime.now().isoformat()))
                )
                for record in demo_data
                if record.get('city')
            ]

            session.bulk_save_objects(demo_objects)
            session.commit()

            logger.info(f"Inséré {len(demo_objects)} enregistrements démographiques")
            return len(demo_objects)

    # ===== REQUÊTES D'ANALYSE (C2) =====

    def get_market_analysis(self) -> Dict[str, Any]:
        """Requête complexe pour analyse du marché immobilier"""
        with self.get_session() as session:
            # Statistiques générales
            general_stats = session.query(
                func.count(Property.id).label('total_properties'),
                func.avg(Property.price).label('avg_price'),
                func.avg(Property.surface).label('avg_surface')
            ).first()

            # Top 10 des villes les plus chères
            expensive_cities = session.query(
                Property.city,
                func.avg(Property.price).label('avg_price'),
                func.count(Property.id).label('property_count')
            ).group_by(Property.city)\
             .order_by(desc('avg_price'))\
             .limit(10)\
             .all()

            # Distribution par source
            source_stats = session.query(
                Property.source,
                func.count(Property.id).label('count')
            ).group_by(Property.source)\
             .order_by(desc('count'))\
             .all()

            return {
                'general_stats': {
                    'total_properties': general_stats.total_properties or 0,
                    'avg_price': round(float(general_stats.avg_price or 0), 2),
                    'avg_surface': round(float(general_stats.avg_surface or 0), 2)
                },
                'expensive_cities': [
                    {'city': city, 'avg_price': round(float(avg_price), 2), 'count': count}
                    for city, avg_price, count in expensive_cities
                ],
                'source_distribution': [
                    {'source': source, 'count': count}
                    for source, count in source_stats
                ]
            }

    def close(self):
        """Ferme la connexion à la base de données"""
        self.engine.dispose()