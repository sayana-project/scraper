# Guide Technique Développeur - Observatoire Immobilier Public

##  Table des Matières

1. [Vue d'ensemble de l'architecture](#vue-densemble-de-larchitecture)
2. [Structure du projet](#structure-du-projet)
3. [Installation et configuration](#installation-et-configuration)
4. [Composants techniques](#composants-techniques)
5. [Base de données](#base-de-données)
6. [API REST](#api-rest)
7. [Sécurité](#sécurité)
8. [Tests et qualité](#tests-et-qualité)
9. [Déploiement](#déploiement)
10. [Maintenance et évolution](#maintenance-et-évolution)

---

## Vue d'ensemble de l'architecture

### Architecture en couches

```
┌─────────────────┐
│   Interface     │  FastAPI (Endpoints REST)
│      API        │  OpenAPI/Swagger Documentation
└─────────┬───────┘
          │
┌─────────▼───────┐
│  Service Layer  │  Business Logic (C3)
│   (C3)         │  Data Processing & Aggregation
└─────────┬───────┘
          │
┌─────────▼───────┐
│ Repository      │  Data Access Layer (C2)
│   (C2)         │  SQL Queries & ORM
└─────────┬───────┘
          │
┌─────────▼───────┐
│   Models        │  Database Schema (C4)
│   (C4)         │  GDPR Compliance
└─────────┬───────┘
          │
┌─────────▼───────┐
│  Data Sources   │  Scrapers & APIs (C1)
│   (C1)         │  Multi-source Collection
└─────────────────┘
```

### Patterns utilisés

- **Repository Pattern** : Abstraction de l'accès aux données
- **Service Layer** : Logique métier isolée
- **DTO (Data Transfer Objects)** : Validation avec Pydantic
- **Dependency Injection** : Injection via FastAPI
- **Strategy Pattern** : Scrapers modulaires par source

---

## Structure du projet

```
observatoire-immobilier/
├── src/                          # Source code principal
│   ├── api/                       # API REST (C5)
│   │   ├── app.py                 # Application FastAPI principale
│   │   ├── routes/                # Routes organisées par fonction
│   │   │   ├── __init__.py
│   │   │   ├── properties.py      # CRUD propriétés
│   │   │   ├── analytics.py       # Statistiques et analyses
│   │   │   ├── auth.py           # Authentification JWT
│   │   │   └── health.py         # Health checks
│   │   └── dependencies.py       # Injection dépendances
│   ├── scrapers/                 # Collection données (C1)
│   │   ├── __init__.py
│   │   ├── base_scraper.py       # Classe abstraite scraping
│   │   ├── seloger_scraper.py    # Spécialisation SeLoger
│   │   ├── leboncoin_scraper.py  # Spécialisation LeBonCoin
│   │   └── insee_client.py       # Client API INSEE
│   ├── repositories/              # Accès données (C2)
│   │   ├── __init__.py
│   │   └── property_repository.py
│   ├── services/                  # Logique métier (C3)
│   │   ├── __init__.py
│   │   └── property_service.py
│   ├── models/                    # Modèles BDD (C4)
│   │   ├── __init__.py
│   │   └── database.py           # Configuration SQLAlchemy
│   ├── schemas/                   # DTOs Pydantic (C5)
│   │   ├── __init__.py
│   │   ├── property.py
│   │   └── user.py
│   ├── utils/                     # Utilitaires
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration application
│   │   ├── auth.py               # Utilitaires authentification
│   │   └── gdpr.py               # Outils conformité RGPD
│   └── database/                 # Scripts BDD
│       ├── __init__.py
│       ├── migrations/            # Scripts migration
│       └── seeds/                # Données initiales
├── data/                         # Données applicatives
│   ├── raw/                      # Données brutes collectées
│   ├── processed/                # Données nettoyées
│   ├── immobilier.db            # BDD développement SQLite
│   └── immobilier_rgpd.db       # BDD production anonymisée
├── logs/                        # Logs application
├── tests/                       # Tests automatisés
│   ├── unit/                     # Tests unitaires
│   ├── integration/              # Tests d'intégration
│   └── e2e/                     # Tests end-to-end
├── docs/                        # Documentation
│   ├── rapport_pro.md            # Rapport professionnel
│   ├── technical_guide.md        # Guide technique (ce fichier)
│   └── api_documentation.md     # Documentation API
├── scripts/                     # Scripts utilitaires
│   ├── setup_database.py        # Initialisation BDD
│   ├── run_scrapers.py          # Lancement collecte
│   └── backup_database.py       # Sauvegardes
├── docker/                      # Configuration Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
├── requirements.txt             # Dépendances Python
├── .env.example                # Variables environnement
├── .gitignore
└── README.md                   # Documentation projet
```

---

## Installation et configuration

### Prérequis

- **Python 3.9+**
- **Git**
- **SQLite** (développement) / **PostgreSQL** (production)
- **Docker** (optionnel, pour déploiement)

### Installation locale

```bash
# 1. Cloner le repository
git clone https://github.com/username/observatoire-immobilier.git
cd observatoire-immobilier

# 2. Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Configurer variables environnement
cp .env.example .env
# Éditer .env avec vos configurations

# 5. Initialiser base de données
python scripts/setup_database.py

# 6. Lancer API développement
uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8001
```

### Configuration environnement

```bash
# .env
# Base de données
DATABASE_URL=sqlite:///data/immobilier_rgpd.db
# DATABASE_URL=postgresql://user:password@localhost:5432/observatoire

# Sécurité
JWT_SECRET_KEY=votre_cle_secrete_jwt_tres_longue_ici
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Observatoire Immobilier API
VERSION=1.0.0
DEBUG=False

# Scraping Configuration
SCRAPING_DELAY_MIN=1
SCRAPING_DELAY_MAX=3
MAX_RETRIES=3

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/observatoire.log

# Monitoring
ENABLE_METRICS=True
METRICS_PORT=9090
```

---

## Composants techniques

### C1 - Collection Multi-Sources

#### Architecture des scrapers

```python
# src/scrapers/base_scraper.py
from abc import ABC, abstractmethod
from typing import List, Optional
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
import random

class BaseScraper(ABC):
    """Classe abstraite pour tous les scrapers"""

    def __init__(self, base_url: str, name: str):
        self.base_url = base_url
        self.name = name
        self.session = None
        self.last_request_time = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers=self._get_headers(),
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @abstractmethod
    async def search_properties(self, criteria: SearchCriteria) -> List[RawProperty]:
        """Méthode abstraite à implémenter"""
        pass

    def _get_headers(self) -> dict:
        """Headers anti-détection"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    async def _make_request(self, url: str) -> Optional[str]:
        """Requête HTTP avec gestion anti-bot"""
        await self._enforce_rate_limit()

        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                elif response.status == 429:
                    retry_after = int(response.headers.get('Retry-After', 5))
                    await asyncio.sleep(retry_after)
                    return await self._make_request(url)
                else:
                    logger.warning(f"HTTP {response.status} pour {url}")
                    return None
        except Exception as e:
            logger.error(f"Erreur requête {url}: {e}")
            return None

    async def _enforce_rate_limit(self):
        """Respect des limites de taux"""
        min_delay = 1  # Secondes entre requêtes
        time_since_last = time.time() - self.last_request_time
        if time_since_last < min_delay:
            await asyncio.sleep(min_delay - time_since_last)
        self.last_request_time = time.time()
```

#### Implémentation SeLoger

```python
# src/scrapers/seloger_scraper.py
from .base_scraper import BaseScraper
from urllib.parse import urljoin, urlencode
from typing import List, Optional
import re
import json

class SeLogerScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.seloger.com", "seloger")

    async def search_properties(self, criteria: SearchCriteria) -> List[RawProperty]:
        """Recherche de propriétés sur SeLoger"""
        properties = []

        # Construction URL de recherche
        search_url = self._build_search_url(criteria)

        # Pagination
        page = 1
        max_pages = 10  # Limite pour éviter surcharge

        while page <= max_pages:
            page_url = f"{search_url}?page={page}"

            html_content = await self._make_request(page_url)
            if not html_content:
                break

            page_properties = self._parse_page(html_content)
            if not page_properties:
                break

            properties.extend(page_properties)
            page += 1

            # Délai entre pages
            await asyncio.sleep(random.uniform(2, 4))

        return properties

    def _build_search_url(self, criteria: SearchCriteria) -> str:
        """Construction URL de recherche SeLoger"""
        params = {
            'idtypebien': self._get_property_type(criteria.property_type),
            'px_1': criteria.min_price or '',
            'px_2': criteria.max_price or '',
            'surf_1': criteria.min_surface or '',
            'surf_2': criteria.max_surface or '',
            'ci': self._get_city_code(criteria.city),
        }

        return f"{self.base_url}/recherche?" + urlencode(params)

    def _parse_page(self, html_content: str) -> List[RawProperty]:
        """Parsing HTML des annonces"""
        soup = BeautifulSoup(html_content, 'html.parser')
        properties = []

        # Sélecteurs CSS spécifiques à SeLoger
        listings = soup.find_all('div', class_='c-cartaannonce')

        for listing in listings:
            try:
                # Extraction prix
                price_elem = listing.find('div', class_='c-cartaannonce__price')
                price = self._extract_price(price_elem.get_text() if price_elem else '0')

                # Extraction surface
                surface_elem = listing.find('div', class_='c-cartaannonce__surface')
                surface = self._extract_surface(surface_elem.get_text() if surface_elem else '0')

                # Extraction localisation
                location_elem = listing.find('div', class_='c-cartaannonce__location')
                location = location_elem.get_text().strip() if location_elem else ''
                city, postal_code = self._parse_location(location)

                # Extraction titre
                title_elem = listing.find('a', class_='c-cartaannonce__link')
                title = title_elem.get_text().strip() if title_elem else ''

                # Lien annonce
                link = urljoin(self.base_url, title_elem.get('href')) if title_elem else ''

                if price > 0 and surface > 0 and city:
                    properties.append(RawProperty(
                        title=title,
                        price=price,
                        surface=surface,
                        city=city,
                        postal_code=postal_code,
                        source=self.name,
                        link=link,
                        scraped_at=datetime.now().isoformat()
                    ))

            except Exception as e:
                logger.warning(f"Erreur parsing annonce: {e}")
                continue

        return properties

    def _extract_price(self, price_text: str) -> int:
        """Extraction prix depuis texte"""
        price_clean = re.sub(r'[^\d]', '', price_text)
        return int(price_clean) if price_clean else 0

    def _extract_surface(self, surface_text: str) -> int:
        """Extraction surface depuis texte"""
        surface_clean = re.sub(r'[^\d]', '', surface_text)
        return int(surface_clean) if surface_clean else 0

    def _parse_location(self, location_text: str) -> tuple:
        """Parsing localisation (ville, code postal)"""
        # Pattern: "75001 Paris 1er Arrondissement"
        match = re.search(r'(\d{5})\s+([A-Za-z\s]+)', location_text)
        if match:
            return match.group(2).strip(), match.group(1)
        return location_text, ''
```

#### Client API INSEE

```python
# src/scrapers/insee_client.py
import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime

class INSEEClient:
    """Client pour l'API INSEE (données démographiques)"""

    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://api.insee.fr"
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_demographic_data(self, postal_code: str, city: str) -> Optional[Dict]:
        """Récupération données démographiques"""
        try:
            # API INSEE données communales
            url = f"{self.base_url}/metadonnees/cog/commune/{postal_code}"

            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._format_demographic_data(data, postal_code, city)
                else:
                    logger.warning(f"INSEE API error {response.status} for {postal_code}")
                    return None

        except Exception as e:
            logger.error(f"Erreur INSEE API: {e}")
            return None

    def _format_demographic_data(self, data: dict, postal_code: str, city: str) -> Dict:
        """Formatage données démographiques"""
        return {
            'postal_code': postal_code,
            'city': city,
            'population': data.get('population', 0),
            'surface_km2': data.get('surface', 0),
            'density': data.get('population', 0) / max(data.get('surface', 1), 1),
            'source': 'insee',
            'scraped_at': datetime.now().isoformat()
        }
```

### C2 - Repository Pattern

#### Architecture Repository

```python
# src/repositories/property_repository.py
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, func, and_, or_, desc, asc
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
import logging

from src.models import Property, DemographicData, AggregatedProperty

logger = logging.getLogger(__name__)

class PropertyRepository:
    """Repository pour les opérations de base de données"""

    def __init__(self, database_url: str = "sqlite:///data/immobilier_rgpd.db"):
        self.engine = create_engine(
            database_url,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            echo=False  # Mettre True pour debug SQL
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_session(self) -> Session:
        """Crée une session de base de données"""
        return self.SessionLocal()

    # Requêtes simples
    def get_by_id(self, property_id: int) -> Optional[Property]:
        """Récupère une propriété par ID"""
        with self.get_session() as session:
            return session.query(Property).filter(
                Property.id_prop == property_id
            ).first()

    def get_all(self, limit: int = 100) -> List[Property]:
        """Récupère toutes les propriétés avec limite"""
        with self.get_session() as session:
            return session.query(Property).limit(limit).all()

    # Requêtes avec filtres
    def get_by_city(self, city: str, limit: int = 50) -> List[Property]:
        """Requête optimisée pour les propriétés par ville"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(Property.ville.ilike(f'%{city}%'))\
                .order_by(desc(Property.prix_euros))\
                .limit(limit)\
                .all()

    def get_by_price_range(self, min_price: int, max_price: int, limit: int = 50) -> List[Property]:
        """Requête optimisée pour les propriétés par plage de prix"""
        with self.get_session() as session:
            return session.query(Property)\
                .filter(and_(
                    Property.prix_euros >= min_price,
                    Property.prix_euros <= max_price
                ))\
                .order_by(asc(Property.prix_euros))\
                .limit(limit)\
                .all()

    # Requêtes complexes avec jointures
    def get_properties_with_demographics(self, city: str = None) -> List[Dict[str, Any]]:
        """Requête complexe avec jointure sur données démographiques"""
        with self.get_session() as session:
            query = session.query(
                Property,
                DemographicData.population,
                (Property.prix_euros / Property.surface_m2).label('price_per_m2')
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

    # Requêtes avec agrégation
    def get_statistics_by_city(self, city: str = None) -> List[Dict[str, Any]]:
        """Requête avec agrégation GROUP BY par ville"""
        with self.get_session() as session:
            query = session.query(
                Property.ville,
                Property.code_postal,
                func.count(Property.id_prop).label('total_properties'),
                func.avg(Property.prix_euros).label('avg_price'),
                func.min(Property.prix_euros).label('min_price'),
                func.max(Property.prix_euros).label('max_price'),
                func.avg(Property.surface_m2).label('avg_surface')
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
```

### C3 - Service Layer

#### Logique métier

```python
# src/services/property_service.py
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime, timedelta
import re
import logging

from src.repositories.property_repository import PropertyRepository
from src.models import Property, DemographicData, AggregatedProperty

logger = logging.getLogger(__name__)

class PropertyService:
    """Service Layer pour le traitement des données immobilières"""

    def __init__(self, database_url: str = "sqlite:///data/immobilier_rgpd.db"):
        self.property_repo = PropertyRepository(database_url)

    # Pipeline de traitement
    async def process_raw_properties(self, raw_properties: List[Dict[str, Any]]) -> List[Property]:
        """Pipeline complet de traitement des données brutes"""
        logger.info(f"Début traitement {len(raw_properties)} propriétés brutes")

        # 1. Nettoyage et validation
        cleaned_properties = self._clean_properties(raw_properties)

        # 2. Détection doublons
        unique_properties = self._remove_duplicates(cleaned_properties)

        # 3. Validation métier
        valid_properties = self._validate_business_rules(unique_properties)

        # 4. Enrichissement (calcul prix/m², etc.)
        enriched_properties = self._enrich_properties(valid_properties)

        logger.info(f"Traitement terminé : {len(enriched_properties)} propriétés valides")
        return enriched_properties

    def _clean_properties(self, raw_properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Nettoyage et standardisation des données"""
        cleaned_properties = []

        for i, prop in enumerate(raw_properties):
            try:
                # Validation champs obligatoires
                if not self._validate_required_fields(prop):
                    logger.debug(f"Propriété {i} ignorée : champs manquants")
                    continue

                # Standardisation
                cleaned_prop = self._standardize_property_data(prop)

                if self._is_reasonable_property(cleaned_prop):
                    cleaned_properties.append(cleaned_prop)

            except Exception as e:
                logger.warning(f"Erreur nettoyage propriété {i}: {e}")
                continue

        return cleaned_properties

    def _standardize_property_data(self, prop: Dict[str, Any]) -> Dict[str, Any]:
        """Standardisation des formats de données"""
        # Standardisation prix
        if isinstance(prop.get('price'), str):
            price_clean = re.sub(r'[^\d]', '', str(prop['price']))
            prop['price'] = int(price_clean) if price_clean else 0

        # Standardisation surface
        if isinstance(prop.get('surface'), str):
            surface_clean = re.sub(r'[^\d]', '', str(prop['surface']))
            prop['surface'] = int(surface_clean) if surface_clean else 1

        # Standardisation code postal
        if isinstance(prop.get('postal_code'), str):
            prop['postal_code'] = prop['postal_code'].strip().zfill(5)

        # Standardisation ville
        if isinstance(prop.get('city'), str):
            prop['city'] = prop['city'].strip().title()

        # Standardisation titre
        if isinstance(prop.get('title'), str):
            prop['title'] = prop['title'].strip().title()

        # Normalisation source
        valid_sources = ['seloger', 'leboncoin', 'csv_import', 'insee', 'json_import']
        if prop.get('source') not in valid_sources:
            prop['source'] = 'other'

        # Ajout timestamp si manquant
        if not prop.get('scraped_at'):
            prop['scraped_at'] = datetime.now().isoformat()

        return prop

    def _validate_business_rules(self, properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validation des règles métier"""
        valid_properties = []

        for prop in properties:
            try:
                # Règle 1: Prix au m² raisonnable
                price_per_m2 = prop['price'] / prop['surface']
                if not (100 <= price_per_m2 <= 50000):
                    logger.debug(f"Prix/m² suspect: {price_per_m2:.2f}€")
                    continue

                # Règle 2: Taille raisonnable
                if not (10 <= prop['surface'] <= 1000):
                    logger.debug(f"Surface suspecte: {prop['surface']}m²")
                    continue

                # Règle 3: Prix raisonnable
                if not (10000 <= prop['price'] <= 10000000):
                    logger.debug(f"Prix suspect: {prop['price']}€")
                    continue

                # Règle 4: Code postal français valide
                postal_code = str(prop['postal_code'])
                if len(postal_code) == 5 and postal_code.isdigit():
                    dept = int(postal_code[:2])
                    if not (1 <= dept <= 95):  # Départements français valides
                        logger.debug(f"Département suspect: {dept}")
                        continue

                valid_properties.append(prop)

            except Exception as e:
                logger.warning(f"Erreur validation règles métier: {e}")
                continue

        return valid_properties

    def _enrich_properties(self, properties: List[Dict[str, Any]]) -> List[Property]:
        """Enrichissement des propriétés avec calculs et classifications"""
        enriched_properties = []

        for prop in properties:
            try:
                # Calcul prix au m²
                price_per_m2 = prop['price'] / prop['surface']

                # Classification type de bien
                property_type = self._classify_property_type(prop.get('title', ''))

                # Génération quartier anonymisé
                quartier = self._generate_anonymized_quarter(
                    prop['postal_code'],
                    prop['city']
                )

                enriched_property = Property(
                    quartier_anonymise=quartier,
                    prix_euros=prop['price'],
                    surface_m2=prop['surface'],
                    prix_m2_euros=price_per_m2,
                    code_postal=prop['postal_code'],
                    ville=prop['city'],
                    type_bien=property_type,
                    source_collecte=prop['source'],
                    date_collecte=datetime.now().date(),
                    date_anonymisation=datetime.now(),
                    mois_annee=datetime.now().strftime('%Y-%m'),
                    created_at=datetime.now()
                )

                enriched_properties.append(enriched_property)

            except Exception as e:
                logger.warning(f"Erreur enrichissement propriété: {e}")
                continue

        return enriched_properties

    def _classify_property_type(self, title: str) -> str:
        """Classification du type de bien depuis le titre"""
        title_lower = title.lower()

        if any(keyword in title_lower for keyword in ['studio', 't1', 'f1']):
            return 'studio'
        elif any(keyword in title_lower for keyword in ['appartement', 't2', 't3', 't4', 'f2', 'f3', 'f4']):
            return 'appartement'
        elif any(keyword in title_lower for keyword in ['maison', 'villa', 'pavillon']):
            return 'maison'
        elif 'terrain' in title_lower:
            return 'terrain'
        else:
            return 'autre'

    def _generate_anonymized_quarter(self, postal_code: str, city: str) -> str:
        """Génération quartier anonymisé pour conformité RGPD"""
        # Hash du code postal pour anonymisation
        import hashlib
        hash_object = hashlib.sha256(f"{postal_code}{city}".encode())
        hex_dig = hash_object.hexdigest()

        # Génération nom de quartier générique
        quarter_names = ['Centre', 'Nord', 'Sud', 'Est', 'Ouest', 'Quartier Historique']
        quarter_index = int(hex_dig[:8], 16) % len(quarter_names)

        return f"{quarter_names[quarter_index]} {city[:3].upper()}"
```

---

## Base de données

### Schéma de données (RGPD)

```sql
-- Table principale des propriétés anonymisées
CREATE TABLE proprietes_anonymisees (
    id_prop INTEGER PRIMARY KEY AUTOINCREMENT,
    surface_m2 INTEGER NOT NULL,
    prix_euros INTEGER NOT NULL,
    prix_m2_euros REAL NOT NULL,
    code_postal VARCHAR(5) NOT NULL,
    ville VARCHAR(100) NOT NULL,
    quartier_anonymise VARCHAR(50),
    type_bien VARCHAR(50) NOT NULL,
    source_collecte VARCHAR(20) NOT NULL,
    date_collecte DATE NOT NULL,
    date_anonymisation DATETIME,
    mois_annee VARCHAR(7) NOT NULL,
    created_at DATETIME NOT NULL,

    CHECK (prix_euros >= 0),
    CHECK (surface_m2 > 0)
);

-- Données démographiques INSEE
CREATE TABLE demographic_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    postal_code VARCHAR(5) NOT NULL,
    city VARCHAR(100) NOT NULL,
    population INTEGER,
    source VARCHAR(50) DEFAULT 'insee',
    scraped_at DATETIME NOT NULL,

    CHECK (population >= 0)
);

-- Données agrégées par localisation
CREATE TABLE aggregated_properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    postal_code VARCHAR(5) NOT NULL,
    city VARCHAR(100) NOT NULL,
    total_properties INTEGER NOT NULL,
    avg_price REAL NOT NULL,
    min_price INTEGER NOT NULL,
    max_price INTEGER NOT NULL,
    avg_surface REAL NOT NULL,
    avg_price_per_m2 REAL NOT NULL,
    sources_count INTEGER NOT NULL,
    sources_list VARCHAR(255),
    aggregation_date DATETIME NOT NULL,
    data_period_start DATETIME NOT NULL,
    data_period_end DATETIME NOT NULL,

    CHECK (total_properties >= 0),
    CHECK (avg_price >= 0),
    CHECK (sources_count >= 0)
);

-- Journal d'audit pour conformité RGPD
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id_hash VARCHAR(64),
    action VARCHAR(20) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id INTEGER,
    ip_address_hash VARCHAR(64),
    user_agent TEXT,
    timestamp DATETIME NOT NULL,
    legal_basis VARCHAR(100)
);

-- Index pour performance
CREATE INDEX idx_location ON proprietes_anonymisees(code_postal, ville);
CREATE INDEX idx_price_surface ON proprietes_anonymisees(prix_euros, surface_m2);
CREATE INDEX idx_source_date ON proprietes_anonymisees(source_collecte, date_collecte);
CREATE INDEX idx_city_search ON proprietes_anonymisees(ville);
CREATE INDEX idx_demo_location ON demographic_data(postal_code, city);
```

### Modèles SQLAlchemy

```python
# src/models/__init__.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Index, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Property(Base):
    """Modèle principal pour les propriétés immobilières anonymisées"""
    __tablename__ = 'proprietes_anonymisees'

    id_prop = Column(Integer, primary_key=True, index=True)
    surface_m2 = Column(Integer, nullable=False, index=True)
    prix_euros = Column(Integer, nullable=False, index=True)
    prix_m2_euros = Column(Float, nullable=False, index=True)
    code_postal = Column(String(5), nullable=False, index=True)
    ville = Column(String(100), nullable=False, index=True)
    quartier_anonymise = Column(String(50), nullable=True, index=True)
    type_bien = Column(String(50), nullable=False)
    source_collecte = Column(String(20), nullable=False)
    date_collecte = Column(Date, nullable=False)
    date_anonymisation = Column(DateTime, nullable=True)
    mois_annee = Column(String(7), nullable=False)
    created_at = Column(DateTime, nullable=False)

    __table_args__ = (
        CheckConstraint('prix_euros >= 0', name='check_price_positive'),
        CheckConstraint('surface_m2 > 0', name='check_surface_positive'),
        Index('idx_location', 'code_postal', 'ville'),
        Index('idx_price_surface', 'prix_euros', 'surface_m2'),
        Index('idx_source_date', 'source_collecte', 'date_collecte'),
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
            'type': self.type_bien,
            'source': self.source_collecte,
            'scraped_at': self.date_anonymisation.isoformat() if self.date_anonymisation else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
```

---

## API REST

### Architecture FastAPI

```python
# src/api/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import api_router
from src.utils.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API REST pour l'observatoire immobilier public",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.DEBUG
    )
```

### Routes API

```python
# src/api/routes/properties.py
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user, get_property_service
from src.schemas.property import PropertyResponse, PropertyCreate, PaginatedPropertiesResponse
from src.models.user import User

router = APIRouter()

@router.get("/", response_model=PaginatedPropertiesResponse)
async def get_properties(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum d'éléments"),
    city: Optional[str] = Query(None, description="Filtrer par ville"),
    min_price: Optional[int] = Query(None, ge=0, description="Prix minimum"),
    max_price: Optional[int] = Query(None, ge=0, description="Prix maximum"),
    property_type: Optional[str] = Query(None, description="Type de bien"),
    current_user: User = Depends(get_current_user),
    property_service = Depends(get_property_service)
):
    """Liste des propriétés avec filtres et pagination"""

    properties = await property_service.get_properties(
        skip=skip,
        limit=limit,
        city=city,
        min_price=min_price,
        max_price=max_price,
        property_type=property_type
    )

    total = await property_service.count_properties(
        city=city,
        min_price=min_price,
        max_price=max_price,
        property_type=property_type
    )

    return PaginatedPropertiesResponse(
        properties=properties,
        total=total,
        skip=skip,
        limit=limit,
        has_more=skip + limit < total
    )

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: int = Path(..., ge=1, description="ID de la propriété"),
    current_user: User = Depends(get_current_user),
    property_service = Depends(get_property_service)
):
    """Détail d'une propriété spécifique"""

    property = await property_service.get_property_by_id(property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Propriété non trouvée")

    # Vérification droits d'accès
    if not await property_service.check_access_rights(current_user, property):
        raise HTTPException(status_code=403, detail="Accès non autorisé")

    return property

@router.post("/", response_model=PropertyResponse)
async def create_property(
    property_data: PropertyCreate,
    current_user: User = Depends(get_current_user),
    property_service = Depends(get_property_service)
):
    """Création d'une nouvelle propriété"""

    try:
        property = await property_service.create_property(property_data, current_user.id)
        return property
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: int = Path(..., ge=1),
    property_update: PropertyCreate,
    current_user: User = Depends(get_current_user),
    property_service = Depends(get_property_service)
):
    """Mise à jour d'une propriété"""

    # Vérification existence et droits
    existing_property = await property_service.get_property_by_id(property_id)
    if not existing_property:
        raise HTTPException(status_code=404, detail="Propriété non trouvée")

    if not await property_service.check_update_rights(current_user, existing_property):
        raise HTTPException(status_code=403, detail="Modification non autorisée")

    try:
        updated_property = await property_service.update_property(property_id, property_update)
        return updated_property
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{property_id}")
async def delete_property(
    property_id: int = Path(..., ge=1),
    current_user: User = Depends(get_current_user),
    property_service = Depends(get_property_service)
):
    """Suppression d'une propriété"""

    # Vérification existence et droits
    existing_property = await property_service.get_property_by_id(property_id)
    if not existing_property:
        raise HTTPException(status_code=404, detail="Propriété non trouvée")

    if not await property_service.check_delete_rights(current_user, existing_property):
        raise HTTPException(status_code=403, detail="Suppression non autorisée")

    success = await property_service.delete_property(property_id)
    if success:
        return {"message": "Propriété supprimée avec succès"}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression")
```

### Schémas Pydantic

```python
# src/schemas/property.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class PropertyBase(BaseModel):
    """Schéma de base pour les propriétés"""
    title: str = Field(..., min_length=1, max_length=100, description="Titre de l'annonce")
    price: int = Field(..., gt=0, le=10000000, description="Prix en euros")
    surface: int = Field(..., gt=10, le=1000, description="Surface en m²")
    postal_code: str = Field(..., regex=r'^[0-9]{5}$', description="Code postal français")
    city: str = Field(..., min_length=2, max_length=100, description="Nom de la ville")
    property_type: Optional[str] = Field(None, description="Type de bien")

class PropertyCreate(PropertyBase):
    """Schéma pour la création de propriété"""

    @validator('price_per_m2')
    def validate_price_per_m2(cls, v, values):
        if 'price' in values and 'surface' in values:
            price_per_m2 = values['price'] / values['surface']
            if not (100 <= price_per_m2 <= 50000):
                raise ValueError('Prix au m² hors limites raisonnables (100€ - 50000€)')
        return v

class PropertyUpdate(PropertyBase):
    """Schéma pour la mise à jour de propriété"""
    pass

class PropertyResponse(PropertyBase):
    """Schéma pour la réponse des propriétés"""
    id: int
    price_per_m2: float
    type: Optional[str] = None
    source: str
    scraped_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class PaginatedPropertiesResponse(BaseModel):
    """Schéma pour les réponses paginées"""
    properties: List[PropertyResponse]
    total: int = Field(..., ge=0, description="Nombre total d'éléments")
    skip: int = Field(..., ge=0, description="Nombre d'éléments sautés")
    limit: int = Field(..., ge=1, le=1000, description="Limite de requête")
    has_more: bool = Field(..., description="Indique s'il y a plus d'éléments")
```

---

## Sécurité

### Authentification JWT

```python
# src/utils/auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.utils.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Création d'un token JWT d'accès"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def create_refresh_token(data: dict):
    """Création d'un token JWT de rafraîchissement"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Vérification d'un token JWT"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Vérification type de token
        if payload.get("type") != token_type:
            return None

        # Vérification expiration
        if datetime.utcnow() > datetime.fromtimestamp(payload.get("exp", 0)):
            return None

        return payload

    except JWTError:
        return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérification mot de passe"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashage mot de passe"""
    return pwd_context.hash(password)
```

### Middleware de sécurité

```python
# src/api/middleware/security.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
import hashlib
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware pour la limitation des requêtes"""

    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/"):
            client_ip = request.client.host

            if not self._is_allowed(client_ip):
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too Many Requests"},
                    headers={"Retry-After": str(self.period)}
                )

        response = await call_next(request)
        return response

    def _is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        requests = self.clients[client_ip]

        # Nettoyage anciennes requêtes
        requests[:] = [req_time for req_time in requests if now - req_time < self.period]

        # Vérification limite
        if len(requests) >= self.calls:
            return False

        requests.append(now)
        return True

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware pour en-têtes de sécurité OWASP"""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # En-têtes sécurité
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response
```

---

## Tests et qualité

### Structure des tests

```bash
tests/
├── unit/                     # Tests unitaires
│   ├── test_repositories.py
│   ├── test_services.py
│   ├── test_scrapers.py
│   └── test_auth.py
├── integration/              # Tests d'intégration
│   ├── test_api_endpoints.py
│   ├── test_database.py
│   └── test_scraping_pipeline.py
├── e2e/                     # Tests end-to-end
│   ├── test_complete_workflow.py
│   └── test_performance.py
└── conftest.py               # Configuration pytest
```

### Tests unitaires

```python
# tests/unit/test_property_repository.py
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, date

from src.repositories.property_repository import PropertyRepository
from src.models import Property

class TestPropertyRepository:
    """Tests unitaires pour PropertyRepository"""

    @pytest.fixture
    def repository(self):
        """Fixture pour le repository"""
        return PropertyRepository("sqlite:///:memory:")

    @pytest.fixture
    def sample_property(self):
        """Fixture pour une propriété exemple"""
        return Property(
            quartier_anonymise="Centre PAR",
            prix_euros=300000,
            surface_m2=60,
            prix_m2_euros=5000.0,
            code_postal="75001",
            ville="Paris",
            type_bien="appartement",
            source_collecte="seloger",
            date_collecte=date.today(),
            date_anonymisation=datetime.now(),
            mois_annee="2024-01",
            created_at=datetime.now()
        )

    def test_create_tables(self, repository):
        """Test création des tables"""
        repository.create_tables()

        # Vérification existence table
        with repository.get_session() as session:
            result = session.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in result]
            assert 'proprietes_anonymisees' in tables

    def test_insert_property(self, repository, sample_property):
        """Test insertion propriété"""
        repository.create_tables()

        with repository.get_session() as session:
            session.add(sample_property)
            session.commit()
            session.refresh(sample_property)

            assert sample_property.id_prop is not None
            assert sample_property.ville == "Paris"
            assert sample_property.prix_euros == 300000

    def test_get_by_id(self, repository, sample_property):
        """Test récupération par ID"""
        repository.create_tables()

        with repository.get_session() as session:
            session.add(sample_property)
            session.commit()
            session.refresh(sample_property)

        # Test récupération
        found_property = repository.get_by_id(sample_property.id_prop)

        assert found_property is not None
        assert found_property.id_prop == sample_property.id_prop
        assert found_property.ville == "Paris"

    def test_get_by_city(self, repository, sample_property):
        """Test récupération par ville"""
        repository.create_tables()

        with repository.get_session() as session:
            session.add(sample_property)
            session.commit()

        # Test récupération
        properties = repository.get_by_city("Paris")

        assert len(properties) == 1
        assert properties[0].ville == "Paris"

    def test_get_statistics_by_city(self, repository, sample_property):
        """Test statistiques par ville"""
        repository.create_tables()

        with repository.get_session() as session:
            session.add(sample_property)
            session.commit()

        # Test statistiques
        stats = repository.get_statistics_by_city("Paris")

        assert len(stats) == 1
        assert stats[0]['city'] == "Paris"
        assert stats[0]['total_properties'] == 1
        assert stats[0]['avg_price'] == 300000.0
```

### Tests d'intégration API

```python
# tests/integration/test_api_endpoints.py
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

from src.api.app import app
from src.utils.auth import create_access_token

class TestAPIEndpoints:
    """Tests d'intégration pour les endpoints API"""

    @pytest.fixture
    def client(self):
        """Fixture client de test"""
        return TestClient(app)

    @pytest.fixture
    async def async_client(self):
        """Fixture client asynchrone"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac

    @pytest.fixture
    def auth_headers(self):
        """Fixture en-têtes authentifiés"""
        token_data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(token_data)
        return {"Authorization": f"Bearer {token}"}

    def test_health_check(self, client):
        """Test endpoint health"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_get_properties_unauthorized(self, client):
        """Test accès non autorisé"""
        response = client.get("/api/v1/properties")

        assert response.status_code == 401
        assert "detail" in response.json()

    def test_get_properties_authorized(self, client, auth_headers):
        """Test accès autorisé"""
        response = client.get("/api/v1/properties", headers=auth_headers)

        assert response.status_code == 200
        assert "properties" in response.json()
        assert "total" in response.json()
        assert "skip" in response.json()
        assert "limit" in response.json()

    def test_get_properties_with_filters(self, client, auth_headers):
        """Test filtres propriétés"""
        response = client.get(
            "/api/v1/properties?city=Paris&min_price=100000&max_price=500000",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "properties" in data
        assert len(data["properties"]) <= 100  # Limite par défaut

    def test_create_property_validation_error(self, client, auth_headers):
        """Test validation erreur création"""
        invalid_property = {
            "title": "Test Property",
            "price": -1000,  # Invalide
            "surface": 50,
            "postal_code": "75001",
            "city": "Paris"
        }

        response = client.post(
            "/api/v1/properties",
            json=invalid_property,
            headers=auth_headers
        )

        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("price" in str(error) for error in errors)

    async def test_api_performance(self, async_client, auth_headers):
        """Test performance API"""
        import time

        start_time = time.time()

        response = await async_client.get(
            "/api/v1/properties",
            headers=auth_headers
        )

        end_time = time.time()
        response_time = end_time - start_time

        assert response.status_code == 200
        assert response_time < 2.0  # < 2 secondes
```

### Configuration pytest

```python
# tests/conftest.py
import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.repositories.property_repository import PropertyRepository

@pytest.fixture(scope="session")
def event_loop():
    """Création event loop pour tests asynchrones"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def test_db():
    """Base de données de test"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    yield TestSessionLocal

    # Nettoyage
    Base.metadata.drop_all(engine)

@pytest.fixture
def test_repository(test_db):
    """Repository de test"""
    return PropertyRepository("sqlite:///:memory:")

@pytest.fixture
def mock_scraping_response():
    """Mock réponse scraping"""
    return """
    <html>
        <div class="c-cartaannonce">
            <div class="c-cartaannonce__price">300 000 €</div>
            <div class="c-cartaannonce__surface">60 m²</div>
            <div class="c-cartaannonce__location">75001 Paris</div>
            <div class="c-cartaannonce__link">/annonce/123</div>
        </div>
    </html>
    """
```

---

## Déploiement

### Configuration Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Configuration environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installation dépendances système
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Configuration workspace
WORKDIR /app

# Copie requirements et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie code source
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY .env.example .env

# Création répertoires
RUN mkdir -p logs data

# Permissions
RUN chmod +x scripts/*.py

# Exposition port
EXPOSE 8001

# Commande lancement
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8001"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=sqlite:///data/immobilier_rgpd.db
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:13-alpine
    environment:
      - POSTGRES_DB=observatoire
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
```

### Script de déploiement

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

echo " Déploiement Observatoire Immobilier"

# Vérifications pré-déploiement
if [ ! -f ".env" ]; then
    echo " Fichier .env manquant"
    exit 1
fi

# Backup base de données
if [ -f "data/immobilier_rgpd.db" ]; then
    echo "📦 Backup base de données..."
    cp data/immobilier_rgpd.db data/backup_$(date +%Y%m%d_%H%M%S).db
fi

# Build Docker
echo "🔨 Build Docker..."
docker-compose build

# Migration base de données
echo " Migration base de données..."
docker-compose run --rm api python scripts/setup_database.py

# Redémarrage services
echo " Redémarrage services..."
docker-compose down
docker-compose up -d

# Attente démarrage
echo "⏳ Attente démarrage services..."
sleep 30

# Vérification santé
echo "🏥 Vérification santé API..."
if curl -f http://localhost:8001/health; then
    echo " API fonctionnelle"
else
    echo " API non fonctionnelle"
    docker-compose logs api
    exit 1
fi

echo "🎉 Déploiement terminé avec succès"
echo " API disponible : http://localhost:8001"
echo "📚 Documentation : http://localhost:8001/docs"
```

### Configuration Nginx

```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8001;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    server {
        listen 80;
        server_name observatoire-immobilier.local;

        # Redirection HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name observatoire-immobilier.local;

        # SSL
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

        # En-têtes sécurité
        add_header X-Content-Type-Options nosniff;
        add_header X-Frame-Options DENY;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

        location / {
            limit_req zone=api burst=20 nodelay;

            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://api/health;
            access_log off;
        }
    }
}
```

---

## Maintenance et évolution

### Monitoring et logs

```python
# src/utils/monitoring.py
import logging
import time
import psutil
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SystemMonitor:
    """Monitoring système et application"""

    def __init__(self):
        self.metrics = {}
        self.start_time = datetime.now()

    def collect_system_metrics(self) -> Dict[str, Any]:
        """Collecte métriques système"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'active_connections': len(psutil.net_connections()),
            'uptime': (datetime.now() - self.start_time).total_seconds()
        }

    def collect_application_metrics(self) -> Dict[str, Any]:
        """Collecte métriques application"""
        return {
            'requests_count': self.metrics.get('requests_count', 0),
            'errors_count': self.metrics.get('errors_count', 0),
            'avg_response_time': self.metrics.get('avg_response_time', 0),
            'active_users': self.metrics.get('active_users', 0),
            'database_connections': self.metrics.get('database_connections', 0)
        }

    def log_metrics(self):
        """Logging des métriques"""
        system_metrics = self.collect_system_metrics()
        app_metrics = self.collect_application_metrics()

        logger.info(f"Métriques système: {system_metrics}")
        logger.info(f"Métriques application: {app_metrics}")

        # Alertes si seuils dépassés
        if system_metrics['cpu_percent'] > 80:
            logger.warning(f"CPU élevé: {system_metrics['cpu_percent']}%")

        if system_metrics['memory_percent'] > 80:
            logger.warning(f"Mémoire élevée: {system_metrics['memory_percent']}%")

        if app_metrics['avg_response_time'] > 2000:  # 2 secondes
            logger.warning(f"Temps de réponse élevé: {app_metrics['avg_response_time']}ms")
```

### Scripts de maintenance

```python
# scripts/maintenance.py
import asyncio
import logging
from datetime import datetime, timedelta

from src.repositories.property_repository import PropertyRepository
from src.utils.monitoring import SystemMonitor

logger = logging.getLogger(__name__)

class MaintenanceTasks:
    """Tâches de maintenance automatisées"""

    def __init__(self):
        self.repository = PropertyRepository()
        self.monitor = SystemMonitor()

    async def run_daily_tasks(self):
        """Tâches journalières"""
        logger.info("Début tâches maintenance journalières")

        try:
            # Nettoyage logs anciens
            await self.cleanup_old_logs()

            # Agrégation données
            await self.aggregate_daily_data()

            # Sauvegarde base de données
            await self.backup_database()

            # Vérification intégrité
            await self.check_data_integrity()

            logger.info("Tâches journalières terminées")

        except Exception as e:
            logger.error(f"Erreur tâches journalières: {e}")

    async def cleanup_old_logs(self):
        """Nettoyage logs anciens"""
        cutoff_date = datetime.now() - timedelta(days=30)

        # Suppression logs audit anciens
        with self.repository.get_session() as session:
            from src.models import AuditLog
            deleted = session.query(AuditLog)\
                .filter(AuditLog.timestamp < cutoff_date)\
                .delete()
            session.commit()

            logger.info(f"Supprimé {deleted} logs audit anciens")

    async def aggregate_daily_data(self):
        """Agrégation données journalières"""
        today = datetime.now().date()

        # Agrégation par ville
        city_stats = self.repository.get_statistics_by_city()

        for stat in city_stats:
            if stat['total_properties'] >= 3:  # Minimum 3 propriétés
                await self.save_aggregated_data(stat, today)

        logger.info(f"Agrégé {len(city_stats)} villes pour {today}")

    async def backup_database(self):
        """Sauvegarde base de données"""
        backup_path = f"data/backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

        import shutil
        shutil.copy2("data/immobilier_rgpd.db", backup_path)

        logger.info(f"Base de données sauvegardée: {backup_path}")

    async def check_data_integrity(self):
        """Vérification intégrité données"""
        with self.repository.get_session() as session:
            from src.models import Property

            # Vérification données incohérentes
            invalid_properties = session.query(Property)\
                .filter(or_(
                    Property.prix_euros <= 0,
                    Property.surface_m2 <= 0,
                    Property.prix_m2_euros <= 0
                ))\
                .count()

            if invalid_properties > 0:
                logger.warning(f"{invalid_properties} propriétés incohérentes trouvées")

            # Vérification doublons
            potential_duplicates = session.query(Property)\
                .group_by(
                    Property.code_postal,
                    Property.ville,
                    Property.surface_m2,
                    Property.prix_euros
                )\
                .having(func.count(Property.id_prop) > 1)\
                .count()

            if potential_duplicates > 0:
                logger.warning(f"{potential_duplicates} doublons potentiels détectés")

async def main():
    """Point d'entrée maintenance"""
    logging.basicConfig(level=logging.INFO)

    maintenance = MaintenanceTasks()

    while True:
        try:
            await maintenance.run_daily_tasks()

            # Exécution une fois par jour
            await asyncio.sleep(24 * 3600)

        except KeyboardInterrupt:
            logger.info("Maintenance interrompue")
            break
        except Exception as e:
            logger.error(f"Erreur maintenance: {e}")
            await asyncio.sleep(3600)  # Retry dans 1 heure

if __name__ == "__main__":
    asyncio.run(main())
```

### Guide d'évolution

#### Ajout de nouvelles sources de données

1. **Créer un nouveau scraper** :
```python
# src/scrapers/new_source_scraper.py
from .base_scraper import BaseScraper

class NewSourceScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://newsource.com", "newsource")

    async def search_properties(self, criteria):
        # Implémentation spécifique
        pass
```

2. **Enregistrer le scraper** :
```python
# src/scrapers/__init__.py
from .new_source_scraper import NewSourceScraper

AVAILABLE_SCRAPERS = {
    'seloger': SeLogerScraper,
    'leboncoin': LeBonCoinScraper,
    'newsource': NewSourceScraper,
}
```

3. **Configurer dans l'orchestrateur** :
```python
# scripts/orchestrate_scraping.py
scrapers = [
    NewSourceScraper() for _ in range(1)  # 1 instance
]
```

#### Ajout de nouveaux endpoints API

1. **Créer le schéma Pydantic** :
```python
# src/schemas/new_feature.py
from pydantic import BaseModel

class NewFeatureResponse(BaseModel):
    id: int
    name: str
    value: float

    class Config:
        orm_mode = True
```

2. **Créer le service** :
```python
# src/services/new_feature_service.py
class NewFeatureService:
    async def get_data(self):
        # Logique métier
        pass
```

3. **Créer les routes** :
```python
# src/api/routes/new_feature.py
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/", response_model=List[NewFeatureResponse])
async def get_new_feature(
    current_user: User = Depends(get_current_user),
    service = Depends(get_new_feature_service)
):
    return await service.get_data()
```

4. **Enregistrer les routes** :
```python
# src/api/routes/__init__.py
from .new_feature import router as new_feature_router

api_router.include_router(
    new_feature_router,
    prefix="/new-feature",
    tags=["new-feature"]
)
```

#### Performance et scalabilité

1. **Mise en cache Redis** :
```python
# src/utils/cache.py
import redis
import json
from typing import Optional, Any

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def get(self, key: str) -> Optional[Any]:
        value = self.redis.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: Any, ttl: int = 3600):
        self.redis.setex(key, ttl, json.dumps(value))

    async def delete(self, key: str):
        self.redis.delete(key)
```

2. **Optimisation requêtes** :
```python
# Utilisation de requêtes préparées
from sqlalchemy import text

class OptimizedRepository:
    def get_properties_fast(self, city: str):
        query = text("""
            SELECT * FROM proprietes_anonymisees
            WHERE ville LIKE :city
            ORDER BY prix_euros DESC
            LIMIT 50
        """)

        with self.get_session() as session:
            return session.execute(query, {"city": f"%{city}%"}).fetchall()
```

---

*Ce guide technique fournit une documentation complète pour comprendre, maintenir et faire évoluer l'Observatoire Immobilier Public. Il couvre tous les aspects techniques du projet, de l'architecture à la maintenance en passant par la sécurité et les tests.*