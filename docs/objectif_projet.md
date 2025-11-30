Compétences à valider — Bloc 1 
1. Collecte de données
Savoir identifier et exploiter différentes sources de données :
Sites web (scraping, crawling)
API (REST, GraphQL)
Fichiers (CSV, JSON, XML…)
Big Data (streaming, batch)
Bases de données (SQL, NoSQL)
2. Traitement et agrégation
Maîtriser les étapes d’extraction, nettoyage, et fusion des données :
Filtrage, normalisation, dédoublonnage
Agrégation multi-source
Structuration des données pour usage IA
3. Stockage structuré
Savoir concevoir et interroger une base de données relationnelle (SQL) :
Création de schémas
Requêtes SELECT, JOIN, GROUP BY…
Optimisation des performances
4. Exposition des données
Mettre à disposition les données via une API REST :
Développement en Python (ex: Flask, FastAPI)
Endpoints GET/POST sécurisés
Documentation et test de l’API
C1. Automatiser l’extraction de données depuis un service web, une page web (scraping*), un fichier de données, une
base de données et un système big data* en programmant le script* adapté afin de pérenniser la collecte des données
nécessaires au projet.
C2. Développer des requêtes de type SQL d’extraction des données depuis un système de gestion de base de données et
un système big data en appliquant le langage de requête propre au système afin de préparer la collecte des données
nécessaires au projet.
C3. Développer des règles d'agrégation de données issues de différentes sources en programmant, sous forme de script,
la suppression des entrées corrompues et en programmant l’homogénéisation des formats des données afin de préparer
le stockage du jeu de données final.
C4. Créer une base de données dans le respect du RGPD en élaborant les modèles conceptuels et physiques des
données à partir des données préparées et en programmant leur import afin de stocker le jeu de données du projet.
C5. Développer une API mettant à disposition le jeu de données en utilisant l’architecture REST afin de permettre
l’exploitation du jeu de données par les autres composants du projet.
C1. Automatiser l’extraction
de données
depuis un service web, une
page web (scraping*), un
fichier de données, une base
de données et un système big
data* en, programmant le
script* adapté afin de
pérenniser la collecte des
données
nécessaires au projet.
E1. Mise en situation (C1, C2, C3,
C4, C5)
L’évaluation doit se faire dans un contexte
de réalisation d’un service numérique réel
ou fictif basé sur l’usage de données, à
partir du cadrage pour la réalisation d’un
service numérique (spécifications
fonctionnelles et techniques par exemple).
Le projet évalué a pour but d’optimiser,
d’automatiser, de pérenniser et de mettre à
- La présentation du projet et de son contexte
est complète : acteurs, objectifs fonctionnels et
techniques, environnements et contraintes
techniques, budget, organisation du travail et
planification.
- Les spécifications techniques précisent : les
technologies et outils, les services externes, les
exigences de programmation
(langages), l’accessibilité (disponibilité, accès).
- Le périmètre des spécifications techniques est
complet : il couvre l’ensemble des moyens


SIMPLON.CO | Fabrique sociale de codeurs | SAS agréée ESUS au capital de 448.390 euros | RCS Bobigny 792 791 329 | Siège social : 55 Rue de Vincennes, Montreuil (93100)
Enregistré en tant qu’organisme de formation auprès de la DRIEETS IDF sous le N° 11 93 06676 93. Cet enregistrement ne vaut pas agrément de l’État | N°UAI : 0932753M
N° TVA : FR 56 79279132900016
disposition les flux de données et les
données, utiles et nécessaires à la réalisation
du service numérique, par les
équipes techniques (par exemple en
analyse statistique, en business intelligence, en
machine learning ou encore en intelligence
artificielle).
Livrable : rapport professionnel individuel
Évaluation :
- Correction du rapport professionnel
- Soutenance orale individuelle
techniques à mettre en œuvre pour l’extraction
et l'agrégation des données en un jeu de
données brutes
final.
- Le script d’extraction des données est
fonctionnel : toutes les données visées sont
effectivement récupérées à l’issue de
l’exécution du script.
- Le script comprend un point de lancement,
l’initialisation des dépendances et des
connexions externes, les règles logiques de
traitement, la gestion des erreurs et des
exceptions, la fin du traitement et la
sauvegarde des résultats.
- Le script d’extraction des données est
versionné* et accessible depuis un dépôt Git*.
- L’extraction des données est faite depuis un
mix entre au moins les sources suivantes : un
service web (API REST), un fichier de données,
un scraping, une base de données et un
système big data.
C2. Développer des
requêtes de type SQL
d’extraction des données
depuis un système de gestion
de base de données et un
système big data en
appliquant le langage de
requête propre au système
afin de préparer la collecte
des données nécessaires au
- Les requêtes de type SQL pour la collecte
de données sont fonctionnelles : les données
visées sont effectivement extraites suite à
l'exécution des requêtes.
- La documentation des requêtes met en
lumière choix de sélections, filtrages,
conditions, jointures, etc., en fonction des
objectifs de collecte.
- La documentation explicite les
optimisations appliquées aux requêtes .
SIMPLON.CO | Fabrique sociale de codeurs | SAS agréée ESUS au capital de 448.390 euros | RCS Bobigny 792 791 329 | Siège social : 55 Rue de Vincennes, Montreuil (93100)
Enregistré en tant qu’organisme de formation auprès de la DRIEETS IDF sous le N° 11 93 06676 93. Cet enregistrement ne vaut pas agrément de l’État | N°UAI : 0932753M
N° TVA : FR 56 79279132900016
projet.
C3. Développer des règles
d'agrégation de données
issues de différentes sources
en programmant, sous forme
de script, la suppression des
entrées corrompues et en
programmant
l’homogénéisation des
formats des données afin de
préparer le stockage du jeu de
données final.
- Le script d’agrégation des données est
fonctionnel : les données sont effectivement
agrégées, nettoyées et normalisées en un seul
jeu de données à l’issue de l’exécution du
script.
- Le script d’agrégation des données est
versionné et accessible depuis un dépôt Git.
- La documentation du script d’agrégation est
complète : dépendances, commandes, les
enchaînements logiques de l’algorithme, les
choix de nettoyage et d’homogénéisation des
formats données.

ACQUIS
C4. Créer une base de
données dans le respect du
RGPD en élaborant les
modèles conceptuels et
physiques des données à
partir des données préparées
et en programmant leur
import afin de stocker le jeu
de données du projet.
- Les modélisations des données respectent la
méthode et le formalisme Merise.
- Le modèle physique des données est
fonctionnel : il est intégré avec succès lors de la
création de la base de données, sans erreur.
- La base de données est choisie au regard de la
modélisation des données et des contraintes
du projet.
- La reproduction des procédures d’installation
décrites (base de données et API) a pour
résultat un système conforme aux objets
techniques attendus..
- Le script d’import fourni est fonctionnel : il
permet l’insertion des données dans le système
mis en place.
- La documentation technique du script
d’import est versionné à la racine du même
dépôt Git que celui utilisé pour le script
d’import.
SIMPLON.CO | Fabrique sociale de codeurs | SAS agréée ESUS au capital de 448.390 euros | RCS Bobigny 792 791 329 | Siège social : 55 Rue de Vincennes, Montreuil (93100)
Enregistré en tant qu’organisme de formation auprès de la DRIEETS IDF sous le N° 11 93 06676 93. Cet enregistrement ne vaut pas agrément de l’État | N°UAI : 0932753M
N° TVA : FR 56 79279132900016
- Les documentations techniques des
scripts couvrent les parties suivantes :
- les dépendances nécessaires pour la
réutilisation des scripts (langages,
dépendances externes, etc)
- les commandes pour l’exécution des
scripts.
- Le registre des traitements de données
personnelles intègre l’ensemble des
traitements de données personnelles impliqués
dans la base de données.
- Les procédures de tri des données
personnelles pour la mise en conformité de la
base de données avec le RGPD sont rédigées.
- Les procédures de tri détaillent les
traitements de conformité (automatisés ou
non) à appliquer ainsi que leur fréquence
d’exécution.
C5. Développer une API
mettant à disposition le jeu
de données en utilisant
l’architecture REST afin de
permettre l’exploitation du
jeu de données par les autres
composants du projet.
- La documentation technique de l’API (REST)
couvre tous les points de terminaisons.
- La documentation technique couvre les règles
d’authentification et/ou d’autorisation de l’API.
- La documentation technique respecte les
standards du modèle choisi (par exemple
OpenAPI*).
- L’API REST est fonctionnelle pour l’accès aux
données du projet : elle restreint par une
autorisation (ou authentification) l'accès aux
données,
- L’API REST est fonctionnelle pour la mise à
disposition : elle permet la récupération de
SIMPLON.CO | Fabrique sociale de codeurs | SAS agréée ESUS au capital de 448.390 euros | RCS Bobigny 792 791 329 | Siège social : 55 Rue de Vincennes, Montreuil (93100)
Enregistré en tant qu’organisme de formation auprès de la DRIEETS IDF sous le N° 11 93 06676 93. Cet enregistrement ne vaut pas agrément de l’État | N°UAI : 0932753M
N° TVA : FR 56 79279132900016
l’ensemble des données nécessaires au projet,
comme prévu selon les spécifications données