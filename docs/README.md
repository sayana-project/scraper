# Documentation - Observatoire Immobilier

Cette documentation couvre l'architecture, les choix techniques et la conformité RGPD du projet.

## Structure de la documentation

### Documents principaux

| Fichier | Description | Pour qui? |
|---------|-------------|-----------|
| [architecture.md](architecture.md) | Architecture N-Tiers du projet | Développeurs, jury technique |
| [mcd_rgpd.md](mcd_rgpd.md) | Modèle Conceptuel de Données (Merise) | Jury C4, architectes BDD |
| [mld_rgpd.md](mld_rgpd.md) | Modèle Logique de Données (SQL) | Jury C4, DBA |
| [technical_guide.md](technical_guide.md) | Guide technique complet | Développeurs |
| [rapport_pro.md](rapport_pro.md) | Rapport professionnel de soutenance | Jury d'évaluation |
| [roadmap.md](roadmap.md) | Planning et jalons du projet | Chef de projet, jury |
| [checklist_projet.md](checklist_projet.md) | Checklist validation C1-C5 | Auto-évaluation |
| [objectif_projet.md](objectif_projet.md) | Objectifs et périmètre | Tous publics |
| [guide_rapport_5_pages.md](guide_rapport_5_pages.md) | Template rapport soutenance | Candidat |

---

## Organisation par compétences Simplon

### C1 - Collecte de données
**Fichiers**: [architecture.md](architecture.md) (section Scrapers), [technical_guide.md](technical_guide.md) (section C1)

Démontre la collecte multi-sources:
- Scraping web (BeautifulSoup, Selenium)
- APIs REST (INSEE)
- Fichiers CSV/JSON

### C2 - Requêtes SQL optimisées
**Fichiers**: [mcd_rgpd.md](mcd_rgpd.md), [mld_rgpd.md](mld_rgpd.md)

Architecture Repository Pattern avec:
- Modèles SQLAlchemy
- Index optimisés
- Requêtes complexes (JOIN, agrégation)

### C3 - Traitement et agrégation
**Fichiers**: [architecture.md](architecture.md) (Service Layer), [technical_guide.md](technical_guide.md) (section C3)

Pipeline de traitement:
- Nettoyage et validation (Pandas)
- Agrégation multi-critères
- Transformation pour anonymisation

### C4 - Base de données RGPD
**Fichiers**: [mcd_rgpd.md](mcd_rgpd.md), [mld_rgpd.md](mld_rgpd.md)

Conformité RGPD démontrée:
- Modélisation Merise complète (MCD/MLD/MPD)
- Anonymisation au niveau quartier
- Registre des traitements (Art. 30)
- Politiques de rétention (Art. 5.1)

### C5 - API REST sécurisée
**Fichiers**: [architecture.md](architecture.md) (API Layer), [technical_guide.md](technical_guide.md) (section C5)

API FastAPI avec:
- Endpoints CRUD + Analytics
- Authentification JWT
- Validation Pydantic
- Documentation OpenAPI

---

## Archives

Le dossier `_archives/` contient d'anciennes versions et travaux hors périmètre:

- **E1/** : Anciennes versions de la documentation (conservées pour historique)
- **E3/** : Préparation future (vide)
- **C9/** : Compétences C9-C13 Machine Learning MLOps (hors périmètre projet actuel)

Ces dossiers sont conservés mais **ne font pas partie du livrable final**.

---

## Pour le jury

### Lecture recommandée (ordre)

1. **[objectif_projet.md](objectif_projet.md)** - Comprendre le contexte et les objectifs
2. **[architecture.md](architecture.md)** - Vue d'ensemble technique
3. **[mcd_rgpd.md](mcd_rgpd.md) + [mld_rgpd.md](mld_rgpd.md)** - Architecture base de données RGPD
4. **[rapport_pro.md](rapport_pro.md)** - Rapport complet de soutenance

### Checklist validation

Utilisez [checklist_projet.md](checklist_projet.md) pour vérifier que toutes les compétences C1-C5 sont validées.

---

## Mise à jour de la documentation

Cette documentation est maintenue tout au long du projet.

**Dernière mise à jour**: Janvier 2025

**Version du projet**: 1.0.0 (Phase 4 - C4 complétée)

---

## Contact

Pour toute question sur la documentation:
- Consulter d'abord [technical_guide.md](technical_guide.md)
- Vérifier [checklist_projet.md](checklist_projet.md) pour l'état d'avancement
- Référence: Formation Simplon.co Développeur Junior 2024-2025
