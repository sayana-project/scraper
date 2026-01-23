# Rapport Professionnel - Observatoire Immobilier Public

## 📋 Contexte du Projet

### Acteurs
- **Développeur** : Étudiant Simplon.co
- **Organisme évaluateur** : Simplon.co
- **Utilisateurs cibles** : Analystes immobiliers, acheteurs, professionnels secteur

### Objectifs Fonctionnels
- Automatiser la collecte de données immobilières publiques
- Analyser les tendances du marché immobilier français
- Fournir des statistiques fiables et anonymisées
- Mettre à disposition les données via une API sécurisée

### Objectifs Techniques
- Implémenter 5 compétences clés (C1-C5) du diplôme
- Respecter les exigences RGPD et OWASP
- Créer une solution scalable et maintenable

## 🏗️ Spécifications Techniques

### Technologies
- **Backend** : Python 3.9+
- **Framework API** : FastAPI (alternatives : Flask, Django REST)
- **Scraping** : BeautifulSoup4, Scrapy, Selenium
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **ORM** : SQLAlchemy
- **Sécurité** : JWT, bcrypt, python-jose
- **Documentation API** : OpenAPI/Swagger

### Services Externes
- **Sources de données** : Sites immobiliers publics (SeLoger, LeBonCoin, notaires)
- **API externes** : INSEE (données démographiques)
- **Email** : SMTP pour alertes (avec consentement)

### Exigences de Programmation
- Python 3.9+ (type hints recommandés)
- Gestion d'erreurs robuste
- Logging structuré
- Tests unitaires (pytest)
- Documentation complète

### Environnements et Contraintes
- **Développement** : Windows 11, Python local
- **Production** : Container Docker (recommandé)
- **Contraintes RGPD** : Anonymisation adresses, registre des traitements
- **Performance** : Rate limiting, cache réponses API

## 📊 Périmètre Fonctionnel

### Fonctionnalités Incluses
1. **Collecte multi-sources** (C1)
   - Scraping sites immobiliers publics
   - API REST intégration
   - Import fichiers CSV/JSON
   - Connexion base de données existantes

2. **Traitement des données** (C2-C3)
   - Nettoyage et dédoublonnage
   - Standardisation formats
   - Calcul indicateurs (prix/m², évolutions)
   - Agrégation par zone géographique

3. **Stockage sécurisé** (C4)
   - Base données relationnelle
   - Anonymisation données personnelles
   - Conformité RGPD complète
   - Backups automatiques

4. **Exposition API** (C5)
   - Endpoints REST sécurisés
   - Authentification JWT
   - Documentation OpenAPI
   - Rate limiting

### Fonctionnalités Exclues
- Prédictions prix (machine learning)
- Interface web complète (API uniquement)
- Données immobilières privées
- Transactions financières

## 🗓️ Organisation et Planification

### Phases de Développement

**Phase 1 - Collecte (C1)** : 2 semaines
- Configuration scrapers
- Scripts extraction multi-sources
- Tests robustesse

**Phase 2 - Traitement (C2-C3)** : 2 semaines
- Développement requêtes SQL
- Scripts agrégation
- Algorithmes nettoyage

**Phase 3 - Base données (C4)** : 1 semaine
- Modélisation Merise
- Scripts migration
- Mise en conformité RGPD

**Phase 4 - API (C5)** : 2 semaines
- Développement endpoints
- Sécurisation authentification
- Documentation OpenAPI

**Phase 5 - Tests & Documentation** : 1 semaine
- Tests unitaires/intégration
- Rapport professionnel
- Préparation soutenance

### Livrables Finaux
- Code source complet et versionné (Git)
- Documentation technique et utilisateur
- Base de données fonctionnelle
- API REST sécurisée
- Rapport de conformité RGPD
- Soutenance orale

## 🛡️ Sécurité et Conformité

### Mesures OWASP
- Validation entrées utilisateur
- Protection injections SQL/XSS
- Gestion sécurisée sessions
- HTTPS obligatoire
- Rate limiting endpoints

### Conformité RGPD
- **Données collectées** : Prix, surface, localisation (niveau quartier)
- **Finalité** : Analyse statistique marché immobilier
- **Base légale** : Intérêt public (données publiques)
- **Droits utilisateurs** : Accès, rectification, suppression
- **Durée conservation** : 2 ans maximum
- **Sous-traitants** : Hébergeur cloud certifié UE

### Registre des Traitements
Consultez le fichier `rgpd_register.md` pour le détail complet des traitements de données personnelles.