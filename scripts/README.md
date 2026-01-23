# Scripts Utilitaires - Observatoire Immobilier

Ce dossier contient les scripts de développement, migration et vérification pour le projet.

## Structure

```
scripts/
├── migration/          Scripts de migration et initialisation BDD
└── verification/       Scripts de diagnostic et vérification
```

## Migration (`migration/`)

Scripts pour créer et peupler la base de données RGPD.

### phase4_rgpd_implementation.py
**Description**: Implémentation complète de la Phase 4 - C4 (Base de Données RGPD)

**Usage**:
```bash
python scripts/migration/phase4_rgpd_implementation.py
```

**Fonctionnalités**:
- Création des tables RGPD (MCD/MLD/MPD)
- Initialisation du registre des traitements (Art. 30 RGPD)
- Politiques de rétention (Art. 5(1) RGPD)
- Migration et anonymisation des données
- Création des triggers automatiques
- Validation conformité RGPD

### simple_fix_rgpd.py
**Description**: Script simple de correction et migration des données

**Usage**:
```bash
python scripts/migration/simple_fix_rgpd.py
```

**Fonctionnalités**:
- Charge les données depuis `generated_properties.json`
- Insère dans la table `proprietes_anonymisees`
- Calcul automatique du prix/m²
- Gestion des erreurs d'insertion

### create_property_table.py
**Description**: Création manuelle de la table propriétés (SQLite direct)

**Usage**:
```bash
python scripts/migration/create_property_table.py
```

**Note**: Utilisé pour créer rapidement la table sans SQLAlchemy

### init_database.py
**Description**: Initialisation complète de la base de données

**Usage**:
```bash
python scripts/migration/init_database.py
```

### generate_demo_data.py
**Description**: Génération de données FICTIVES pour tests et démonstration

**IMPORTANT**: Ce script génère des données ALÉATOIRES, il ne scrape PAS de vrais sites.

**Usage**:
```bash
python scripts/migration/generate_demo_data.py
```

**Sortie**:
- `data/generated_properties.json` (2000 propriétés fictives)
- `data/generated_demographics.json` (20 villes fictives)

**Note**: Pour collecter de VRAIES données, utilisez les scrapers dans `src/scrapers/`

### generate_statistics.py
**Description**: Génère les statistiques agrégées pour l'API Analytics (C5)

**Usage**:
```bash
python scripts/migration/generate_statistics.py
```

**Fonctionnalités**:
- Agrège les données de `proprietes_anonymisees` par ville et mois
- Calcule prix moyen/min/max, surfaces moyennes
- Validation RGPD (groupes avec minimum 5 biens)
- Affiche un résumé des statistiques générées

**Important**: Ce script doit être exécuté après avoir peuplé `proprietes_anonymisees` pour que l'API Analytics fonctionne correctement.

---

## Vérification (`verification/`)

Scripts pour diagnostiquer et vérifier l'état de la base de données.

### check_db.py
**Description**: Vérification simple de la base avec SQLAlchemy

**Usage**:
```bash
python scripts/verification/check_db.py
```

**Fonctionnalités**:
- Vérifie la création des tables
- Compte les enregistrements
- Teste une requête simple

### check_rgpd_db.py
**Description**: Vérification complète de la conformité RGPD

**Usage**:
```bash
python scripts/verification/check_rgpd_db.py
```

**Fonctionnalités**:
- Vérifie toutes les tables RGPD
- Compte les enregistrements par table
- Affiche des exemples de données

### debug_rgpd_database.py
**Description**: Diagnostic approfondi avec insertion de test

**Usage**:
```bash
python scripts/verification/debug_rgpd_database.py
```

**Fonctionnalités**:
- Liste toutes les tables et colonnes
- Affiche la structure de chaque table
- Teste une insertion manuelle
- Diagnostique les problèmes de migration

### final_verification_rgpd.py
**Description**: Vérification finale avant validation C4

**Usage**:
```bash
python scripts/verification/final_verification_rgpd.py
```

**Fonctionnalités**:
- Audit complet de conformité RGPD
- Génération de rapport final
- Validation des contraintes et triggers

---

## Ordre d'exécution recommandé

### Première installation

```bash
# 1. Générer des données de test (FICTIVES)
python scripts/migration/generate_demo_data.py

# 2. Implémenter la base RGPD complète (recommandé)
python scripts/migration/phase4_rgpd_implementation.py

# OU créer manuellement la table puis migrer
python scripts/migration/create_property_table.py
python scripts/migration/simple_fix_rgpd.py

# 3. Générer les statistiques agrégées (IMPORTANT pour API Analytics)
python scripts/migration/generate_statistics.py

# 4. Vérifier l'installation
python scripts/verification/check_rgpd_db.py

# 5. Validation finale
python scripts/verification/final_verification_rgpd.py
```

### Vérification rapide

```bash
# Diagnostic complet
python scripts/verification/debug_rgpd_database.py
```

---

## Notes importantes

- Ces scripts sont pour le **développement** et **debugging** uniquement
- Les **vrais tests unitaires** sont dans le dossier `tests/`
- Pour l'API en production, utilisez les migrations SQLAlchemy via `src/models/`
- Tous les scripts respectent l'encodage UTF-8 pour Windows

---

## Dépendances

Ces scripts nécessitent:
- SQLAlchemy
- pandas (pour generate_realistic_data.py)
- Les modèles dans `src/models/rgpd_models.py`

Installer avec:
```bash
pip install -r requirements.txt
```
