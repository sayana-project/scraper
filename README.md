# Observatoire Immobilier - Projet Scraper

**Projet de validation du bloc E1 "Gestion des données"**
**Formation**: Simplon.co - Développeur en Intelligence Artificielle
**Date**: Janvier 2025

---

## Objectif

Développer un observatoire immobilier automatisé conforme au RGPD pour valider les 5 compétences du diplôme :
- **C1** : Collecter les données (5 sources)
- **C2** : Stocker et requêter (SQL optimisé)
- **C3** : Traiter et agréger (nettoyage, validation)
- **C4** : Base de données RGPD (anonymisation)
- **C5** : API REST sécurisée (FastAPI)

---

## Architecture

**Stack Python moderne et légère**:
- **Backend**: Python 3.10+ avec FastAPI
- **Scraping**: BeautifulSoup, Selenium, Scrapy
- **Base de données**: SQLite + SQLAlchemy ORM
- **Sécurité**: JWT, bcrypt, conformité RGPD
- **Tests**: pytest (couverture 80%+)

**Pattern architectural**: Repository Pattern (N-Tiers)

---

## Structure du Projet

```
scraper/
├── src/                    # Code source
│   ├── api/               # C5 - API REST FastAPI
│   ├── scrapers/          # C1 - 5 sources collecte
│   ├── models/            # C2, C4 - Tables RGPD
│   ├── repositories/      # C2 - Repository Pattern
│   ├── services/          # C3 - Logique traitement
│   ├── schemas/           # C5 - Validation Pydantic
│   └── utils/             # Config, sécurité, logging
├── tests/                 # Tests unitaires (pytest)
├── scripts/               # Scripts auxiliaires
│   ├── migration/         # Migration données
│   └── verification/      # Diagnostic BDD
├── docs/                  # Documentation
│   ├── RAPPORT_PROFESSIONNEL_6PAGES.md  # Pour soutenance ✅
│   ├── C1_SOURCES_MULTIPLES.md          # Détails 5 sources
│   └── nettoyage/         # Documentation nettoyage
├── data/                  # Données
│   └── immobilier_rgpd.db # Base SQLite (2000+ biens)
├── main.py                # Point d'entrée API
├── requirements.txt       # Dépendances Python
└── PROJET_PRET_SOUTENANCE.md  # Checklist soutenance
```

---

## Quick Start

### Installation

```bash
# 1. Cloner le projet
git clone <repository-url>
cd scraper

# 2. Activer l'environnement virtuel
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
```

### Lancer l'API

```bash
# Démarrer l'API
python main.py

# Accéder à la documentation interactive
http://localhost:8000/docs
```

### Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Tests avec couverture
pytest tests/ --cov=src
```

---

## Compétences Validées

| Compétence | Résultat | Validation |
|------------|----------|------------|
| **C1** - Collecte | 5 sources (HTML, JS, API, CSV, JSON) | ✅ VALIDÉ |
| **C2** - SQL | SQLite, 4 index, Repository Pattern | ✅ VALIDÉ |
| **C3** - Traitement | 2000 nettoyées, 20 agrégées | ✅ VALIDÉ |
| **C4** - RGPD | Art. 5.1, 30, anonymisation | ✅ VALIDÉ |
| **C5** - API | 8+ endpoints, JWT, tests 80%+ | ✅ VALIDÉ |

**Référentiel C1**: Minimum 3 sources → **5 sources implémentées** ✅

---

## Endpoints API Principaux

### Santé
- `GET /api/v1/health` - Health check

### Propriétés
- `GET /api/v1/properties` - Liste propriétés (pagination)
- `GET /api/v1/properties/{code_postal}` - Par code postal
- `GET /api/v1/properties/stats` - Statistiques globales

### Analytics (données agrégées RGPD)
- `GET /api/v1/analytics/overview` - Vue d'ensemble
- `GET /api/v1/analytics/city/{city}` - Statistiques par ville
- `GET /api/v1/analytics/price-evolution` - Évolution prix

---

## Sources de Collecte (C1)

| # | Source | Type | Technologie |
|---|--------|------|-------------|
| 1 | SeLoger | HTML statique | BeautifulSoup |
| 2 | LeBonCoin | JavaScript | Selenium |
| 3 | API INSEE | API REST | requests |
| 4 | CSV | Fichiers | Pandas |
| 5 | JSON | Fichiers | json |

---

## Base de Données RGPD (C4)

**5 tables actives** (immobilier_rgpd.db):

| Table | Enregistrements | Usage |
|-------|-----------------|-------|
| proprietes_anonymisees | 2000 | Données immobilières anonymisées |
| statistiques_agregees | 20 | Statistiques pour API Analytics |
| registre_traitements_rgpd | 3 | Conformité Art. 30 RGPD |
| logs_access_rgpd | 5 | Traçabilité des accès |
| politiques_retention_rgpd | 4 | Durée de conservation |

**Conformité RGPD**:
- Anonymisation des adresses (quartier générique)
- Registre des traitements (Art. 30)
- Politique de rétention (24 mois)
- Seuil minimal 5 biens/statistique

---

## Scripts Utilitaires

### Migration et initialisation
```bash
# Générer données de test (fictives)
python scripts/migration/generate_demo_data.py

# Créer base RGPD complète
python scripts/migration/phase4_rgpd_implementation.py

# Générer statistiques agrégées (IMPORTANT pour API)
python scripts/migration/generate_statistics.py
```

### Vérification et diagnostic
```bash
# Vérifier conformité RGPD
python scripts/verification/check_rgpd_db.py

# Visualiser statistiques
python scripts/verification/view_statistics.py

# Vérifier tables
python scripts/verification/check_table_status.py
```

---

## Documentation

### Pour la soutenance
- [PROJET_PRET_SOUTENANCE.md](PROJET_PRET_SOUTENANCE.md) - Checklist complète
- [docs/RAPPORT_PROFESSIONNEL_6PAGES.md](docs/RAPPORT_PROFESSIONNEL_6PAGES.md) - Rapport 6 pages
- [docs/C1_SOURCES_MULTIPLES.md](docs/C1_SOURCES_MULTIPLES.md) - Détails 5 sources

### Documentation technique
- [docs/architecture.md](docs/architecture.md) - Architecture détaillée
- [docs/mcd_rgpd.md](docs/mcd_rgpd.md) - Modèle de données RGPD
- [scripts/README.md](scripts/README.md) - Scripts auxiliaires

### Documentation nettoyage
- [docs/nettoyage/TECHNOLOGIES_REELLES.md](docs/nettoyage/TECHNOLOGIES_REELLES.md) - Stack technique
- [docs/nettoyage/NETTOYAGE_TABLES_VIDES.md](docs/nettoyage/NETTOYAGE_TABLES_VIDES.md) - Justification

---

## Sécurité

### RGPD
- Données publiques uniquement
- Anonymisation automatique (quartier)
- Registre des traitements (Art. 30)
- Durée limitée conservation (24 mois)
- Seuil minimal agrégations (5 biens)

### OWASP
- Validation entrées (Pydantic)
- Authentification JWT
- Protection injection SQL (ORM)
- Rate limiting API
- Logs sécurisés

---

## Technologies Utilisées

| Catégorie | Technologies |
|-----------|-------------|
| **Scraping** | BeautifulSoup, Selenium, Scrapy, requests, Pandas |
| **Base de données** | SQLite, SQLAlchemy ORM |
| **API** | FastAPI, Pydantic, uvicorn |
| **Sécurité** | python-jose (JWT), passlib |
| **Tests** | pytest, pytest-asyncio, httpx |

**Note**: Pas de PostgreSQL, Airflow, Plotly, Dash - Stack simple et efficace avec SQLite.

---

## Métriques Finales

- **5 sources** de collecte (au-delà des 3 requises)
- **2000 propriétés** collectées et validées
- **20 villes** avec statistiques agrégées
- **5 tables RGPD** actives et documentées
- **8+ endpoints** API REST sécurisés
- **80%+ couverture** de tests

---

## Développement

### Mode développement
```bash
uvicorn src.api.app:app --reload
```

### Logs
Les logs sont dans `logs/observatoire.log`

### Ajout d'une source de collecte
1. Créer scraper dans `src/scrapers/`
2. Implémenter méthode `scrape()`
3. Ajouter au `scraper_manager.py`
4. Tester avec `pytest tests/test_scrapers.py`

---

## Licence et Auteur

**Projet académique** - Simplon.co 2024-2025
**Candidat**: [Votre Nom]
**Titre professionnel**: Développeur en Intelligence Artificielle

---

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: Voir [PROJET_PRET_SOUTENANCE.md](PROJET_PRET_SOUTENANCE.md)
- **RGPD**: Conforme Art. 5.1 et Art. 30

---

**Projet prêt pour la soutenance** ✅
