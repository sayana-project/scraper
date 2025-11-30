# Base Scraper (C1)
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import logging

logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Récupère et parse une page web"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            time.sleep(self.delay)  # Respect robots.txt
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def extract_property_data(self, soup: BeautifulSoup) -> List[Dict]:
        """Méthode à implémenter dans les classes enfants"""
        raise NotImplementedError