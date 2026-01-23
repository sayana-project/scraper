"""
Configuration de la base de données SQLAlchemy (C4 - Compétence RGPD)

Ce module configure la connexion à la base de données SQLite respectant le RGPD.
Utilise SQLAlchemy ORM pour l'abstraction des requêtes SQL et garantir la sécurité.

Architecture:
- Base de données: data/immobilier_rgpd.db
- ORM: SQLAlchemy pour éviter les injections SQL
- Session: SessionLocal pour gérer les transactions

Conformité RGPD:
- Données anonymisées (adresses au niveau quartier uniquement)
- Pas de données personnelles identifiables
- Durée de conservation limitée des données
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion à la base de données RGPD
SQLALCHEMY_DATABASE_URL = "sqlite:///data/immobilier_rgpd.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Générateur de session de base de données pour les dépendances FastAPI.

    Yields:
        Session: Session SQLAlchemy active

    Note:
        La session est automatiquement fermée après utilisation (pattern context manager)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()