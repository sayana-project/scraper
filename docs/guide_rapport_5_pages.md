# Rapport Professionnel - Observatoire Immobilier Public

**Certification Developpeur en Intelligence Artificielle**
**E1 : Gestion des donnees**

---

## Sommaire

I. Automatiser l'extraction des donnees depuis un service web
   - A. Contexte du projet
   - B. Specifications techniques
   - C. Extraction des donnees

II. Developper des requetes de type SQL d'extraction des donnees

III. Developper des regles d'agregation de donnees issues de differentes sources

IV. Creer une base de donnees

V. Developper une API mettant a disposition le jeu de donnees

---

## I. Automatiser l'extraction des donnees depuis un service web

### A. Contexte du projet

Le projet "Observatoire Immobilier Public" est un projet personnel developpe dans le cadre de la certification Simplon. Ce projet repond a un besoin concret : les donnees immobilieres sont dispersees sur de nombreux sites web et il n'existe pas d'outil centralise pour analyser le marche immobilier francais de maniere automatisee.

L'objectif est de developper une application permettant de :
- Collecter automatiquement des donnees immobilieres publiques
- Agreger et nettoyer ces donnees
- Les stocker dans une base conforme au RGPD
- Les exposer via une API REST securisee

Les utilisateurs cibles sont les analystes immobiliers, les acheteurs potentiels et les professionnels du secteur qui souhaitent obtenir des statistiques fiables sur le marche.

L'organisation du travail a suivi les phases suivantes :
- Phase 1-2 : Collecte multi-sources (C1)
- Phase 3-4 : Traitement et agregation (C2-C3)
- Phase 5 : Base de donnees RGPD (C4)
- Phase 6-7 : API REST (C5)
- Phase 8 : Tests et documentation

### B. Specifications techniques

Le projet est developpe en Python 3.10. Le code est redige dans Visual Studio Code et versionne sur un depot GitHub.

Technologies utilisees :
- **Framework API** : FastAPI (documentation automatique, performant)
- **Base de donnees** : SQLite avec SQLAlchemy (ORM)
- **Scraping** : BeautifulSoup4, Requests
- **Traitement** : Pandas, NumPy
- **Securite** : JWT (python-jose), bcrypt
- **Tests** : pytest

Architecture du projet :
```
src/
  scrapers/      -> Collecte des donnees (C1)
  repositories/  -> Requetes SQL (C2)
  services/      -> Traitement et agregation (C3)
  models/        -> Modeles de donnees RGPD (C4)
  api/           -> Endpoints REST (C5)
```

### C. Extraction des donnees

Les donnees sont extraites a partir de plusieurs types de sources :

1. **Scraping web** : Sites d'annonces immobilieres publiques (SeLoger, LeBonCoin)
2. **API REST externe** : API INSEE pour les donnees demographiques
3. **Fichiers de donnees** : Import de fichiers CSV et JSON

Le script d'extraction est disponible dans le dossier `src/scrapers/`. Il comprend :
- L'initialisation des connexions externes
- Les regles de collecte pour chaque source
- La gestion des erreurs et des timeouts
- La sauvegarde des donnees brutes

Exemple de code d'extraction (scraper SeLoger) :
```python
class SeLogerScraper:
    def __init__(self):
        self.base_url = "https://www.seloger.com"
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def scrape_properties(self, city, max_pages=5):
        properties = []
        for page in range(1, max_pages + 1):
            response = requests.get(url, headers=self.headers)
            # Extraction des donnees...
        return properties
```

---

## II. Developper des requetes de type SQL d'extraction des donnees

Le script d'extraction realise des transformations pour nettoyer les donnees :
- Filtrage des annonces valides
- Selection et nettoyage des colonnes
- Suppression des doublons
- Traitement des valeurs manquantes

Les requetes SQL sont implementees via le Repository Pattern dans `src/repositories/property_repository.py`.

Exemples de requetes :

**Requete simple avec filtres :**
```sql
SELECT * FROM proprietes_anonymisees
WHERE ville = 'Paris' AND prix_euros BETWEEN 100000 AND 500000
ORDER BY prix_m2_euros DESC
```

**Requete avec agregation :**
```sql
SELECT ville, AVG(prix_m2_euros) as prix_moyen, COUNT(*) as nb_biens
FROM proprietes_anonymisees
GROUP BY ville
ORDER BY prix_moyen DESC
```

**Requete avec jointure :**
```sql
SELECT p.*, d.population
FROM proprietes_anonymisees p
LEFT JOIN donnees_demographiques d ON p.code_postal = d.postal_code
WHERE p.ville = 'Lyon'
```

Les requetes sont optimisees avec des index sur les colonnes frequemment utilisees (ville, code_postal, prix_euros).

---

## III. Developper des regles d'agregation de donnees issues de differentes sources

Apres les etapes de nettoyage, le script enregistre les donnees dans la base de donnees et realise l'agregation des differentes sources.

Le service d'agregation (`src/services/property_service.py`) effectue :

1. **Dedoublonnage** : Suppression des annonces identiques basee sur titre + code postal + surface + prix

2. **Standardisation des formats** :
   - Prix : suppression des caracteres non numeriques
   - Surface : conversion en entier (m2)
   - Code postal : format 5 chiffres
   - Ville : premiere lettre majuscule

3. **Validation des regles metier** :
   - Prix au m2 entre 100 et 50 000 euros
   - Surface entre 10 et 1000 m2
   - Code postal francais valide

4. **Calcul des indicateurs** :
   - Prix moyen par ville
   - Prix au m2 moyen
   - Distribution des prix (quartiles)

Exemple de fonction de nettoyage :
```python
def standardize_property_data(self, prop):
    # Standardisation du prix
    prop['price'] = int(re.sub(r'[^\d]', '', str(prop['price'])))

    # Standardisation du code postal
    prop['postal_code'] = prop['postal_code'].strip().zfill(5)

    # Standardisation de la ville
    prop['city'] = prop['city'].strip().title()

    return prop
```

Resultats de l'agregation :
- 2000 proprietes nettoyees et validees
- 20 villes couvertes
- 4 types de sources agregees

---

## IV. Creer une base de donnees

### Modele conceptuel des donnees

```
PROPRIETE_ANONYMISEE              DONNEE_DEMOGRAPHIQUE
-------------------               --------------------
id_prop (PK)                      id_demo (PK)
code_postal          n -------- 1 postal_code
ville                             city
quartier_anonymise                population
surface_m2                        source
prix_euros
prix_m2_euros
type_bien
source_collecte
date_collecte
```

### Modele physique des donnees

| Table | Colonne | Type | Contrainte |
|-------|---------|------|------------|
| proprietes_anonymisees | id_prop | INTEGER | PK |
| | code_postal | VARCHAR(5) | INDEX |
| | ville | VARCHAR(100) | INDEX |
| | quartier_anonymise | VARCHAR(50) | |
| | surface_m2 | INTEGER | > 0 |
| | prix_euros | INTEGER | > 0 |
| | prix_m2_euros | DECIMAL | |
| | source_collecte | VARCHAR(20) | |
| | date_collecte | DATE | |

La base de donnees SQLite est choisie car elle est legere, ne necessite pas de serveur et convient pour un projet de demonstration.

### Conformite RGPD

Les donnees stockees ne contiennent pas d'adresses precises (anonymisation au niveau quartier). Les mesures RGPD implementees sont :

| Article RGPD | Mesure implementee |
|--------------|-------------------|
| Art. 5 - Minimisation | Seules les donnees necessaires sont collectees |
| Art. 25 - Privacy by design | Anonymisation des la collecte |
| Art. 30 - Registre | 3 traitements documentes |
| Art. 32 - Securite | Chiffrement, acces controle |

Tables RGPD creees :
- `registre_traitements_rgpd` : Documentation des traitements
- `politiques_retention_rgpd` : Durees de conservation (5 ans donnees, 12 mois logs)
- `logs_access_rgpd` : Tracabilite des acces

---

## V. Developper une API mettant a disposition le jeu de donnees

L'API REST est developpee avec FastAPI. Elle est protegee par authentification JWT.

### Documentation de l'API

L'API dispose d'une documentation automatique accessible sur `/api/v1/docs` (Swagger UI).

### Endpoints disponibles

| Methode | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/v1/health | Verification de sante |
| POST | /api/v1/auth/token | Authentification (JWT) |
| GET | /api/v1/auth/me | Info utilisateur connecte |
| GET | /api/v1/properties | Liste des proprietes |
| GET | /api/v1/properties/{id} | Detail d'une propriete |
| POST | /api/v1/properties | Creer une propriete |
| PUT | /api/v1/properties/{id} | Modifier une propriete |
| DELETE | /api/v1/properties/{id} | Supprimer une propriete |
| GET | /api/v1/analytics/overview | Statistiques globales |
| GET | /api/v1/analytics/cities | Statistiques par ville |

### Securite

- **Authentification** : JWT avec expiration 30 minutes
- **Validation** : Schemas Pydantic pour toutes les entrees
- **Protection SQL** : ORM SQLAlchemy (pas de requetes brutes)
- **CORS** : Configuration des origines autorisees

Exemple d'endpoint :
```python
@router.get("/properties/", response_model=List[PropertyResponse])
async def get_properties(
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    service: PropertyService = Depends(get_property_service)
):
    return service.get_properties(skip, limit, city)
```

### Tests

34 tests pytest couvrent l'ensemble des endpoints :
- Tests health check : 4 tests
- Tests authentification : 7 tests
- Tests CRUD proprietes : 10 tests
- Tests validation : 4 tests
- Tests analytics : 4 tests
- Tests HTTP : 3 tests
- Tests integration : 3 tests

Resultat : **34/34 tests passes (100%)**

---

## Donnees du projet

### Statistiques globales

| Metrique | Valeur |
|----------|--------|
| Nombre de proprietes | 2 000 |
| Prix minimum | 25 906 euros |
| Prix maximum | 3 545 166 euros |
| Prix moyen | 290 021 euros |
| Surface moyenne | 74 m2 |
| Prix/m2 moyen | 3 943 euros |

### Prix par ville (Top 5)

| Ville | Prix/m2 moyen |
|-------|---------------|
| Paris | 12 504 euros |
| Lyon | 5 222 euros |
| Nice | 4 807 euros |
| Bordeaux | 4 705 euros |
| Aix-en-Provence | 4 574 euros |

### Sources de donnees

| Source | Nombre | Type |
|--------|--------|------|
| seloger | 391 | Scraping web |
| leboncoin | 366 | Scraping web |
| insee | 389 | API REST |
| csv_import | 422 | Fichier |
| json_import | 432 | Fichier |

---

## Conclusion

Ce projet a permis de valider les 5 competences du bloc E1 :
- **C1** : Extraction multi-sources (scraping, API, fichiers)
- **C2** : Requetes SQL optimisees
- **C3** : Agregation et nettoyage des donnees
- **C4** : Base de donnees conforme RGPD
- **C5** : API REST securisee avec documentation

Le code source est versionne et accessible sur GitHub.
