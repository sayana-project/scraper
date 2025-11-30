# Scraper Manager (C1) - Coordination multi-sources
from typing import List, Dict, Optional
import logging
import json
import time
from pathlib import Path
from .seloger_scraper import SeLogerScraper
from .leboncoin_scraper import LeBonCoinScraper
from .csv_importer import CSVImporter
from .api_insee import INSEImporter

logger = logging.getLogger(__name__)

class ScraperManager:
    def __init__(self):
        self.seloger_scraper = SeLogerScraper()
        self.leboncoin_scraper = LeBonCoinScraper()
        self.csv_importer = CSVImporter()
        self.insee_importer = INSEImporter()

    def scrape_all_sources(self, max_pages: int = 1) -> Dict[str, List[Dict]]:
        """Scrape toutes les sources configurées"""
        results = {
            'seloger': [],
            'leboncoin': [],
            'csv_import': [],
            'insee_api': []
        }

        logger.info("Demarrage scraping multi-sources (C1)")

        # 1. Scraping SeLoger
        try:
            logger.info("Scraping SeLoger...")
            seloger_properties = self.seloger_scraper.run_scraper(max_pages=max_pages)
            results['seloger'] = seloger_properties
            logger.info(f"OK SeLoger: {len(seloger_properties)} proprietes")
        except Exception as e:
            logger.error(f"Erreur SeLoger: {e}")

        # 2. Scraping LeBonCoin
        try:
            logger.info("Scraping LeBonCoin...")
            leboncoin_properties = self.leboncoin_scraper.run_scraper(max_pages=max_pages)
            results['leboncoin'] = leboncoin_properties
            logger.info(f"OK LeBonCoin: {len(leboncoin_properties)} proprietes")
        except Exception as e:
            logger.error(f"Erreur LeBonCoin: {e}")

        # 3. Import CSV (si fichiers existants)
        try:
            logger.info("Import CSV...")
            csv_properties = self._import_csv_files()
            results['csv_import'] = csv_properties
            logger.info(f"OK CSV: {len(csv_properties)} proprietes")
        except Exception as e:
            logger.error(f"Erreur import CSV: {e}")

        # 4. Import API INSEE (démographie)
        try:
            logger.info("Import API INSEE...")
            insee_data = self.insee_importer.run_api_importer()
            results['insee_api'] = insee_data
            logger.info(f"OK INSEE: {len(insee_data)} enregistrements")
        except Exception as e:
            logger.error(f"Erreur API INSEE: {e}")

        # 5. Statistiques finales
        total_properties = sum(len(properties) for properties in results.values())
        logger.info(f"Total: {total_properties} enregistrements")

        return results

    def _import_csv_files(self) -> List[Dict]:
        """Import tous les fichiers CSV du dossier data/raw/"""
        raw_dir = Path("data/raw")
        all_properties = []

        if not raw_dir.exists():
            logger.info("Dossier data/raw/ inexistant")
            # Création et fichiers d'exemple
            self._create_sample_files()

        # Recherche des fichiers CSV/JSON
        for file_path in raw_dir.glob("*"):
            if file_path.suffix.lower() in ['.csv', '.json']:
                logger.info(f"Import fichier: {file_path.name}")
                file_properties = self.csv_importer.import_file(str(file_path))
                all_properties.extend(file_properties)

        return all_properties

    def _create_sample_files(self):
        """Crée des fichiers d'exemple pour tester"""
        logger.info("Création fichiers d'exemple...")
        self.csv_importer.create_sample_files("data/raw")

    def save_results(self, results: Dict[str, List[Dict]], output_file: str = "data/raw/scraped_properties.json"):
        """Sauvegarde les résultats dans un fichier JSON"""
        try:
            # Fusion de toutes les propriétés
            all_properties = []
            for source, properties in results.items():
                for prop in properties:
                    prop['scraping_session'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    all_properties.append(prop)

            # Sauvegarde
            output_path = Path(output_file)
            output_path.parent.mkdir(exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(all_properties, f, ensure_ascii=False, indent=2)

            logger.info(f"💾 Sauvegardé {len(all_properties)} propriétés dans {output_file}")

            # Création d'un fichier CSV pour analyse
            csv_file = output_path.with_suffix('.csv')
            self._save_as_csv(all_properties, csv_file)

            return all_properties

        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")
            return []

    def _save_as_csv(self, properties: List[Dict], csv_file: Path):
        """Sauvegarde en CSV pour analyse"""
        if not properties:
            return

        import csv

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if properties:
                fieldnames = ['title', 'price', 'surface', 'postal_code', 'city', 'source', 'scraped_at']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(properties)

        logger.info(f"📊 CSV sauvegardé: {csv_file}")

    def get_statistics(self, results: Dict[str, List[Dict]]) -> Dict:
        """Génère des statistiques sur les résultats"""
        stats = {}

        for source, properties in results.items():
            if properties:
                # Statistiques de base
                prices = [prop['price'] for prop in properties if prop.get('price')]
                surfaces = [prop['surface'] for prop in properties if prop.get('surface')]

                stats[source] = {
                    'count': len(properties),
                    'avg_price': sum(prices) / len(prices) if prices else 0,
                    'min_price': min(prices) if prices else 0,
                    'max_price': max(prices) if prices else 0,
                    'avg_surface': sum(surfaces) / len(surfaces) if surfaces else 0,
                    'cities': list(set(prop.get('city', 'Inconnue') for prop in properties))
                }

        # Statistiques globales
        total_properties = sum(len(properties) for properties in results.values())
        stats['total'] = {
            'properties': total_properties,
            'sources': len([s for s, p in results.items() if p])
        }

        return stats

    def run_full_collection(self, max_pages: int = 1) -> Dict:
        """Lance la collection complète et sauvegarde"""
        logger.info("🚀 Lancement collection C1 complète")

        # 1. Scraping multi-sources
        results = self.scrape_all_sources(max_pages)

        # 2. Sauvegarde
        all_properties = self.save_results(results)

        # 3. Statistiques
        stats = self.get_statistics(results)

        logger.info("📊 Statistiques de la collection:")
        for source, data in stats.items():
            if isinstance(data, dict):
                logger.info(f"- {source}: {data['count']} propriétés")

        return {
            'results': results,
            'all_properties': all_properties,
            'statistics': stats
        }

# Test du manager
if __name__ == "__main__":
    manager = ScraperManager()

    print("Lancement Test Scraper Manager (C1)")
    print("=" * 50)

    # Collection complète avec 1 page maximum pour test
    collection_result = manager.run_full_collection(max_pages=1)

    print(f"\nResultats:")
    print(f"- Proprietes totales: {len(collection_result['all_properties'])}")
    print(f"- Sources utilisees: {collection_result['statistics']['total']['sources']}")

    print(f"\nDetail par source:")
    for source, properties in collection_result['results'].items():
        print(f"- {source}: {len(properties)} proprietes")

    print(f"\nFichier sauvegarde: data/raw/scraped_properties.json")