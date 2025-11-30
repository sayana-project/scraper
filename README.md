# 🏠 Observatoire Immobilier Public

Projet de fin d'études Simplon.co - Développeur Junior

## 🎯 Objectif

Développer un observatoire immobilier automatisé qui respecte le RGPD et les meilleures pratiques OWASP pour valider les 5 compétences du diplôme Simplon.co.

## 🏗️ Architecture

Architecture N-Tiers simplifiée pour développeur junior :
- **Backend** : Python 3.9+ avec FastAPI
- **Scraping** : BeautifulSoup4, Scrapy, Selenium
- **Base de données** : SQLAlchemy + SQLite/PostgreSQL
- **Sécurité** : JWT, bcrypt, conformité RGPD

## 📋 Compétences Validées (C1-C5)

- **C1** : Collecte multi-sources (web, API, fichiers, BDD)
- **C2** : Requêtes SQL optimisées avec Repository Pattern
- **C3** : Agrégation et nettoyage des données
- **C4** : Base de données conforme RGPD
- **C5** : API REST sécurisée avec Pydantic DTOs

## 📁 Structure du Projet

```
src/
├── models/          # C4 - SQLAlchemy Models
├── schemas/         # C5 - Pydantic DTOs
├── repositories/    # C2 - Repository Pattern
├── services/        # C3 - Service Layer
├── scrapers/        # C1 - Web Scraping
├── api/            # C5 - FastAPI Endpoints
└── utils/          # Configuration, Sécurité, Logging
```

## 🚀 Quick Start

### Prérequis
- Python 3.9+
- Git

### Installation

1. **Cloner le repository**
```bash
git clone <repository-url>
cd scraper
```

2. **Activer l'environnement virtuel**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

5. **Lancer l'API**
```bash
python main.py
```

6. **Accéder à l'API**
- URL : http://localhost:8000
- Documentation : http://localhost:8000/docs

## 📊 Endpoints Principaux

### POST /properties/
Créer une nouvelle propriété

### GET /analytics/{city}
Obtenir les statistiques par ville

### GET /health
Vérifier l'état de l'API

## 🔧 Développement

### Lancement en mode développement
```bash
uvicorn src.api.app:app --reload
```

### Tests
```bash
pytest
```

### Logging
Les logs sont disponibles dans `logs/observatoire.log`

## 📋 Documentation

- **Roadmap** : [docs/roadmap.md](docs/roadmap.md)
- **Architecture** : [docs/architecture.md](docs/architecture.md)
- **Checklist** : [docs/checklist_projet.md](docs/checklist_projet.md)
- **Rapport** : [docs/rapport_pro.md](docs/rapport_pro.md)

## 🛡️ Sécurité et Conformité

### RGPD
- ✅ Données publiques uniquement
- ✅ Anonymisation quartier
- ✅ Registre des traitements
- ✅ Durée limitée de conservation

### OWASP
- ✅ Validation des entrées (Pydantic)
- ✅ Authentification JWT
- ✅ Rate limiting
- ✅ Protection injection SQL

## 📈 Timeline du Projet

- **Semaine 1** : ✅ Structure + Configuration
- **Semaine 2** : 🔄 C1 - Collecte
- **Semaines 3-4** : ⏳ C2-C3 - Traitement
- **Semaine 5** : ⏳ C4 - Base de données
- **Semaines 6-7** : ⏳ C5 - API REST
- **Semaine 8** : ⏳ Soutenance

## 🏆 Évaluation

- **Rapport professionnel** : Documentation complète
- **Démo fonctionnelle** : Pipeline end-to-end
- **Code qualité** : Tests > 80%, Git propre
- **Soutenance orale** : 5 compétences validées

---

**Développé par votre nom - Simplon.co 2024** 🎓