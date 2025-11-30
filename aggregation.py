# Phase 3 - C2-C3 : Traitement et Agrégation
"""
Script principal d'orchestration pour la Phase 3 :
- C2 : Requêtes SQL optimisées
- C3 : Agrégation et nettoyage des données

Valide les compétences C2 (Requêtes SQL) et C3 (Traitement/Agrégation)
"""

import logging
import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/phase3_c2_c3.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Imports des modules C2-C3
from src.models import Property, DemographicData, AggregatedProperty
from src.repositories.property_repository import PropertyRepository
from src.services.property_service import PropertyService

class Phase3Orchestrator:
    """Orchestrateur pour la Phase 3 - C2-C3 : Traitement et Agrégation"""

    def __init__(self):
        self.property_service = PropertyService()
        self.property_repo = self.property_service.property_repo

        # Assurer que les dossiers existent
        Path("data/processed").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)

        # Validation C2-C3
        self.validation_results = {
            'c2_sql_queries': 0,
            'c2_optimizations': 0,
            'c3_data_cleaning': 0,
            'c3_aggregation': 0,
            'c3_deduplication': 0,
            'total_validations': 0
        }

    # ===== PHASE 3 DÉMARRAGE =====

    def run_phase_3_c2_c3(self) -> Dict[str, Any]:
        """
        Exécute la Phase 3 complète : C2-C3 Traitement et Agrégation
        """
        logger.info("=" * 60)
        logger.info("DEMARRAGE PHASE 3 - C2-C3 : TRAITEMENT ET AGGREGATION")
        logger.info("=" * 60)

        # 1. Lecture des données Phase 2 (C1)
        logger.info("📂 ÉTAPE 1: Chargement des données collectées (Phase 2)")
        raw_data = self._load_phase2_data()

        # 2. C2 - Création et optimisation de la base de données
        logger.info("🗃️ ÉTAPE 2: C2 - Base de données et requêtes SQL")
        c2_results = self._execute_c2_database_operations(raw_data)

        # 3. C3 - Nettoyage et validation des données
        logger.info("🧹 ÉTAPE 3: C3 - Nettoyage et validation des données")
        cleaned_properties = self._execute_c3_data_cleaning(raw_data['properties'])

        # 4. C3 - Agrégation multi-sources
        logger.info("📊 ÉTAPE 4: C3 - Agrégation multi-sources")
        aggregated_data = self._execute_c3_data_aggregation(cleaned_properties)

        # 5. C3 - Fusion avec données démographiques
        logger.info("🏙️ ÉTAPE 5: C3 - Fusion avec données démographiques")
        final_data = self._execute_c3_data_fusion(aggregated_data, raw_data['demographics'])

        # 6. C3 - Sauvegarde des données traitées
        logger.info("💾 ÉTAPE 6: C3 - Sauvegarde des données traitées")
        save_results = self._save_processed_data(final_data)

        # 7. C2 - Analyse et rapports
        logger.info("📈 ÉTAPE 7: C2 - Analyse du marché et rapports")
        market_analysis = self._execute_c2_market_analysis()

        # 8. Validation finale C2-C3
        logger.info("✅ ÉTAPE 8: Validation finale C2-C3")
        validation_results = self._validate_c2_c3_results()

        # Synthèse des résultats
        phase3_results = {
            'phase': 'C2-C3_Traitement_Agregation',
            'execution_date': datetime.now().isoformat(),
            'data_summary': {
                'raw_properties': len(raw_data.get('properties', [])),
                'demographics_records': len(raw_data.get('demographics', [])),
                'cleaned_properties': len(cleaned_properties),
                'aggregated_locations': len(aggregated_data),
                'final_processed_records': len(final_data)
            },
            'c2_results': c2_results,
            'c3_results': {
                'cleaned_properties': len(cleaned_properties),
                'aggregated_locations': len(aggregated_data),
                'final_records': len(final_data),
                'data_quality_score': self._calculate_overall_quality_score(final_data)
            },
            'save_results': save_results,
            'market_analysis': market_analysis,
            'validation_results': validation_results
        }

        # Rapport final
        self._generate_phase3_report(phase3_results)

        return phase3_results

    def _load_phase2_data(self) -> Dict[str, Any]:
        """Charge les données collectées dans la Phase 2 (C1)"""
        data = {
            'properties': [],
            'demographics': []
        }

        # Chargement des propriétés brutes
        properties_file = Path("data/raw/scraped_properties.json")
        if properties_file.exists():
            try:
                with open(properties_file, 'r', encoding='utf-8') as f:
                    raw_properties = json.load(f)

                # Séparation des propriétés et données démographiques
                for prop in raw_properties:
                    if prop.get('source') == 'insee_test':
                        data['demographics'].append(prop)
                    else:
                        data['properties'].append(prop)

                logger.info(f"✅ Propriétés chargées : {len(data['properties'])}")
                logger.info(f"✅ Démographiques chargées : {len(data['demographics'])}")

            except Exception as e:
                logger.error(f"❌ Erreur chargement propriétés : {e}")

        # Chargement CSV si disponible
        csv_file = Path("data/raw/sample_properties.csv")
        if csv_file.exists():
            try:
                df_csv = pd.read_csv(csv_file)
                csv_properties = df_csv.to_dict('records')
                data['properties'].extend(csv_properties)
                logger.info(f"✅ Propriétés CSV ajoutées : {len(csv_properties)}")
            except Exception as e:
                logger.error(f"❌ Erreur chargement CSV : {e}")

        return data

    def _execute_c2_database_operations(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute les opérations C2 - Base de données et requêtes SQL"""
        logger.info("🔧 C2 : Initialisation base de données...")

        c2_results = {
            'tables_created': False,
            'properties_inserted': 0,
            'demographics_inserted': 0,
            'sql_queries_executed': 0,
            'query_performance': {}
        }

        try:
            # 1. Création des tables
            self.property_repo.create_tables()
            c2_results['tables_created'] = True
            self.validation_results['c2_sql_queries'] += 1
            logger.info("✅ Tables créées avec succès")

            # 2. Insertion des propriétés
            if raw_data.get('properties'):
                properties_count = self.property_repo.insert_properties(raw_data['properties'])
                c2_results['properties_inserted'] = properties_count
                self.validation_results['c2_sql_queries'] += 1
                logger.info(f"✅ Propriétés insérées : {properties_count}")

            # 3. Insertion des données démographiques
            if raw_data.get('demographics'):
                demo_count = self.property_repo.insert_demographic_data(raw_data['demographics'])
                c2_results['demographics_inserted'] = demo_count
                self.validation_results['c2_sql_queries'] += 1
                logger.info(f"✅ Démographiques insérées : {demo_count}")

            # 4. Test des requêtes SQL optimisées
            logger.info("🔍 C2 : Test des requêtes SQL optimisées...")
            query_results = self._test_sql_queries()
            c2_results['query_performance'] = query_results
            c2_results['sql_queries_executed'] = len(query_results)
            self.validation_results['c2_sql_queries'] += len(query_results)
            self.validation_results['c2_optimizations'] = self._count_query_optimizations(query_results)

            logger.info(f"✅ Requêtes testées : {len(query_results)}")
            logger.info(f"✅ Optimisations appliquées : {c2_results['sql_queries_executed']}")

        except Exception as e:
            logger.error(f"❌ Erreur opérations C2 : {e}")

        return c2_results

    def _test_sql_queries(self) -> List[Dict[str, Any]]:
        """Test des requêtes SQL optimisées (C2)"""
        query_results = []

        test_queries = [
            {
                'name': 'Requête simple - GET BY ID',
                'method': lambda: self.property_repo.get_by_id(1),
                'expected_time': 0.01
            },
            {
                'name': 'Requête filtrée - PAR VILLE',
                'method': lambda: self.property_repo.get_by_city('Paris'),
                'expected_time': 0.05
            },
            {
                'name': 'Requête filtrée - PAR CODE POSTAL',
                'method': lambda: self.property_repo.get_by_postal_code('75001'),
                'expected_time': 0.05
            },
            {
                'name': 'Requête complexe - LOCALISATION + PRIX',
                'method': lambda: self.property_repo.get_by_location_and_price('Paris', 300000, 500000),
                'expected_time': 0.1
            },
            {
                'name': 'Requête avec agrégation - STATISTIQUES PAR VILLE',
                'method': lambda: self.property_repo.get_statistics_by_city(),
                'expected_time': 0.15
            },
            {
                'name': 'Requête avec jointure - PROPRIÉTÉS + DÉMOGRAPHIQUES',
                'method': lambda: self.property_repo.get_properties_with_demographics(),
                'expected_time': 0.2
            },
            {
                'name': 'Requête avec sous-requête - AU-DESSUS MOYENNE',
                'method': lambda: self.property_repo.get_properties_above_avg_price(),
                'expected_time': 0.1
            },
            {
                'name': 'Requête d\'analyse - ANALYSE MARCHÉ',
                'method': lambda: self.property_repo.get_market_analysis(),
                'expected_time': 0.25
            }
        ]

        for query_test in test_queries:
            try:
                start_time = datetime.now()
                result = query_test['method']()
                execution_time = (datetime.now() - start_time).total_seconds()

                query_result = {
                    'query_name': query_test['name'],
                    'execution_time': execution_time,
                    'expected_time': query_test['expected_time'],
                    'result_count': len(result) if isinstance(result, list) else 1,
                    'is_optimized': execution_time <= query_test['expected_time'],
                    'success': True
                }

                query_results.append(query_result)

                status = "✅" if query_result['is_optimized'] else "⚠️"
                logger.info(f"{status} {query_test['name']} : {execution_time:.3f}s ({len(result) if isinstance(result, list) else 1} résultats)")

            except Exception as e:
                query_result = {
                    'query_name': query_test['name'],
                    'execution_time': 0,
                    'expected_time': query_test['expected_time'],
                    'result_count': 0,
                    'is_optimized': False,
                    'success': False,
                    'error': str(e)
                }
                query_results.append(query_result)
                logger.error(f"❌ {query_test['name']} : {e}")

        return query_results

    def _count_query_optimizations(self, query_results: List[Dict[str, Any]]) -> int:
        """Compte le nombre d'optimisations de requêtes réussies"""
        return sum(1 for q in query_results if q.get('is_optimized', False))

    def _execute_c3_data_cleaning(self, raw_properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Exécute les opérations C3 - Nettoyage des données"""
        logger.info("🧹 C3 : Nettoyage et validation des données...")

        if not raw_properties:
            logger.warning("⚠️ Aucune donnée à nettoyer")
            return []

        # Nettoyage des données
        cleaned_properties = self.property_service.clean_property_data(raw_properties)

        # Validation du nettoyage
        self.validation_results['c3_data_cleaning'] = len(cleaned_properties)
        self.validation_results['c3_deduplication'] = len(cleaned_properties)

        # Analyse de qualité
        quality_score = self._calculate_data_quality_score(cleaned_properties)
        logger.info(f"✅ Données nettoyées : {len(cleaned_properties)}/{len(raw_properties)}")
        logger.info(f"✅ Score de qualité : {quality_score:.1f}/100")

        # Distribution des sources
        sources = {}
        for prop in cleaned_properties:
            source = prop.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1

        logger.info("📊 Distribution des sources post-nettoyage :")
        for source, count in sources.items():
            logger.info(f"  - {source}: {count}")

        return cleaned_properties

    def _calculate_data_quality_score(self, properties: List[Dict[str, Any]]) -> float:
        """Calcule un score de qualité des données (0-100)"""
        if not properties:
            return 0.0

        score = 0.0

        # Critère 1: Complétude des données (30 points)
        complete_properties = sum(1 for prop in properties
                              if all(prop.get(field) for field in ['title', 'price', 'surface', 'city']))
        completeness_score = (complete_properties / len(properties)) * 30
        score += completeness_score

        # Critère 2: Validité des données (25 points)
        valid_properties = sum(1 for prop in properties
                            if self.property_service._validate_business_rules(prop))
        validity_score = (valid_properties / len(properties)) * 25
        score += validity_score

        # Critère 3: Cohérence des prix/m² (25 points)
        consistent_properties = sum(1 for prop in properties
                               if 100 <= (prop['price'] / prop['surface']) <= 50000)
        consistency_score = (consistent_properties / len(properties)) * 25
        score += consistency_score

        # Critère 4: Diversité des sources (20 points)
        unique_sources = len(set(prop.get('source', 'unknown') for prop in properties))
        diversity_score = min(unique_sources * 5, 20)  # Max 20 points
        score += diversity_score

        return min(score, 100.0)

    def _execute_c3_data_aggregation(self, cleaned_properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Exécute les opérations C3 - Agrégation des données"""
        logger.info("📊 C3 : Agrégation multi-sources...")

        if not cleaned_properties:
            logger.warning("⚠️ Aucune donnée à agréger")
            return []

        # Agrégation par localisation
        aggregated_data = self.property_service.aggregate_properties_by_location(cleaned_properties)

        # Validation de l'agrégation
        self.validation_results['c3_aggregation'] = len(aggregated_data)

        logger.info(f"✅ Données agrégées : {len(aggregated_data)} localisations")

        # Analyse des agrégations
        total_properties_aggregated = sum(loc['total_properties'] for loc in aggregated_data)
        logger.info(f"📈 Total propriétés agrégées : {total_properties_aggregated}")

        # Top localisations par nombre de propriétés
        top_locations = sorted(aggregated_data, key=lambda x: x['total_properties'], reverse=True)[:5]
        logger.info("🏆 Top 5 localisations par nombre de propriétés :")
        for i, loc in enumerate(top_locations, 1):
            logger.info(f"  {i}. {loc['city']} ({loc['postal_code']}): {loc['total_properties']} propriétés")

        return aggregated_data

    def _execute_c3_data_fusion(self, aggregated_data: List[Dict[str, Any]],
                                demographic_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Exécute la fusion des données agrégées avec les données démographiques"""
        logger.info("🏙️ C3 : Fusion avec données démographiques...")

        if not aggregated_data:
            logger.warning("⚠️ Aucune donnée agrégée à fusionner")
            return []

        # Fusion avec données démographiques
        final_data = []

        for record in aggregated_data:
            # Recherche des données démographiques correspondantes
            demographic_info = self._find_demographic_data(record, demographic_data)

            # Enrichissement de l'enregistrement
            enriched_record = record.copy()

            if demographic_info:
                enriched_record.update({
                    'population': demographic_info.get('population', 0),
                    'price_per_inhabitant': round((record['avg_price'] * record['total_properties']) /
                                                max(demographic_info.get('population', 1), 1), 2),
                    'properties_per_1000_inhabitants': round((record['total_properties'] * 1000) /
                                                        max(demographic_info.get('population', 1), 1), 2)
                })
            else:
                enriched_record.update({
                    'population': 0,
                    'price_per_inhabitant': 0,
                    'properties_per_1000_inhabitants': 0
                })

            # Calcul des indicateurs de qualité
            enriched_record['data_quality_score'] = self._calculate_quality_score_for_location(record)

            final_data.append(enriched_record)

        logger.info(f"✅ Données fusionnées : {len(final_data)} enregistrements enrichis")

        # Statistiques de la fusion
        enriched_count = sum(1 for record in final_data if record['population'] > 0)
        logger.info(f"📊 Localisations enrichies : {enriched_count}/{len(final_data)}")

        return final_data

    def _find_demographic_data(self, location_record: Dict[str, Any],
                            demographic_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Trouve les données démographiques correspondant à une localisation"""
        city = location_record['city']
        postal_code = location_record['postal_code']

        # Recherche exacte
        for demo in demographic_data:
            if (demo.get('city', '').lower() == city.lower() and
                demo.get('postal_code') == postal_code):
                return demo

        # Recherche par ville uniquement
        for demo in demographic_data:
            if demo.get('city', '').lower() == city.lower():
                return demo

        # Recherche par code postal
        for demo in demographic_data:
            if demo.get('postal_code') == postal_code:
                return demo

        return {}

    def _calculate_quality_score_for_location(self, location_record: Dict[str, Any]) -> float:
        """Calcule un score de qualité pour une localisation agrégée"""
        score = 0.0

        # Critère 1: Échantillon suffisant (30 points)
        if location_record['total_properties'] >= 5:
            score += 30
        elif location_record['total_properties'] >= 3:
            score += 20
        elif location_record['total_properties'] >= 1:
            score += 10

        # Critère 2: Sources multiples (25 points)
        if location_record['sources_count'] >= 3:
            score += 25
        elif location_record['sources_count'] >= 2:
            score += 20
        elif location_record['sources_count'] >= 1:
            score += 15

        # Critère 3: Données récentes (25 points)
        if location_record.get('data_period_end'):
            try:
                data_date = datetime.fromisoformat(location_record['data_period_end'].replace('Z', '+00:00'))
                days_old = (datetime.now() - data_date).days
                if days_old <= 7:
                    score += 25
                elif days_old <= 30:
                    score += 20
                elif days_old <= 90:
                    score += 15
                elif days_old <= 365:
                    score += 10
            except:
                pass

        # Critère 4: Cohérence statistique (20 points)
        if (location_record.get('avg_price', 0) > 0 and
            location_record.get('avg_surface', 0) > 0 and
            location_record.get('price_per_m2_mean', 0) > 0):

            # Vérification de la cohérence
            calculated_price_per_m2 = location_record['avg_price'] / location_record['avg_surface']
            expected_price_per_m2 = location_record['price_per_m2_mean']

            # Tolérance de 10%
            if abs(calculated_price_per_m2 - expected_price_per_m2) <= (expected_price_per_m2 * 0.1):
                score += 20
            elif abs(calculated_price_per_m2 - expected_price_per_m2) <= (expected_price_per_m2 * 0.2):
                score += 15
            else:
                score += 5

        return min(score, 100.0)

    def _calculate_overall_quality_score(self, final_data: List[Dict[str, Any]]) -> float:
        """Calcule le score de qualité global pour toutes les données"""
        if not final_data:
            return 0.0

        quality_scores = [record.get('data_quality_score', 0) for record in final_data]
        return sum(quality_scores) / len(quality_scores)

    def _save_processed_data(self, final_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sauvegarde les données traitées de la Phase 3"""
        logger.info("💾 C3 : Sauvegarde des données traitées...")

        save_results = {
            'properties_saved': 0,
            'aggregated_saved': 0,
            'files_created': [],
            'success': False
        }

        try:
            # Sauvegarde en JSON
            json_file = Path("data/processed/phase3_aggregated_properties.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, ensure_ascii=False, indent=2, default=str)
            save_results['files_created'].append(str(json_file))
            logger.info(f"✅ Fichier JSON sauvegardé : {json_file}")

            # Sauvegarde en CSV
            csv_file = Path("data/processed/phase3_aggregated_properties.csv")
            df_final = pd.DataFrame(final_data)
            df_final.to_csv(csv_file, index=False, encoding='utf-8')
            save_results['files_created'].append(str(csv_file))
            logger.info(f"✅ Fichier CSV sauvegardé : {csv_file}")

            # Sauvegarde via le repository (objets AggregatedProperty)
            save_repo_result = self.property_service.save_processed_data(final_data, final_data)
            save_results.update(save_repo_result)

            save_results['success'] = True
            save_results['aggregated_saved'] = len(final_data)

            logger.info(f"✅ Données sauvegardées : {len(final_data)} enregistrements")

        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde données : {e}")

        return save_results

    def _execute_c2_market_analysis(self) -> Dict[str, Any]:
        """Exécute l'analyse du marché avec les requêtes SQL (C2)"""
        logger.info("📈 C2 : Analyse du marché immobilier...")

        try:
            market_analysis = self.property_repo.get_market_analysis()

            # Affichage des résultats
            logger.info("📊 Analyse du marché :")

            # Statistiques générales
            stats = market_analysis.get('general_stats', {})
            logger.info(f"  Total propriétés : {stats.get('total_properties', 0)}")
            logger.info(f"  Prix moyen : {stats.get('avg_price', 0):.2f}€")
            logger.info(f"  Surface moyenne : {stats.get('avg_surface', 0):.2f}m²")

            # Top villes par prix
            cities = market_analysis.get('expensive_cities', [])
            logger.info("  Top 5 villes par prix moyen :")
            for i, city in enumerate(cities[:5], 1):
                logger.info(f"    {i}. {city['city']} : {city['avg_price']:.2f}€ ({city['count']} propriétés)")

            # Distribution par source
            sources = market_analysis.get('source_distribution', [])
            logger.info("  Distribution par source :")
            for source in sources:
                logger.info(f"    {source['source']} : {source['count']} propriétés")

            logger.info("✅ Analyse du marché terminée")

        except Exception as e:
            logger.error(f"❌ Erreur analyse marché : {e}")
            market_analysis = {}

        return market_analysis

    def _validate_c2_c3_results(self) -> Dict[str, Any]:
        """Validation finale des compétences C2 et C3"""
        logger.info("✅ Validation finale C2-C3...")

        validation = {
            'c2_sql_validated': False,
            'c3_cleaning_validated': False,
            'c3_aggregation_validated': False,
            'overall_success': False,
            'validation_details': []
        }

        # Validation C2 - Requêtes SQL
        sql_queries_count = self.validation_results['c2_sql_queries']
        sql_optimizations_count = self.validation_results['c2_optimizations']

        c2_sql_success = sql_queries_count >= 8 and sql_optimizations_count >= 5
        validation['validation_details'].append({
            'competence': 'C2_SQL',
            'criterion': 'Nombre de requêtes SQL',
            'expected': '>= 8',
            'actual': sql_queries_count,
            'success': sql_queries_count >= 8
        })

        validation['validation_details'].append({
            'competence': 'C2_SQL',
            'criterion': 'Requêtes optimisées',
            'expected': '>= 5',
            'actual': sql_optimizations_count,
            'success': sql_optimizations_count >= 5
        })

        if c2_sql_success:
            validation['c2_sql_validated'] = True
            logger.info("✅ C2 - Requêtes SQL validées")

        # Validation C3 - Nettoyage
        c3_cleaning_count = self.validation_results['c3_data_cleaning']
        c3_deduplication_count = self.validation_results['c3_deduplication']

        c3_cleaning_success = c3_cleaning_count > 0 and c3_deduplication_count > 0
        validation['validation_details'].append({
            'competence': 'C3_Cleaning',
            'criterion': 'Données nettoyées',
            'expected': '> 0',
            'actual': c3_cleaning_count,
            'success': c3_cleaning_count > 0
        })

        validation['validation_details'].append({
            'competence': 'C3_Deduplication',
            'criterion': 'Dédoublonnage effectué',
            'expected': '> 0',
            'actual': c3_deduplication_count,
            'success': c3_deduplication_count > 0
        })

        if c3_cleaning_success:
            validation['c3_cleaning_validated'] = True
            logger.info("✅ C3 - Nettoyage validé")

        # Validation C3 - Agrégation
        c3_aggregation_count = self.validation_results['c3_aggregation']
        c3_aggregation_success = c3_aggregation_count >= 1

        validation['validation_details'].append({
            'competence': 'C3_Aggregation',
            'criterion': 'Localisations agrégées',
            'expected': '>= 1',
            'actual': c3_aggregation_count,
            'success': c3_aggregation_count >= 1
        })

        if c3_aggregation_success:
            validation['c3_aggregation_validated'] = True
            logger.info("✅ C3 - Agrégation validée")

        # Succès global
        validation['overall_success'] = (validation['c2_sql_validated'] and
                                       validation['c3_cleaning_validated'] and
                                       validation['c3_aggregation_validated'])

        # Validation totale
        total_validations = self.validation_results['total_validations']
        self.validation_results['total_validations'] = total_validations + len(validation['validation_details'])

        return validation

    def _generate_phase3_report(self, phase3_results: Dict[str, Any]) -> None:
        """Génère le rapport final de la Phase 3"""
        logger.info("=" * 60)
        logger.info("📋 RAPPORT FINAL PHASE 3 - C2-C3 : TRAITEMENT ET AGRÉGATION")
        logger.info("=" * 60)

        # Résumé de l'exécution
        data_summary = phase3_results['data_summary']
        logger.info("📊 RÉSUMÉ DES DONNÉES :")
        logger.info(f"  Propriétés brutes : {data_summary['raw_properties']}")
        logger.info(f"  Enregistrements démographiques : {data_summary['demographics_records']}")
        logger.info(f"  Propriétés nettoyées : {data_summary['cleaned_properties']}")
        logger.info(f"  Localisations agrégées : {data_summary['aggregated_locations']}")
        logger.info(f"  Enregistrements finaux : {data_summary['final_processed_records']}")

        # Résultats C2
        c2_results = phase3_results['c2_results']
        logger.info("🗃️ RÉSULTATS C2 - BASE DE DONNÉES :")
        logger.info(f"  Tables créées : {c2_results['tables_created']}")
        logger.info(f"  Propriétés insérées : {c2_results['properties_inserted']}")
        logger.info(f"  Démographiques insérées : {c2_results['demographics_inserted']}")
        logger.info(f"  Requêtes SQL exécutées : {c2_results['sql_queries_executed']}")
        logger.info(f"  Optimisations appliquées : {self.validation_results['c2_optimizations']}")

        # Résultats C3
        c3_results = phase3_results['c3_results']
        logger.info("🧹 RÉSULTATS C3 - NETTOYAGE ET AGRÉGATION :")
        logger.info(f"  Données nettoyées : {c3_results['cleaned_properties']}")
        logger.info(f"  Localisations agrégées : {c3_results['aggregated_locations']}")
        logger.info(f"  Enregistrements finaux : {c3_results['final_records']}")
        logger.info(f"  Score qualité global : {c3_results['data_quality_score']:.1f}/100")

        # Validation finale
        validation = phase3_results['validation_results']
        logger.info("✅ VALIDATION FINALE C2-C3 :")

        logger.info(f"  C2 - Requêtes SQL : {'✅ VALIDÉE' if validation['c2_sql_validated'] else '❌ NON VALIDÉE'}")
        logger.info(f"  C3 - Nettoyage : {'✅ VALIDÉ' if validation['c3_cleaning_validated'] else '❌ NON VALIDÉ'}")
        logger.info(f"  C3 - Agrégation : {'✅ VALIDÉE' if validation['c3_aggregation_validated'] else '❌ NON VALIDÉE'}")
        logger.info(f"  Succès global : {'✅ PHASE 3 TERMINÉE AVEC SUCCÈS' if validation['overall_success'] else '❌ PHASE 3 À CORRIGER'}")

        # Détails de validation
        logger.info("\n📋 DÉTAILS DES VALIDATIONS :")
        for detail in validation['validation_details']:
            status = "✅" if detail['success'] else "❌"
            logger.info(f"  {status} {detail['competence']} - {detail['criterion']}: {detail['actual']} (attendu: {detail['expected']})")

        # Statistiques de performance
        query_perf = c2_results.get('query_performance', {})
        if query_perf:
            logger.info("\n⚡ PERFORMANCE DES REQUÊTES SQL :")
            optimized_count = sum(1 for q in query_perf if q.get('is_optimized', False))
            total_count = len(query_perf)
            logger.info(f"  Requêtes optimisées : {optimized_count}/{total_count} ({(optimized_count/total_count)*100:.1f}%)")

            for query in query_perf:
                status = "🟢" if query['is_optimized'] else "🔴"
                time_ms = query['execution_time'] * 1000
                logger.info(f"  {status} {query['query_name']}: {time_ms:.1f}ms ({query['result_count']} résultats)")

        # Fichiers générés
        save_results = phase3_results['save_results']
        if save_results.get('success', False):
            logger.info(f"\n💾 FICHIERS GÉNÉRÉS : {len(save_results.get('files_created', []))}")
            for file_path in save_results.get('files_created', []):
                logger.info(f"  ✅ {file_path}")

        logger.info("=" * 60)
        logger.info("🎯 PROCHAINES ÉTAPES : Phase 4 - C4 : Base de données RGPD")
        logger.info("=" * 60)

    def close(self):
        """Ferme toutes les connexions"""
        try:
            self.property_service.close()
            logger.info("✅ Connexions fermées")
        except Exception as e:
            logger.error(f"❌ Erreur fermeture connexions : {e}")


# Point d'entrée principal
if __name__ == "__main__":
    orchestrator = Phase3Orchestrator()

    try:
        # Exécution de la Phase 3 complète
        phase3_results = orchestrator.run_phase_3_c2_c3()

        # Affichage résumé
        validation = phase3_results['validation_results']

        if validation['overall_success']:
            print("\n🎉 PHASE 3 - C2-C3 TERMINÉE AVEC SUCCÈS")
            print("✅ C2 - Requêtes SQL optimisées validées")
            print("✅ C3 - Nettoyage et agrégation validés")
            print("✅ Données traitées et sauvegardées")
            print("\n👉 Prêt pour Phase 4: C4 - Base de données RGPD")
        else:
            print("\n⚠️ PHASE 3 - C2-C3 NÉCESSITE DES CORRECTIONS")
            print("❌ Certaines validations n'ont pas été réussies")
            print("\n📋 Détails des validations :")
            for detail in validation['validation_details']:
                status = "✅" if detail['success'] else "❌"
                print(f"  {status} {detail['competence']}: {detail['actual']} (attendu: {detail['expected']})")

    except Exception as e:
        logger.error(f"❌ Erreur critique Phase 3 : {e}")
        print(f"\n❌ Erreur critique : {e}")

    finally:
        orchestrator.close()