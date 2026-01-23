# Technologies RÉELLES du Projet - Observatoire Immobilier

**Date**: 15 janvier 2025
**Projet**: Scraper Immobilier - Validation Compétences C1-C5

---

## ATTENTION: Ce qui est RÉELLEMENT utilisé

Ce document corrige les hallucinations possibles et liste UNIQUEMENT les technologies **présentes dans le code**.

---

## 1. Langages et Frameworks

### Python 3.10+
- **Usage**: Langage principal du projet
- **Preuve**: `requirements.txt`, tous les fichiers `.py`

### FastAPI
- **Usage**: Framework API REST moderne
- **Preuve**: `src/api/app.py`, endpoints dans `src/api/routes/`
- **Compétence**: C5 - API RESTful

### SQLAlchemy
- **Usage**: ORM pour abstraction base de données
- **Preuve**: `src/models/database.py`, `src/models/rgpd_models.py`
- **Compétence**: C2 - Requêtes SQL, C4 - Base de données RGPD

---

## 2. Web Scraping

### Scrapy
- **Usage**: Framework de scraping professionnel
- **Preuve**: `requirements.txt` ligne 3
- **Compétence**: C1 - Collecte de données

### BeautifulSoup4
- **Usage**: Parsing HTML/XML
- **Preuve**: `requirements.txt` ligne 10
- **Compétence**: C1 - Extraction de données

### Selenium
- **Usage**: Scraping de sites JavaScript (dynamiques)
- **Preuve**: `requirements.txt` ligne 11
- **Compétence**: C1 - Sites dynamiques

### Requests
- **Usage**: Requêtes HTTP simples
- **Preuve**: `requirements.txt` ligne 2
- **Compétence**: C1 - Collecte de données

---

## 3. Traitement de Données

### Pandas
- **Usage**: Manipulation et nettoyage de données
- **Preuve**: `requirements.txt` ligne 14
- **Compétence**: C3 - Nettoyage et agrégation

### NumPy
- **Usage**: Calculs numériques et statistiques
- **Preuve**: `requirements.txt` ligne 15
- **Compétence**: C3 - Agrégation de données

---

## 4. Base de Données

### SQLite
- **Usage**: Base de données relationnelle (fichier local)
- **Preuve**: `data/immobilier_rgpd.db`, `database.py` ligne 10
- **Compétence**: C2, C4 - Base de données RGPD
- **Note**: AUCUNE mention de PostgreSQL dans le code!

### psycopg2-binary
- **Usage**: Connecteur PostgreSQL (dépendance non utilisée)
- **Preuve**: `requirements.txt` ligne 18
- **Statut**: ❌ NON UTILISÉ - Le projet utilise SQLite uniquement

---

## 5. Sécurité et Authentification

### python-jose
- **Usage**: Tokens JWT pour authentification
- **Preuve**: `requirements.txt` ligne 21, `src/utils/security.py`
- **Compétence**: C5 - Sécurisation API

### passlib
- **Usage**: Hachage de mots de passe
- **Preuve**: `requirements.txt` ligne 22
- **Compétence**: C5 - Sécurité

---

## 6. Testing

### pytest
- **Usage**: Tests unitaires et intégration
- **Preuve**: `requirements.txt` ligne 7, `tests/test_api.py`
- **Compétence**: C5 - Tests API

### pytest-asyncio
- **Usage**: Tests asynchrones FastAPI
- **Preuve**: `requirements.txt` ligne 30
- **Compétence**: C5 - Tests API asynchrones

### httpx
- **Usage**: Client HTTP pour tests API
- **Preuve**: `requirements.txt` ligne 31
- **Compétence**: C5 - Tests d'endpoints

---

## 7. Configuration et Environnement

### python-dotenv
- **Usage**: Chargement variables d'environnement
- **Preuve**: `requirements.txt` ligne 26, `.env.example`
- **Compétence**: Bonnes pratiques (configuration externe)

### pydantic-settings
- **Usage**: Validation configuration avec Pydantic
- **Preuve**: `requirements.txt` ligne 27, `src/utils/config.py`
- **Compétence**: C5 - Validation de données

---

## 8. Serveur Web

### Uvicorn
- **Usage**: Serveur ASGI pour FastAPI
- **Preuve**: `requirements.txt` ligne 5, `main.py`
- **Compétence**: C5 - Déploiement API

---

## 9. Versioning

### Git / GitHub
- **Usage**: Contrôle de version
- **Preuve**: `.git/`, `.gitignore`, historique des commits
- **Compétence**: Bonnes pratiques développement

---

## 10. Documentation

### Markdown
- **Usage**: Documentation technique
- **Preuve**: Tous les fichiers `.md` dans `docs/`
- **Compétence**: Documentation projet

### Docstrings Python
- **Usage**: Documentation inline du code
- **Preuve**: Tous les fichiers `.py` avec `"""`
- **Compétence**: Code maintenable

---

## ❌ CE QUI N'EST **PAS** UTILISÉ (Hallucinations à éviter)

### PostgreSQL
- ❌ Le projet utilise **SQLite uniquement**
- ❌ `psycopg2-binary` est dans requirements mais non utilisé
- ✅ Voir `database.py:10` → `sqlite:///data/immobilier_rgpd.db`

### PostGIS (Extensions géospatiales)
- ❌ Aucune mention dans le code
- ❌ Pas de données géospatiales complexes
- ✅ Seulement code postal + ville (texte simple)

### Apache Airflow
- ❌ Aucun DAG, aucune mention dans le code
- ❌ Pas d'orchestration complexe
- ✅ Script Python simple `aggregation.py` pour orchestration

### Plotly, Dash, Folium (Visualisation)
- ❌ Aucune bibliothèque de visualisation installée
- ❌ Pas de dashboards interactifs
- ✅ API RESTful retourne du JSON (visualisation = responsabilité client)

### Sphinx
- ❌ Pas de configuration Sphinx
- ❌ Pas de génération automatique de docs
- ✅ Documentation Markdown manuelle uniquement

---

## 📊 Résumé pour la Soutenance

### Technologies Backend
- **Langage**: Python 3.10+
- **API**: FastAPI + Uvicorn
- **BDD**: SQLite (fichier local RGPD)
- **ORM**: SQLAlchemy

### Technologies Scraping (C1)
- **Frameworks**: Scrapy, BeautifulSoup, Selenium
- **HTTP**: Requests

### Technologies Traitement (C2-C3)
- **Data**: Pandas, NumPy
- **SQL**: SQLAlchemy ORM

### Technologies Sécurité (C4-C5)
- **Auth**: JWT (python-jose), passlib
- **Validation**: Pydantic

### Technologies Tests
- **Framework**: pytest, pytest-asyncio, httpx

---

## 💡 Argument pour le Jury

> "J'ai choisi une stack Python moderne et légère adaptée au projet:
>
> - **FastAPI** pour l'API REST performante (C5)
> - **SQLite** pour la base RGPD (C4) - simple, portable, conforme
> - **SQLAlchemy** pour éviter les injections SQL (C2, sécurité)
> - **Scrapy + BeautifulSoup** pour le scraping multi-sources (C1)
> - **Pandas** pour le nettoyage et l'agrégation (C3)
>
> Pas besoin de PostgreSQL, Airflow ou dashboards complexes pour ce projet.
> L'architecture est **simple, fonctionnelle et professionnelle**."

---

## 🔗 Preuves dans le Code

| Technologie | Fichier preuve | Ligne |
|-------------|----------------|-------|
| FastAPI | `src/api/app.py` | 1-10 |
| SQLite | `src/models/database.py` | 10 |
| SQLAlchemy | `src/models/rgpd_models.py` | 1-50 |
| Scrapy | `requirements.txt` | 3 |
| Pandas | `requirements.txt` | 14 |
| pytest | `tests/test_api.py` | 1 |
| JWT | `src/utils/security.py` | 1-30 |

---

**Conclusion**: Ton projet utilise une stack **cohérente, moderne et adaptée** aux compétences C1-C5. Pas d'hallucinations nécessaires!
