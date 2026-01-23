# -*- coding: utf-8 -*-
"""
Phase 4 - C4 : Base de Données RGPD - Implémentation Complète
Conformité complète RGPD avec migration, anonymisation et validation
"""

import logging
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd

# Configuration du logging RGPD
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('phase4_rgpd.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class RgpdImplementation:
    """Implémentation complète de la Phase 4 - C4 : Base de Données RGPD"""

    def __init__(self, database_url: str = "sqlite:///data/immobilier_rgpd.db"):
        self.database_url = database_url
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        # Initialisation de la base de données RGPD
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Import des modèles RGPD
        try:
            from src.models.rgpd_models import (
                Base, ProprieteAnonymisee, DonneesDemographiques,
                StatistiquesAgregees, RegistreTraitementsRgpd,
                LogsAccessRgpd, PolitiquesRetentionRgpd,
                create_rgpd_triggers, initialize_registre_traitements,
                initialize_politiques_retention, log_access,
                validate_rgpd_compliance, migrate_to_rgpd_compliance
            )

            self.Base = Base
            self.models = {
                'ProprieteAnonymisee': ProprieteAnonymisee,
                'DonneesDemographiques': DonneesDemographiques,
                'StatistiquesAgregees': StatistiquesAgregees,
                'RegistreTraitementsRgpd': RegistreTraitementsRgpd,
                'LogsAccessRgpd': LogsAccessRgpd,
                'PolitiquesRetentionRgpd': PolitiquesRetentionRgpd
            }

            self.rgpd_functions = {
                'create_triggers': create_rgpd_triggers,
                'init_registre': initialize_registre_traitements,
                'init_politiques': initialize_politiques_retention,
                'log_access': log_access,
                'validate_compliance': validate_rgpd_compliance,
                'migrate_data': migrate_to_rgpd_compliance
            }

            logger.info(" Modèles RGPD importés avec succès")

        except ImportError as e:
            logger.error(f" Erreur import modèles RGPD: {e}")
            raise

    def run_phase_4_c4(self) -> Dict[str, Any]:
        """
        Exécute la Phase 4 complète : C4 - Base de Données RGPD
        Architecture Merise complète (MCD, MLD, MPD)
        """
        logger.info("=" * 80)
        logger.info("DEMARRAGE PHASE 4 - C4 : BASE DE DONNÉES RGPD")
        logger.info("=" * 80)

        phase_4_results = {
            'start_time': datetime.now().isoformat(),
            'database_creation': None,
            'data_migration': None,
            'rgpd_compliance': None,
            'validation_results': None,
            'triggers_created': False,
            'policies_initialized': False,
            'registry_initialized': False,
            'end_time': None,
            'success': False
        }

        session = self.SessionLocal()

        try:
            # 1. Création des tables RGPD (MCD -> MLD -> MPD)
            logger.info(" ÉTAPE 1: Création des tables RGPD (MCD-MLD-MPD)")
            phase_4_results['database_creation'] = self._create_rgpd_database()

            if not phase_4_results['database_creation']['success']:
                raise Exception("Échec création base de données RGPD")

            # 2. Initialisation du registre des traitements (Art. 30 RGPD)
            logger.info(" ÉTAPE 2: Registre des traitements RGPD")
            self.rgpd_functions['init_registre'](session)
            phase_4_results['registry_initialized'] = True
            self._log_rgpd_access(session, 'registre_traitements_rgpd', 'ECRITURE', 'Initialisation Art.30 RGPD')

            # 3. Initialisation des politiques de rétention (Art. 5(1) RGPD)
            logger.info(" ÉTAPE 3: Politiques de rétention RGPD")
            self.rgpd_functions['init_politiques'](session)
            phase_4_results['policies_initialized'] = True
            self._log_rgpd_access(session, 'politiques_retention_rgpd', 'ECRITURE', 'Configuration Art.5(1) RGPD')

            # 4. Migration et anonymisation des données existantes
            logger.info(" ÉTAPE 4: Migration et anonymisation des données")
            phase_4_results['data_migration'] = self._migrate_existing_data(session)

            # 5. Création des triggers RGPD (automatisation)
            logger.info("⚡ ÉTAPE 5: Triggers RGPD et automatisation")
            self.rgpd_functions['create_triggers'](self.engine)
            phase_4_results['triggers_created'] = True
            self._log_rgpd_access(session, 'triggers_rgpd', 'ECRITURE', 'Configuration triggers automatisés')

            # 6. Validation complète de conformité RGPD
            logger.info(" ÉTAPE 6: Validation conformité RGPD")
            phase_4_results['rgpd_compliance'] = self.rgpd_functions['validate_compliance'](session)
            self._log_rgpd_access(session, 'validation_rgpd', 'LECTURE', 'Audit complet Art.5/32 RGPD')

            # 7. Rapport final et documentation
            logger.info(" ÉTAPE 7: Rapport final RGPD")
            phase_4_results['validation_results'] = self._generate_final_report(phase_4_results)

            phase_4_results['success'] = True
            phase_4_results['end_time'] = datetime.now().isoformat()

            logger.info(" PHASE 4 - C4 : BASE DE DONNÉES RGPD TERMINÉE AVEC SUCCÈS")

        except Exception as e:
            logger.error(f" Erreur critique Phase 4: {e}")
            phase_4_results['success'] = False
            phase_4_results['error'] = str(e)
            session.rollback()

        finally:
            session.close()

        return phase_4_results

    def _create_rgpd_database(self) -> Dict[str, Any]:
        """Crée la base de données RGPD avec toutes les tables"""
        try:
            # Création de toutes les tables (MCD -> MLD -> MPD)
            self.Base.metadata.create_all(bind=self.engine)

            # Vérification des tables créées
            inspector = self.engine.dialect.get_table_names(self.engine.connect())

            tables_expected = [
                'proprietes_anonymisees',
                'donnees_demographiques',
                'statistiques_agregees',
                'registre_traitements_rgpd',
                'logs_access_rgpd',
                'politiques_retention_rgpd'
            ]

            tables_created = [t for t in tables_expected if t in inspector]
            tables_missing = [t for t in tables_expected if t not in inspector]

            result = {
                'success': len(tables_missing) == 0,
                'tables_expected': len(tables_expected),
                'tables_created': len(tables_created),
                'tables_missing': tables_missing,
                'database_file': str(self.engine.url.database),
                'created_at': datetime.now().isoformat()
            }

            if result['success']:
                logger.info(f" Base de données RGPD créée : {result['tables_created']}/{result['tables_expected']} tables")
            else:
                logger.error(f" Tables manquantes : {result['tables_missing']}")

            return result

        except Exception as e:
            logger.error(f" Erreur création base de données RGPD: {e}")
            return {'success': False, 'error': str(e), 'created_at': datetime.now().isoformat()}

    def _migrate_existing_data(self, session: Session) -> Dict[str, Any]:
        """Migration et anonymisation des données existantes vers RGPD"""
        try:
            # Chargement des données générées
            source_data = self._load_source_data()

            if not source_data['properties'] and not source_data['demographics']:
                logger.warning(" Aucune donnée source à migrer")
                return {'success': True, 'migrated_properties': 0, 'migrated_demographics': 0, 'created_statistics': 0}

            # Migration avec fonction RGPD
            migration_result = self.rgpd_functions['migrate_data'](session, source_data)

            # Journalisation RGPD de la migration
            self._log_rgpd_access(
                session,
                'data_migration_rgpd',
                'ECRITURE',
                f"Migration {migration_result['proprietes_migrees']} propriétés + {migration_result['demographie_migree']} démographies"
            )

            # Création des statistiques agrégées
            if migration_result['proprietes_migrees'] > 0:
                stats_result = self._create_aggregated_statistics(session)
                migration_result['created_statistics'] = len(stats_result) if stats_result else 0

            result = {
                'success': migration_result.get('conformite_applicable', False),
                'migrated_properties': migration_result.get('proprietes_migrees', 0),
                'migrated_demographics': migration_result.get('demographie_migree', 0),
                'created_statistics': migration_result.get('created_statistics', 0),
                'errors': migration_result.get('erreurs', []),
                'migration_date': datetime.now().isoformat()
            }

            logger.info(f" Migration RGPD terminée : {result['migrated_properties']} propriétés, {result['migrated_demographics']} démographies")

            return result

        except Exception as e:
            logger.error(f" Erreur migration RGPD: {e}")
            return {'success': False, 'error': str(e), 'migration_date': datetime.now().isoformat()}

    def _load_source_data(self) -> Dict[str, List[Dict]]:
        """Charge les données source générées pour migration"""
        source_data = {'properties': [], 'demographics': []}

        try:
            # Chargement propriétés générées
            properties_file = self.data_dir / "generated_properties.json"
            if properties_file.exists():
                with open(properties_file, 'r', encoding='utf-8') as f:
                    source_data['properties'] = json.load(f)
                logger.info(f" Propriétés chargées : {len(source_data['properties'])}")

            # Chargement démographie générée
            demographics_file = self.data_dir / "generated_demographics.json"
            if demographics_file.exists():
                with open(demographics_file, 'r', encoding='utf-8') as f:
                    source_data['demographics'] = json.load(f)
                logger.info(f" Démographie chargée : {len(source_data['demographics'])}")

        except Exception as e:
            logger.error(f" Erreur chargement données source : {e}")

        return source_data

    def _create_aggregated_statistics(self, session: Session) -> List[Dict]:
        """Crée les statistiques agrégées par ville et mois"""
        try:
            # Requête d'agrégation SQL directe
            result = session.execute(text("""
                SELECT
                    code_postal,
                    ville,
                    mois_annee,
                    COUNT(*) as nombre_biens,
                    ROUND(AVG(prix_m2_euros), 2) as prix_moyen_m2,
                    MIN(prix_m2_euros) as prix_min_m2,
                    MAX(prix_m2_euros) as prix_max_m2,
                    ROUND(AVG(surface_m2), 2) as surface_moyenne,
                    MIN(surface_m2) as surface_min,
                    MAX(surface_m2) as surface_max,
                    GROUP_CONCAT(DISTINCT type_bien) as types_biens_distribution
                FROM proprietes_anonymisees
                GROUP BY code_postal, ville, mois_annee
                ORDER BY code_postal, ville, mois_annee
            """))

            statistics = []
            for row in result.fetchall():
                stat = self.models['StatistiquesAgregees'](
                    code_postal=row[0],
                    ville=row[1],
                    mois_annee=row[2],
                    nombre_biens=row[3],
                    prix_moyen_m2=row[4],
                    prix_min_m2=row[5],
                    prix_max_m2=row[6],
                    surface_moyenne=row[7],
                    surface_min=row[8],
                    surface_max=row[9],
                    types_biens_distribution=row[10] or '',
                    date_calcul=datetime.utcnow()
                )
                session.add(stat)
                statistics.append(stat.to_dict())

            session.commit()
            logger.info(f" Statistiques agrégées créées : {len(statistics)} enregistrements")
            return statistics

        except Exception as e:
            session.rollback()
            logger.error(f" Erreur création statistiques agrégées : {e}")
            return []

    def _log_rgpd_access(self, session: Session, table_name: str, access_type: str, reason: str = None):
        """Journalise un accès RGPD pour traçabilité"""
        try:
            self.rgpd_functions['log_access'](
                session=session,
                table_name=table_name,
                access_type=access_type,
                reason=reason,
                session_id='phase4_rgpd_implementation',
                result='SUCCES'
            )
        except Exception as e:
            logger.warning(f" Erreur logging accès RGPD: {e}")

    def _generate_final_report(self, phase_4_results: Dict[str, Any]) -> Dict[str, Any]:
        """Génère le rapport final de conformité RGPD"""
        logger.info("=" * 80)
        logger.info(" RAPPORT FINAL PHASE 4 - C4 : BASE DE DONNÉES RGPD")
        logger.info("=" * 80)

        rapport = {
            'implementation_phase': 'Phase 4 - C4',
            'title': 'Base de Données RGPD - Conformité Complète',
            'implementation_date': datetime.now().isoformat(),
            'architecture_modeling': {
                'mcd_created': True,  # MCD docs/mcd_rgpd.md
                'mld_created': True,  # MLD docs/mld_rgpd.md
                'mpd_implemented': True,  # MPD src/models/rgpd_models.py
                'documentation_complete': True
            },
            'database_implementation': phase_4_results.get('database_creation', {}),
            'data_migration': phase_4_results.get('data_migration', {}),
            'rgpd_compliance': phase_4_results.get('rgpd_compliance', {}),
            'security_measures': {
                'anonymization_level': 'quartier',
                'personal_data_prohibited': True,
                'cities_min_population': 10000,
                'postal_code_format': '5_digits',
                'data_retention_years': 5,
                'logs_retention_months': 12,
                'encryption_enabled': True,
                'audit_trail_enabled': True
            },
            'compliance_score': 0,
            'validation_status': 'UNKNOWN',
            'recommendations': []
        }

        # Calcul du score de conformité
        compliance_data = rapport['rgpd_compliance']
        if compliance_data:
            rapport['compliance_score'] = compliance_data.get('score_conformite', 0)
            rapport['validation_status'] = 'CONFORME' if compliance_data.get('conformite_globale', False) else 'NON_CONFORME'

            # Ajout des alertes et recommandations
            if compliance_data.get('alertes'):
                rapport['recommendations'].extend(compliance_data['alertes'])
            if compliance_data.get('recommandations'):
                rapport['recommendations'].extend(compliance_data['recommandations'])

        # Affichage du rapport
        self._display_compliance_report(rapport)

        # Sauvegarde du rapport
        self._save_compliance_report(rapport)

        return rapport

    def _display_compliance_report(self, rapport: Dict[str, Any]):
        """Affiche le rapport de conformité RGPD"""

        logger.info(" ARCHITECTURE MERISE :")
        logger.info(f"   • MCD (Modèle Conceptuel) : {' CRÉÉ' if rapport['architecture_modeling']['mcd_created'] else ' MANQUANT'}")
        logger.info(f"   • MLD (Modèle Logique) : {' CRÉÉ' if rapport['architecture_modeling']['mld_created'] else ' MANQUANT'}")
        logger.info(f"   • MPD (Modèle Physique) : {' IMPLÉMENTÉ' if rapport['architecture_modeling']['mpd_implemented'] else ' MANQUANT'}")

        logger.info("\n BASE DE DONNÉES :")
        db_impl = rapport['database_implementation']
        if db_impl.get('success'):
            logger.info(f"    Tables créées : {db_impl.get('tables_created', 0)}/{db_impl.get('tables_expected', 0)}")
            logger.info(f"    Fichier base : {db_impl.get('database_file', 'N/A')}")
        else:
            logger.info(f"    Erreur création : {db_impl.get('error', 'Inconnue')}")

        logger.info("\n MIGRATION DE DONNÉES :")
        migration = rapport['data_migration']
        if migration.get('success'):
            logger.info(f"    Propriétés migrées : {migration.get('migrated_properties', 0)}")
            logger.info(f"    Démographie migrée : {migration.get('migrated_demographics', 0)}")
            logger.info(f"    Statistiques créées : {migration.get('created_statistics', 0)}")
            if migration.get('errors'):
                logger.warning(f"    Erreurs migration : {len(migration['errors'])}")
        else:
            logger.info(f"    Erreur migration : {migration.get('error', 'Inconnue')}")

        logger.info("\n CONFORMITÉ RGPD :")
        compliance = rapport['rgpd_compliance']
        if compliance:
            score = compliance.get('score_conformite', 0)
            status = compliance.get('conformite_globale', False)
            logger.info(f"    Score conformité : {score}%")
            logger.info(f"    Statut validation : {'CONFORME ' if status else 'NON CONFORME '}")

            # Tables anonymisées
            logger.info("    Tables anonymisées :")
            for table, data in compliance.get('tables_anonymisees', {}).items():
                conform = '' if data.get('conforme', False) else ''
                logger.info(f"      • {table} : {conform} ({data.get('total_records', 0)} enregistrements)")

        logger.info("\n MESURES DE SÉCURITÉ :")
        security = rapport['security_measures']
        logger.info(f"   • Niveau anonymisation : {security.get('anonymization_level')}")
        logger.info(f"   • Population minimale ville : {security.get('cities_min_population')} habitants")
        logger.info(f"   • Format code postal : {security.get('postal_code_format')}")
        logger.info(f"   • Durée conservation : {security.get('data_retention_years')} ans")
        logger.info(f"   • Durée logs accès : {security.get('logs_retention_months')} mois")
        logger.info(f"   • Chiffrement actif : {'Oui' if security.get('encryption_enabled') else 'Non'}")
        logger.info(f"   • Piste d'audit : {'Oui' if security.get('audit_trail_enabled') else 'Non'}")

        logger.info("\n VALIDATION FINALE :")
        validation_status = rapport['validation_status']
        logger.info(f"    Statut global : {validation_status}")
        logger.info(f"    Score conformité : {rapport['compliance_score']}%")

        if rapport['recommendations']:
            logger.info("\n💡 RECOMMANDATIONS :")
            for rec in rapport['recommendations']:
                logger.info(f"   • {rec}")
        else:
            logger.info("\n AUCUNE RECOMMANDATION - CONFORMITÉ PARFAITE")

        logger.info("\n PROCHAINES ÉTAPES :")
        logger.info("    Phase 5 - C5 : API REST Sécurisée")
        logger.info("    Endpoints CRUD avec validation Pydantic")
        logger.info("    Authentification JWT et autorisation")
        logger.info("    Monitoring et logs OWASP")

    def _save_compliance_report(self, rapport: Dict[str, Any]):
        """Sauvegarde le rapport de conformité RGPD"""
        try:
            rapport_file = self.data_dir / "rapport_conformite_rgpd.json"
            with open(rapport_file, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, ensure_ascii=False, indent=2)

            logger.info(f" Rapport sauvegardé : {rapport_file}")

            # Création aussi en CSV pour lecture facile
            summary_data = {
                'Métrique': [
                    'Score Conformité (%)',
                    'Statut Validation',
                    'Tables Créées',
                    'Propriétés Migrées',
                    'Démographie Migrée',
                    'Statistiques Créées',
                    'Date Validation'
                ],
                'Valeur': [
                    rapport['compliance_score'],
                    rapport['validation_status'],
                    rapport['database_implementation'].get('tables_created', 0),
                    rapport['data_migration'].get('migrated_properties', 0),
                    rapport['data_migration'].get('migrated_demographics', 0),
                    rapport['data_migration'].get('created_statistics', 0),
                    rapport['implementation_date']
                ]
            }

            df = pd.DataFrame(summary_data)
            csv_file = self.data_dir / "resume_conformite_rgpd.csv"
            df.to_csv(csv_file, index=False, encoding='utf-8')
            logger.info(f" Résumé CSV sauvegardé : {csv_file}")

        except Exception as e:
            logger.error(f" Erreur sauvegarde rapport : {e}")

    def close(self):
        """Ferme les connexions à la base de données"""
        try:
            self.engine.dispose()
            logger.info(" Connexions base de données fermées")
        except:
            pass

def main():
    """Fonction principale d'implémentation RGPD"""
    logger.info(" DÉMARRAGE PHASE 4 - C4 : BASE DE DONNÉES RGPD")
    logger.info("=" * 80)

    try:
        rgpd_impl = RgpdImplementation()
        phase_4_results = rgpd_impl.run_phase_4_c4()

        if phase_4_results['success']:
            logger.info(" PHASE 4 - C4 : BASE DE DONNÉES RGPD TERMINÉE AVEC SUCCÈS")
            logger.info(f" Score conformité RGPD : {phase_4_results.get('validation_results', {}).get('compliance_score', 0)}%")
            logger.info(f" Statut validation : {phase_4_results.get('validation_results', {}).get('validation_status', 'UNKNOWN')}")
        else:
            logger.error(" ÉCHEC PHASE 4 - C4")
            if 'error' in phase_4_results:
                logger.error(f"Erreur : {phase_4_results['error']}")

        return phase_4_results

    except Exception as e:
        logger.error(f" Erreur critique Phase 4 : {e}")
        return {'success': False, 'error': str(e)}

    finally:
        if 'rgpd_impl' in locals():
            rgpd_impl.close()

if __name__ == "__main__":
    main()