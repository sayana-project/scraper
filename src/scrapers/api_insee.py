# API INSEE Importer (C1) - Import depuis API externe
import requests
from typing import List, Dict, Optional
import logging
import time
import json
from src.utils.config import settings

logger = logging.getLogger(__name__)

class INSEImporter:
    def __init__(self):
        self.base_url = "https://api.insee.fr"
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_commune_data(self, postal_code: str) -> Optional[Dict]:
        """Récupère les données d'une commune depuis l'API INSEE"""
        try:
            # API INSEE - données démographiques (exemple)
            url = f"{self.base_url}/metadonnees/communes/{postal_code[:5]}"

            logger.info(f"Appel API INSEE pour: {postal_code[:5]}")

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            return self._format_commune_data(data, postal_code)

        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur API INSEE commune {postal_code}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Erreur décodage JSON INSEE: {e}")
            return None
        except Exception as e:
            logger.error(f"Erreur inattendue INSEE: {e}")
            return None

    def get_population_data(self, postal_code: str) -> Optional[Dict]:
        """Récupère les données de population"""
        try:
            # API INSEE - population (endpoint fictif pour démo)
            url = f"{self.base_url}/demographie/populations/{postal_code[:5]}"

            logger.info(f"Appel API INSEE population pour: {postal_code[:5]}")

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            return self._format_population_data(data, postal_code)

        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur API INSEE population {postal_code}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erreur population INSEE: {e}")
            return None

    def _format_commune_data(self, data: Dict, postal_code: str) -> Dict:
        """Formate les données de commune"""
        try:
            return {
                'title': f"Données démographiques - {data.get('nom', 'Commune inconnue')}",
                'price': 0,  # Pas de prix pour données INSEE
                'surface': 0,  # Pas de surface
                'postal_code': postal_code[:5],
                'city': data.get('nom', 'Ville inconnue'),
                'population': data.get('population', 0),
                'source': 'insee_api',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'api_response': data
            }
        except Exception as e:
            logger.error(f"Erreur formatage commune: {e}")
            return None

    def _format_population_data(self, data: Dict, postal_code: str) -> Dict:
        """Formate les données de population"""
        try:
            return {
                'title': f"Population {data.get('nomCommune', 'Commune inconnue')}",
                'price': 0,  # Pas de prix
                'surface': 0,  # Pas de surface
                'postal_code': postal_code[:5],
                'city': data.get('nomCommune', 'Ville inconnue'),
                'population': data.get('population', 0),
                'source': 'insee_population',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'api_response': data
            }
        except Exception as e:
            logger.error(f"Erreur formatage population: {e}")
            return None

    def get_test_data(self) -> List[Dict]:
        """Données de test pour développement"""
        return [
            {
                'title': 'Données démographiques Paris',
                'price': 0,
                'surface': 0,
                'postal_code': '75056',
                'city': 'Paris',
                'population': 2200000,
                'source': 'insee_test',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'title': 'Données démographiques Lyon',
                'price': 0,
                'surface': 0,
                'postal_code': '69123',
                'city': 'Lyon',
                'population': 513000,
                'source': 'insee_test',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'title': 'Données démographiques Marseille',
                'price': 0,
                'surface': 0,
                'postal_code': '13201',
                'city': 'Marseille',
                'population': 861000,
                'source': 'insee_test',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        ]

    def fetch_communes(self, postal_codes: List[str]) -> List[Dict]:
        """Récupère les données pour plusieurs communes"""
        all_data = []

        for postal_code in postal_codes:
            # Rate limiting - respect de l'API
            time.sleep(0.5)

            commune_data = self.get_commune_data(postal_code)
            if commune_data:
                all_data.append(commune_data)

        logger.info(f"Récupérées {len(all_data)} communes sur {len(postal_codes)} demandées")
        return all_data

    def test_api_connection(self) -> bool:
        """Test la connexion à l'API INSEE"""
        try:
            # Test simple avec une requête basique
            test_url = f"{self.base_url}/health"
            response = self.session.get(test_url, timeout=5)

            if response.status_code == 200:
                logger.info(" Connexion API INSEE réussie")
                return True
            else:
                logger.error(f" Erreur API INSEE: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f" Erreur connexion API INSEE: {e}")
            return False

    def run_api_importer(self, postal_codes: List[str] = None) -> List[Dict]:
        """Lance l'import depuis API INSEE"""
        if not postal_codes:
            # Codes postaux par défaut pour le test
            postal_codes = ['75001', '69001', '44001', '31000', '06000']

        # Test de connexion
        if not self.test_api_connection():
            logger.warning("Utilisation des données de test - API INSEE inaccessible")
            return self.get_test_data()

        logger.info(f"Import INSEE pour {len(postal_codes)} codes postaux")
        return self.fetch_communes(postal_codes)

# Test de l'API INSEE
if __name__ == "__main__":
    importer = INSEImporter()

    print(" Test API INSEE")
    connection_ok = importer.test_api_connection()
    print(f"Connexion API: {' OK' if connection_ok else ' Échec'}")

    print(f"\n📥 Import INSEE")
    if connection_ok:
        # Test avec quelques codes postaux
        test_codes = ['75001', '69001', '44001']
        data = importer.run_api_importer(test_codes)
    else:
        # Données de test
        data = importer.get_test_data()

    print(f" {len(data)} enregistrements INSEE importés")
    for item in data[:3]:  # Limiter l'affichage
        print(f"- {item['title']}: {item['population']} habitants ({item['city']})")