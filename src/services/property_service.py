# Property Service (C3) - Nettoyage et Agrégation des données
import logging
from typing import List, Dict, Any, Optional
import json
import pandas as pd
from datetime import datetime, timedelta
import re

from src.repositories.property_repository import PropertyRepository
from src.models import Property, DemographicData, AggregatedProperty

logger = logging.getLogger(__name__)

class PropertyService:
    """Service Layer pour le nettoyage et l'agrégation des données (C3)"""

    def __init__(self, database_url: str = "sqlite:///data/immobilier.db"):
        self.property_repo = PropertyRepository(database_url)

    # ===== MÉTHODES DE NETTOYAGE (C3) =====

    def clean_property_data(self, raw_properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Nettoie les données brutes des propriétés (C3)
        - Suppression des doublons
        - Standardisation des formats
        - Validation des données
        - Gestion des valeurs manquantes
        """
        logger.info(f"Début nettoyage de {len(raw_properties)} propriétés brutes")

        cleaned_properties = []
        seen_properties = set()  # Pour détection des doublons

        for i, prop in enumerate(raw_properties):
            try:
                # 1. Validation des champs obligatoires
                if not self._validate_required_fields(prop):
                    logger.warning(f"Propriété {i} ignorée : champs manquants")
                    continue

                # 2. Standardisation des données
                prop = self._standardize_property_data(prop)

                # 3. Détection des doublons
                prop_key = self._create_property_key(prop)
                if prop_key in seen_properties:
                    logger.debug(f"Propriété {i} ignorée : doublon détecté")
                    continue
                seen_properties.add(prop_key)

                # 4. Validation finale
                if self._validate_business_rules(prop):
                    cleaned_properties.append(prop)
                    logger.debug(f"Propriété {i} nettoyée et validée")
                else:
                    logger.warning(f"Propriété {i} ignorée : règles métier non respectées")

            except Exception as e:
                logger.error(f"Erreur nettoyage propriété {i}: {e}")
                continue

        logger.info(f"Nettoyage terminé : {len(cleaned_properties)}/{len(raw_properties)} propriétés conservées")
        return cleaned_properties

    def _validate_required_fields(self, prop: Dict[str, Any]) -> bool:
        """Valide que les champs obligatoires sont présents et valides"""
        required_fields = ['title', 'price', 'surface', 'postal_code', 'city']

        for field in required_fields:
            if field not in prop or prop[field] is None:
                return False

        # Validation spécifique
        if prop['price'] <= 0:
            return False
        if prop['surface'] <= 0:
            return False
        if len(str(prop['postal_code'])) not in [4, 5]:  # Codes postaux FR/International
            return False
        if len(str(prop['city']).strip()) < 2:
            return False

        return True

    def _standardize_property_data(self, prop: Dict[str, Any]) -> Dict[str, Any]:
        """Standardise les formats de données"""
        # Standardisation du prix (suppression des caractères non numériques)
        if isinstance(prop['price'], str):
            price_clean = re.sub(r'[^\d]', '', str(prop['price']))
            prop['price'] = int(price_clean) if price_clean else 0

        # Standardisation de la surface (suppression de "m²", etc.)
        if isinstance(prop['surface'], str):
            surface_clean = re.sub(r'[^\d]', '', str(prop['surface']))
            prop['surface'] = int(surface_clean) if surface_clean else 1

        # Standardisation du code postal (suppression des espaces)
        if isinstance(prop['postal_code'], str):
            prop['postal_code'] = prop['postal_code'].strip().zfill(5)  # Force 5 chiffres

        # Standardisation de la ville (première lettre majuscule)
        if isinstance(prop['city'], str):
            prop['city'] = prop['city'].strip().title()

        # Standardisation du titre (trim + majuscules)
        if isinstance(prop['title'], str):
            prop['title'] = prop['title'].strip().title()

        # Normalisation de la source
        valid_sources = ['seloger', 'leboncoin', 'csv_import', 'insee', 'json_import']
        if prop.get('source') not in valid_sources:
            prop['source'] = 'other'

        # Ajout timestamp si manquant
        if not prop.get('scraped_at'):
            prop['scraped_at'] = datetime.now().isoformat()

        return prop

    def _create_property_key(self, prop: Dict[str, Any]) -> str:
        """Crée une clé unique pour détecter les doublons"""
        return f"{prop['title']}|{prop['postal_code']}|{prop['surface']}|{prop.get('price', 0)}"

    def _validate_business_rules(self, prop: Dict[str, Any]) -> bool:
        """Valide les règles métier spécifiques"""
        # Règle 1: Prix au m² raisonnable (entre 100€ et 50,000€/m²)
        price_per_m2 = prop['price'] / prop['surface']
        if price_per_m2 < 100 or price_per_m2 > 50000:
            logger.warning(f"Prix au m² suspect: {price_per_m2:.2f}€ pour {prop['title']}")
            return False

        # Règle 2: Taille raisonnable (entre 10m² et 1000m²)
        if prop['surface'] < 10 or prop['surface'] > 1000:
            logger.warning(f"Surface suspecte: {prop['surface']}m² pour {prop['title']}")
            return False

        # Règle 3: Prix raisonnable (entre 10,000€ et 10,000,000€)
        if prop['price'] < 10000 or prop['price'] > 10000000:
            logger.warning(f"Prix suspect: {prop['price']}€ pour {prop['title']}")
            return False

        # Règle 4: Code postal français valide
        postal_code = str(prop['postal_code'])
        if len(postal_code) == 5 and postal_code.isdigit():
            dept = int(postal_code[:2])
            if dept < 1 or dept > 95:  # Départements français valides
                logger.warning(f"Département suspect: {dept} pour {prop['title']}")
                return False

        return True

    # ===== MÉTHODES D'AGRÉGATION (C3) =====

    def aggregate_properties_by_location(self, cleaned_properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Agrège les données par localisation (C3)
        - Calcul des statistiques par ville/code postal
        - Fusion des données démographiques
        - Calcul des indicateurs dérivés
        """
        logger.info(f"Début agrégation par localisation de {len(cleaned_properties)} propriétés")

        # Conversion en DataFrame pour agrégation efficace
        df = pd.DataFrame(cleaned_properties)

        # Agrégation par ville et code postal
        aggregated_data = []

        for (city, postal_code), group in df.groupby(['city', 'postal_code']):
            try:
                # Statistiques de base
                stats = {
                    'postal_code': postal_code,
                    'city': city,
                    'total_properties': len(group),
                    'avg_price': round(group['price'].mean(), 2),
                    'min_price': int(group['price'].min()),
                    'max_price': int(group['price'].max()),
                    'avg_surface': round(group['surface'].mean(), 2),
                    'sources': list(group['source'].unique()),
                    'sources_count': len(group['source'].unique()),
                    'price_per_m2_mean': round((group['price'] / group['surface']).mean(), 2),
                    'price_per_m2_median': round((group['price'] / group['surface']).median(), 2),
                    'aggregation_date': datetime.now().isoformat(),
                    'data_period_start': group['scraped_at'].min(),
                    'data_period_end': group['scraped_at'].max()
                }

                # Analyse avancée
                stats.update(self._calculate_advanced_stats(group))

                aggregated_data.append(stats)
                logger.debug(f"Agrégation {city} {postal_code}: {len(group)} propriétés")

            except Exception as e:
                logger.error(f"Erreur agrégation {city} {postal_code}: {e}")
                continue

        logger.info(f"Agrégation terminée : {len(aggregated_data)} localisations")
        return aggregated_data

    def _calculate_advanced_stats(self, group) -> Dict[str, Any]:
        """Calcule des statistiques avancées pour un groupe de propriétés"""
        try:
            # Distribution des prix par quartiles
            price_quartiles = group['price'].quantile([0.25, 0.5, 0.75]).to_dict()

            # Distribution des surfaces par quartiles
            surface_quartiles = group['surface'].quantile([0.25, 0.5, 0.75]).to_dict()

            # Types de propriétés (déduction depuis titres)
            property_types = self._extract_property_types(group['title'])

            # Sources par fréquence
            source_counts = group['source'].value_counts().to_dict()

            return {
                'price_q1': round(price_quartiles.get(0.25, 0), 2),
                'price_median': round(price_quartiles.get(0.5, 0), 2),
                'price_q3': round(price_quartiles.get(0.75, 0), 2),
                'surface_q1': round(surface_quartiles.get(0.25, 0), 2),
                'surface_median': round(surface_quartiles.get(0.5, 0), 2),
                'surface_q3': round(surface_quartiles.get(0.75, 0), 2),
                'property_types': property_types,
                'source_distribution': source_counts
            }
        except Exception as e:
            logger.warning(f"Erreur calcul stats avancées: {e}")
            return {}

    def _extract_property_types(self, titles) -> Dict[str, int]:
        """Extrait les types de propriétés depuis les titres"""
        type_patterns = {
            'studio': r'\bstudio|t1\b',
            'appartement': r'\bappartement|t[2-9]\b|f\d+\b',
            'maison': r'\bmaison|villa\b',
            'terrain': r'\bterrain\b'
        }

        type_counts = {'studio': 0, 'appartement': 0, 'maison': 0, 'terrain': 0, 'autre': 0}

        for title in titles:
            if pd.isna(title):
                continue

            title_lower = str(title).lower()
            found_type = False

            for prop_type, pattern in type_patterns.items():
                if prop_type != 'autre' and re.search(pattern, title_lower, re.IGNORECASE):
                    type_counts[prop_type] += 1
                    found_type = True
                    break

            if not found_type:
                type_counts['autre'] += 1

        return {k: v for k, v in type_counts.items() if v > 0}

    def close(self):
        """Ferme la connexion à la base de données"""
        self.property_repo.close()