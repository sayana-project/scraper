#  Architecture Technique - Observatoire Immobilier

##  Vue d'Ensemble

**Architecture N-Tiers simplifiée pour développeur junior**
- **Frontend** : API REST (pas d'interface web complexe)
- **Backend** : Python avec organisation en couches
- **Database** : PostgreSQL avec ORM SQLAlchemy
- **Sécurité** : JWT + validation Pydantic

---

##  Principes d'Architecture

###  Adoptés (Niveau Junior)
- **Séparation des responsabilités** : Chaque classe a un rôle clair
- **DTO (Data Transfer Objects)** : Validation avec Pydantic
- **Repository Pattern** : Abstraction de l'accès aux données
- **Service Layer** : Logique métier isolée
- **Dependency Injection** : Injection via FastAPI

###  Évités (Trop complexe pour Junior)
- Design Patterns avancés (Factory, Strategy...)
- Microservices
- Systèmes de messagerie complexes
- Architecture hexagonale complète

---

##  Structure des Dossiers

```
src/
├── models/                 # C4 - SQLAlchemy Models
│   ├── property.py        # Modèle Property
│   ├── location.py        # Modèle Location
│   └── database.py        # Configuration BDD
│
├── schemas/               # C5 - Pydantic DTOs
│   ├── property.py        # DTOs Property
│   ├── location.py        # DTOs Location
│   └── common.py          # DTOs réutilisables
│
├── repositories/           # C2 - Accès aux Données
│   ├── property_repository.py
│   ├── location_repository.py
│   └── base_repository.py
│
├── services/              # C3 - Logique Métier
│   ├── property_service.py
│   ├── scraper_service.py
│   └── analytics_service.py
│
├── scrapers/              # C1 - Collecte Données
│   ├── seloger_scraper.py
│   ├── leboncoin_scraper.py
│   └── base_scraper.py
│
├── api/                   # C5 - API REST
│   ├── dependencies.py    # Injection dépendances
│   ├── endpoints/         # Routes API
│   │   ├── properties.py
│   │   ├── analytics.py
│   │   └── auth.py
│   └── middleware.py      # Sécurité, rate limiting
│
└── utils/                 # Utilitaires
    ├── security.py        # JWT, password hashing
    ├── logging.py         # Configuration logs
    └── config.py          # Variables environnement
```

---

##  Patterns Architecture

### 1. Repository Pattern (C2)
**Objectif** : Abstraire l'accès aux données

```python
# repositories/base_repository.py
class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, model, id: int):
        return self.db.query(model).filter(model.id == id).first()

    def get_all(self, model):
        return self.db.query(model).all()

# repositories/property_repository.py
class PropertyRepository(BaseRepository):
    def get_by_city(self, city: str) -> List[Property]:
        return self.db.query(Property).filter(
            Property.city == city
        ).all()
```

### 2. Service Layer (C3)
**Objectif** : Logique métier, agrégation et nettoyage

```python
# services/property_service.py
class PropertyService:
    def __init__(self, prop_repo: PropertyRepository):
        self.prop_repo = prop_repo

    def calculate_price_per_m2(self, price: int, surface: int) -> float:
        """Calcule le prix au m²"""
        if surface <= 0:
            raise ValueError("Surface must be positive")
        return round(price / surface, 2)

    def get_average_price_by_city(self, city: str) -> float:
        """Calcule le prix moyen au m² par ville"""
        properties = self.prop_repo.get_by_city(city)
        if not properties:
            return 0.0

        total_price_m2 = sum(
            self.calculate_price_per_m2(p.price, p.surface)
            for p in properties
        )
        return round(total_price_m2 / len(properties), 2)
```

### 3. DTO Pattern avec Pydantic (C5)
**Objectif** : Validation et sérialisation des données

```python
# schemas/property.py
from pydantic import BaseModel, validator

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

    class Config:
        from_attributes = True

class PropertyAnalytics(BaseModel):
    """DTO pour les statistiques"""
    city: str
    average_price_per_m2: float
    total_properties: int
    min_price: int
    max_price: int
```

### 4. Dependency Injection (FastAPI)
**Objectif** : Injection des dépendances dans l'API

```python
# api/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db() -> Session:
    """Injection de la session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_property_repository(db: Session = Depends(get_db)) -> PropertyRepository:
    """Injection du repository Property"""
    return PropertyRepository(db)

def get_property_service(
    repo: PropertyRepository = Depends(get_property_repository)
) -> PropertyService:
    """Injection du service Property"""
    return PropertyService(repo)
```

---

##  Flux de Données

### 1. Flux Scraping (C1)
```
Web Sources → Base Scraper → Property Service → Repository → Database
```

### 2. Flux API (C5)
```
Client Request → DTO Validation → Service Layer → Repository → Database
                                    ↓
Response ← DTO Serialization ← Service Logic ← Database
```

### 3. Flux Traitement (C2-C3)
```
Raw Data → Service Layer (nettoyage) → Repository (C2) → Database
```

---

##  Sécurité OWASP

### 1. Validation des Entrées
```python
# Pydantic DTOs pour validation automatique
class PropertyCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    price: int = Field(..., gt=0)
```

### 2. Injection de dépendances sécurisées
```python
# api/dependencies.py
def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validation JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid token")
```

### 3. Rate Limiting
```python
# api/middleware.py
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/properties")
@limiter.limit("10/minute")
async def get_properties(request: Request):
    pass
```

---

##  Mapping Compétences → Architecture

| Compétence | Éléments Architecture | Fichiers Clés |
|------------|----------------------|---------------|
| **C1** - Collecte | Scraping classes | `scrapers/*.py` |
| **C2** - Requêtes SQL | Repository pattern | `repositories/*.py` |
| **C3** - Agrégation | Service layer | `services/*.py` |
| **C4** - BDD RGPD | SQLAlchemy models | `models/*.py` |
| **C5** - API REST | FastAPI + DTOs | `api/*.py`, `schemas/*.py` |

---

##  Avantages de cette Architecture

###  Pour le Jury
- **Code organisé** : Séparation claire des responsabilités
- **Maintenable** : Facile à faire évoluer
- **Testable** : Mock possible pour chaque couche
- **Professionnel** : Montre compréhension patterns standards

###  Pour le Développement
- **Modulaire** : Changer une partie sans casser le reste
- **Scalable** : Ajout facile de nouvelles fonctionnalités
- **Sécurisé** : Validation à plusieurs niveaux
- **Documenté** : DTOs auto-documentés

---

##  Exemple d'Utilisation Complète

```python
# api/endpoints/properties.py
@app.post("/properties", response_model=PropertyResponse)
async def create_property(
    property: PropertyCreate,
    service: PropertyService = Depends(get_property_service)
):
    """Créer une nouvelle propriété"""
    try:
        # Validation automatique via Pydantic
        created_property = service.create_property(property)
        return created_property
    except ValueError as e:
        raise HTTPException(400, str(e))

@app.get("/analytics/{city}", response_model=PropertyAnalytics)
async def get_city_analytics(
    city: str,
    service: PropertyService = Depends(get_property_service)
):
    """Obtenir les statistiques par ville"""
    analytics = service.get_city_analytics(city)
    if not analytics:
        raise HTTPException(404, "City not found")
    return analytics
```

---

## 📝 Conclusion

**Cette architecture est idéale pour un développeur junior car :**
- Structurée sans être surchargée
- Démontre des patterns professionnels
- Facile à expliquer pendant la soutenance
- Parfaitement adaptée aux 5 compétences du diplôme
- Évolutive pour de futures améliorations