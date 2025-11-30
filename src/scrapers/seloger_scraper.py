# SeLoger Scraper (C1)
from bs4 import BeautifulSoup
from typing import List, Dict
from src.scrapers.base_scraper import BaseScraper

class SeLogerScraper(BaseScraper):
    def __init__(self):
        super().__init__(delay=2.0)
        self.base_url = "https://www.seloger.com"

    def extract_property_data(self, soup: BeautifulSoup) -> List[Dict]:
        """Extrait les données des propriétés depuis SeLoger"""
        properties = []

        # Exemple de sélecteurs - à adapter avec la structure réelle du site
        listings = soup.find_all('div', class_='Card__CardWrapper-sc-1g825k8-0')

        for listing in listings:
            try:
                title = self._extract_text(listing, 'h2')
                price = self._extract_price(listing)
                surface = self._extract_surface(listing)
                location = self._extract_location(listing)

                if all([title, price, surface, location]):
                    properties.append({
                        'title': title,
                        'price': price,
                        'surface': surface,
                        'postal_code': self._extract_postal_code(location),
                        'city': self._extract_city(location)
                    })
            except Exception as e:
                print(f"Error extracting property: {e}")
                continue

        return properties

    def _extract_text(self, element, tag: str) -> str:
        """Extrait le texte d'un élément"""
        try:
            return element.find(tag).get_text(strip=True) if element.find(tag) else ""
        except:
            return ""

    def _extract_price(self, element) -> int:
        """Extrait et nettoie le prix"""
        price_text = self._extract_text(element, 'span')
        # Nettoyage du prix à implémenter
        return int(price_text.replace('€', '').replace(' ', '').strip())

    def _extract_surface(self, element) -> int:
        """Extrait et nettoie la surface"""
        surface_text = self._extract_text(element, 'div')
        # Nettoyage de la surface à implémenter
        return int(surface_text.replace('m²', '').replace(' ', '').strip())

    def _extract_location(self, element) -> str:
        """Extrait la localisation"""
        return self._extract_text(element, 'p')

    def _extract_postal_code(self, location: str) -> str:
        """Extrait le code postal"""
        # Implémentation à adapter
        return "75001"  # Exemple

    def _extract_city(self, location: str) -> str:
        """Extrait la ville"""
        # Implémentation à adapter
        return "Paris"  # Exemple