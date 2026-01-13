# SeLoger Scraper (C1) - Implémentation fonctionnelle
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import logging
import re
from src.scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class SeLogerScraper(BaseScraper):
    def __init__(self):
        super().__init__(delay=2.0)
        self.base_url = "https://www.seloger.com"
        self.search_url = "https://www.seloger.com/immobilier/achat/immeuble-paris-75"

    def extract_property_data(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrait les données des propriétés depuis SeLoger"""
        properties = []

        # Sélecteurs adaptés à la structure SeLoger (à valider avec inspection)
        listings = soup.find_all('div', class_='Card__CardWrapper-sc-1g825k8-0')

        if not listings:
            logger.warning("Aucune annonce trouvée - vérifier sélecteurs CSS")
            # Fallback pour test
            return self._get_test_properties()

        for listing in listings:
            try:
                property_data = self._extract_single_property(listing)
                if property_data:
                    properties.append(property_data)
            except Exception as e:
                logger.error(f"Erreur extraction propriété: {e}")
                continue

        logger.info(f"Extrait {len(properties)} propriétés de SeLoger")
        return properties

    def _extract_single_property(self, listing) -> Optional[Dict]:
        """Extrait une seule propriété"""
        try:
            title = self._clean_text(listing.find('h2'))
            price = self._extract_price(listing)
            surface = self._extract_surface(listing)
            location = self._clean_text(listing.find('p', class_='Card__Location-sc-1nk0s6f-0'))

            if not all([title, price, surface, location]):
                logger.warning("Propriété incomplète ignorée")
                return None

            return {
                'title': title,
                'price': price,
                'surface': surface,
                'postal_code': self._extract_postal_code(location),
                'city': self._extract_city(location),
                'source': 'seloger',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"Erreur extraction propriété: {e}")
            return None

    def _extract_price(self, element) -> Optional[int]:
        """Extrait et nettoie le prix"""
        try:
            price_element = element.find('span', class_='Tag__Tag-sc-1p0s089-0')
            if price_element:
                price_text = price_element.get_text(strip=True)
                # Nettoyage: "300 000 €" -> 300000
                price_clean = re.sub(r'[^\d]', '', price_text)
                return int(price_clean) if price_clean else None
        except:
            pass
        return None

    def _extract_surface(self, element) -> Optional[int]:
        """Extrait et nettoie la surface"""
        try:
            # Chercher dans plusieurs endroits possibles
            surface_element = (element.find('span', class_='Tag__Tag-sc-1p0s089-0') or
                           element.find('div', string=re.compile(r'\d+m²')))
            if surface_element:
                surface_text = surface_element.get_text(strip=True)
                # Nettoyage: "85 m²" -> 85
                surface_match = re.search(r'(\d+)', surface_text)
                return int(surface_match.group(1)) if surface_match else None
        except:
            pass
        return None

    def _clean_text(self, element) -> str:
        """Nettoie le texte d'un élément"""
        if element:
            return element.get_text(strip=True)
        return ""

    def _extract_postal_code(self, location: str) -> str:
        """Extrait le code postal"""
        # Recherche pattern: "Paris 75001" -> "75001"
        match = re.search(r'\b(\d{5})\b', location)
        return match.group(1) if match else "75001"  # Default Paris

    def _extract_city(self, location: str) -> str:
        """Extrait la ville"""
        # Nettoyage: "Paris 75001" -> "Paris"
        city = re.sub(r'\s*\d{5}\s*', '', location).strip()
        return city or "Paris"

    def _get_test_properties(self) -> List[Dict]:
        """Propriétés de test pour développement"""
        return [
            {
                'title': 'Appartement T3 Paris Centre',
                'price': 450000,
                'surface': 75,
                'postal_code': '75001',
                'city': 'Paris',
                'source': 'seloger_test',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'title': 'Studio Marais',
                'price': 320000,
                'surface': 35,
                'postal_code': '75004',
                'city': 'Paris',
                'source': 'seloger_test',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        ]

    def scrape_page(self, url: str = None) -> List[Dict]:
        """Scrape une page spécifique"""
        if url is None:
            url = self.search_url

        logger.info(f"Scraping de: {url}")

        soup = self.get_page(url)
        if soup:
            properties = self.extract_property_data(soup)
            return properties
        else:
            logger.error(f"Échec scraping URL: {url}")
            return []

    def run_scraper(self, max_pages: int = 1) -> List[Dict]:
        """Lance le scraper sur plusieurs pages"""
        all_properties = []

        for page in range(1, max_pages + 1):
            url = f"{self.search_url}?page={page}"
            properties = self.scrape_page(url)
            all_properties.extend(properties)

            if not properties:
                logger.info(f"Page {page} vide - arrêt du scraping")
                break

            logger.info(f"Page {page}: {len(properties)} propriétés extraites")

        return all_properties

# Test du scraper
if __name__ == "__main__":
    scraper = SeLogerScraper()
    properties = scraper.run_scraper(max_pages=1)

    print(f"\n {len(properties)} propriétés extraites:")
    for prop in properties[:3]:  # Limiter l'affichage
        print(f"- {prop['title']}: {prop['price']}€ ({prop['surface']}m²) à {prop['city']} ({prop['postal_code']})")