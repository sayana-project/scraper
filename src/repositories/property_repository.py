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

    def __init__(self, database_url: str = "sqlite:///data/immobilier_rgpd.db"):
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
            return session.query(Property).filter(Property.id_prop == property_id).first()

    def get_all(self, limit: int = 100) -> List[Property]:
        """Récupère toutes les propriétés (requête simple)"""
        with self.get_session() as session:
            return session.query(Property).limit(limit).all()

    # ===== REQUÊTES AVEC FILTRAGE (C2) =====

    def get_by_city(self, city: str, limit: int = 50) -> List[Property]:
        """Requête optimisée pour les propriétés par ville"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(Property.ville.ilike(f'%{city}%'))\
                .order_by(desc(Property.prix_euros))\
                .limit(limit)\
                .all()

    def get_by_postal_code(self, postal_code: str, limit: int = 50) -> List[Property]:
        """Requête optimisée pour les propriétés par code postal"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(Property.code_postal == postal_code)\
                .order_by(desc(Property.prix_euros))\
                .limit(limit)\
                .all()

    def get_by_price_range(self, min_price: int, max_price: int, limit: int = 50) -> List[Property]:
        """Requête optimisée pour les propriétés par plage de prix"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(and_(Property.prix_euros >= min_price, Property.prix_euros <= max_price))\
                .order_by(asc(Property.prix_euros))\
                .limit(limit)\
                .all()

    def get_by_surface_range(self, min_surface: int, max_surface: int, limit: int = 50) -> List[Property]:
        """Requête optimisée pour les propriétés par plage de surface"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(and_(Property.surface_m2_m2 >= min_surface, Property.surface_m2_m2 <= max_surface))\
                .order_by(desc(Property.surface_m2_m2))\
                .limit(limit)\
                .all()

    # ===== REQUÊTES COMPLEXES (C2) =====

    def get_by_location_and_price(self, city: str, min_price: int, max_price: int,
                                limit: int = 50) -> List[Property]:
        """Requête complexe avec localisation et prix (JOINTURES INDEX)"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(and_(
                    Property.ville.ilike(f'%{city}%'),
                    Property.prix_euros >= min_price,
                    Property.prix_euros <= max_price
                ))\
                .order_by(desc(Property.prix_euros))\
                .limit(limit)\
                .all()

    def get_properties_with_demographics(self, city: str = None) -> List[Dict[str, Any]]:
        """Requête complexe avec jointure sur données démographiques (JOIN)"""
        with self.get_session() as session:
            query = session.query(
                Property,
                DemographicData.population,
                (Property.prix_euros / Property.surface_m2_m2).label('price_per_m2')
            ).outerjoin(
                DemographicData,
                and_(
                    Property.code_postal == DemographicData.postal_code,
                    Property.ville == DemographicData.city
                )
            )

            if city:
                query = query.filter(Property.ville.ilike(f'%{city}%'))

            results = query.order_by(desc(Property.prix_euros)).limit(100).all()

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
                Property.ville,
                Property.code_postal,
                func.count(Property.id_prop).label('total_properties'),
                func.avg(Property.prix_euros).label('avg_price'),
                func.min(Property.prix_euros).label('min_price'),
                func.max(Property.prix_euros).label('max_price'),
                func.avg(Property.surface_m2_m2).label('avg_surface')
            )

            if city:
                query = query.filter(Property.ville.ilike(f'%{city}%'))

            results = query.group_by(Property.ville, Property.code_postal).all()

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
                Property.ville,
                func.avg(Property.prix_euros / Property.surface_m2).label('avg_price_per_m2'),
                func.count(Property.id_prop).label('property_count')
            )

            if city:
                query = query.filter(Property.ville.ilike(f'%{city}%'))

            results = query.group_by(Property.ville).order_by(desc('avg_price_per_m2')).all()

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
            avg_price_subquery = session.query(func.avg(Property.prix_euros))
            if city:
                avg_price_subquery = avg_price_subquery.filter(Property.ville.ilike(f'%{city}%'))

            return session.query(Property)\
                .filter(and_(
                    Property.prix_euros > avg_price_subquery,
                    Property.ville.ilike(f'%{city}%') if city else True
                ))\
                .order_by(desc(Property.prix_euros))\
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
                func.count(Property.id_prop).label('total_properties'),
                func.avg(Property.prix_euros).label('avg_price'),
                func.avg(Property.surface_m2_m2).label('avg_surface')
            ).first()

            # Top 10 des villes les plus chères
            expensive_cities = session.query(
                Property.ville,
                func.avg(Property.prix_euros).label('avg_price'),
                func.count(Property.id_prop).label('property_count')
            ).group_by(Property.ville)\
             .order_by(desc('avg_price'))\
             .limit(10)\
             .all()

            # Distribution par source
            source_stats = session.query(
                Property.source_collecte,
                func.count(Property.id_prop).label('count')
            ).group_by(Property.source_collecte)\
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

    def get_city_analytics(self, city: str) -> Optional[Dict[str, Any]]:
        """Obtenir les statistiques analytiques pour une ville spécifique"""
        with self.get_session() as session:
            # Vérifier si la ville existe dans la base
            city_properties = session.query(Property).filter(Property.ville.ilike(f'%{city}%')).all()

            if not city_properties:
                return None

            # Calculer les statistiques
            total_properties = len(city_properties)
            prices = [p.prix_euros for p in city_properties]
            surfaces = [p.surface_m2 for p in city_properties]
            prices_per_m2 = [p.prix_euros / p.surface_m2 for p in city_properties]

            return {
                'city': city,
                'total_properties': total_properties,
                'min_price': min(prices),
                'max_price': max(prices),
                'average_price_per_m2': round(sum(prices_per_m2) / len(prices_per_m2), 2),
                'price_q1': round(sorted(prices)[len(prices)//4], 2),
                'price_median': round(sorted(prices)[len(prices)//2], 2),
                'price_q3': round(sorted(prices)[3*len(prices)//4], 2),
                'surface_q1': round(sorted(surfaces)[len(surfaces)//4], 2),
                'surface_median': round(sorted(surfaces)[len(surfaces)//2], 2),
                'surface_q3': round(sorted(surfaces)[3*len(surfaces)//4], 2)
            }

    def get_properties(self, skip: int = 0, limit: int = 100,
                       city: Optional[str] = None,
                       min_price: Optional[int] = None,
                       max_price: Optional[int] = None) -> List[Dict[str, Any]]:
        """Lister les propriétés avec filtres optionnels"""
        with self.get_session() as session:
            query = session.query(Property)

            # Appliquer les filtres
            if city:
                query = query.filter(Property.ville.ilike(f'%{city}%'))

            if min_price is not None:
                query = query.filter(Property.prix_euros >= min_price)

            if max_price is not None:
                query = query.filter(Property.prix_euros <= max_price)

            # Appliquer pagination et ordre
            properties = query.offset(skip).limit(limit).all()

            # Convertir en dictionnaires en utilisant la méthode to_dict() du modèle
            return [prop.to_dict() for prop in properties]

    def get_available_cities(self) -> List[str]:
        """Lister toutes les villes disponibles dans la base de données"""
        with self.get_session() as session:
            cities = session.query(Property.ville).distinct().all()
            return [city[0] for city in cities if city[0]]

    def get_overview_analytics(self) -> Dict[str, Any]:
        """Statistiques générales sur toutes les propriétés"""
        with self.get_session() as session:
            # Statistiques générales
            total_properties = session.query(func.count(Property.id_prop)).scalar() or 0

            if total_properties == 0:
                return {
                    'city': 'Toutes villes',
                    'total_properties': 0,
                    'min_price': 0,
                    'max_price': 0,
                    'average_price_per_m2': 0
                }

            # Prix et surfaces
            price_stats = session.query(
                func.min(Property.prix_euros).label('min_price'),
                func.max(Property.prix_euros).label('max_price'),
                func.avg(Property.prix_euros).label('avg_price')
            ).first()

            # Prix au m² moyen
            price_per_m2_avg = session.query(
                func.avg(Property.prix_euros / Property.surface_m2)
            ).scalar() or 0

            return {
                'city': 'Toutes villes',
                'total_properties': total_properties,
                'min_price': int(price_stats.min_price or 0),
                'max_price': int(price_stats.max_price or 0),
                'average_price_per_m2': round(float(price_per_m2_avg), 2)
            }

    # ===== MÉTHODES MANQUANTES POUR L'API (C5) =====

    def get_property_by_id(self, property_id: int) -> Optional[Dict[str, Any]]:
        """Récupère une propriété par ID et retourne un dictionnaire"""
        with self.get_session() as session:
            property = session.query(Property).filter(Property.id_prop == property_id).first()
            if property:
                return property.to_dict()
            return None

    def update_property(self, property_id: int, property_update: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Met à jour une propriété par ID"""
        with self.get_session() as session:
            property = session.query(Property).filter(Property.id_prop == property_id).first()
            if property:
                if property_update.get('title'):
                    property.quartier_anonymise = property_update['title']
                if property_update.get('price'):
                    property.prix_euros = property_update['price']
                if property_update.get('surface'):
                    property.surface_m2 = property_update['surface']
                if property_update.get('postal_code'):
                    property.code_postal = property_update['postal_code']
                if property_update.get('city'):
                    property.ville = property_update['city']
                if property_update.get('source'):
                    property.source_collecte = property_update['source']

                session.commit()
                session.refresh(property)

                return property.to_dict()
            return None

    def delete_property(self, property_id: int) -> bool:
        """Supprime une propriété par ID"""
        with self.get_session() as session:
            property = session.query(Property).filter(Property.id_prop == property_id).first()
            if property:
                session.delete(property)
                session.commit()
                return True
            return False

    def close(self):
        """Ferme la connexion à la base de données"""
        self.engine.dispose()