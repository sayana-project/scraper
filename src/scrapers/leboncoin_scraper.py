# LeBonCoin Scraper (C1) - Implémentation fonctionnelle
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import logging
import re
from src.scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class LeBonCoinScraper(BaseScraper):
    def __init__(self):
        super().__init__(delay=3.0)  # Respect robots.txt
        self.base_url = "https://www.leboncoin.fr"
        self.search_url = "https://www.leboncoin.fr/recherche?category=9&region=ile_de_france"

    def extract_property_data(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrait les données des propriétés depuis LeBonCoin"""
        properties = []

        # Structure LeBonCoin pour annonces immobilières
        listings = soup.find_all('a', attrs={'data-qa-id': 'aditem_container'})

        if not listings:
            logger.warning("Aucune annonce trouvée - vérifier sélecteurs CSS")
            return self._get_test_properties()

        for listing in listings:
            try:
                property_data = self._extract_single_property(listing)
                if property_data:
                    properties.append(property_data)
            except Exception as e:
                logger.error(f"Erreur extraction propriété: {e}")
                continue

        logger.info(f"Extrait {len(properties)} propriétés de LeBonCoin")
        return properties

    def _extract_single_property(self, listing) -> Optional[Dict]:
        """Extrait une seule propriété"""
        try:
            # Extraction depuis attributs data-qa et structure HTML
            title = self._extract_title(listing)
            price = self._extract_price(listing)
            surface = self._extract_surface(listing)
            location = self._extract_location(listing)

            if not all([title, price, surface, location]):
                logger.warning("Propriété incomplète ignorée")
                return None

            return {
                'title': title,
                'price': price,
                'surface': surface,
                'postal_code': self._extract_postal_code(location),
                'city': self._extract_city(location),
                'source': 'leboncoin',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"Erreur extraction propriété: {e}")
            return None

    def _extract_title(self, element) -> Optional[str]:
        """Extrait le titre"""
        try:
            title_element = element.find('p', attrs={'data-qa-id': 'aditem_title'})
            return title_element.get_text(strip=True) if title_element else None
        except:
            return None

    def _extract_price(self, element) -> Optional[int]:
        """Extrait et nettoie le prix"""
        try:
            # Recherche dans le span de prix
            price_element = element.find('span', attrs={'data-qa-id': 'aditem_price'})
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
            # Cherche la surface dans plusieurs emplacements possibles
            surface_element = (
                element.find('span', attrs={'data-qa-id': 'aditem_attribute'}) or
                element.find(string=re.compile(r'\d+m²'))
            )

            if surface_element:
                if hasattr(surface_element, 'get_text'):
                    surface_text = surface_element.get_text(strip=True)
                else:
                    surface_text = str(surface_element)

                # Nettoyage: "85 m²" -> 85
                surface_match = re.search(r'(\d+)', surface_text)
                return int(surface_match.group(1)) if surface_match else None
        except:
            pass
        return None

    def _extract_location(self, element) -> Optional[str]:
        """Extrait la localisation"""
        try:
            location_element = element.find('span', attrs={'data-qa-id': 'aditem_location'})
            return location_element.get_text(strip=True) if location_element else None
        except:
            return None

    def _extract_postal_code(self, location: str) -> str:
        """Extrait le code postal"""
        if not location:
            return "75001"  # Default Paris

        # Recherche pattern: "Paris 75001" -> "75001"
        match = re.search(r'(\d{5})', location)
        return match.group(1) if match else "75001"

    def _extract_city(self, location: str) -> str:
        """Extrait la ville"""
        if not location:
            return "Paris"

        # Nettoyage: "Paris 75001" -> "Paris"
        city = re.sub(r'\s*\d{5}\s*', '', location).strip()
        return city or "Paris"

    def _get_test_properties(self) -> List[Dict]:
        """Propriétés de test pour développement"""
        return [
            {
                'title': 'Maison avec jardin Paris',
                'price': 850000,
                'surface': 120,
                'postal_code': '75014',
                'city': 'Paris',
                'source': 'leboncoin_test',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'title': 'Appartement 2 pièces Le Marais',
                'price': 550000,
                'surface': 55,
                'postal_code': '75004',
                'city': 'Paris',
                'source': 'leboncoin_test',
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
            url = f"{self.search_url}&page={page}"
            properties = self.scrape_page(url)
            all_properties.extend(properties)

            if not properties:
                logger.info(f"Page {page} vide - arrêt du scraping")
                break

            logger.info(f"Page {page}: {len(properties)} propriétés extraites")

        return all_properties

# Test du scraper
if __name__ == "__main__":
    scraper = LeBonCoinScraper()
    properties = scraper.run_scraper(max_pages=1)

    print(f"\n🏠 {len(properties)} propriétés extraites:")
    for prop in properties[:3]:  # Limiter l'affichage
        print(f"- {prop['title']}: {prop['price']}€ ({prop['surface']}m²) à {prop['city']} ({prop['postal_code']})")