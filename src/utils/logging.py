# Configuration Logging (OWASP)
import logging
import sys
from pathlib import Path

def setup_logging(log_level: str = "INFO"):
    """Configure le logging pour le projet"""

    # Création du dossier logs s'il n'existe pas
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configuration du format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Logger root
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_dir / "observatoire.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Logger pour les scrapers
scraper_logger = logging.getLogger("scrapers")

# Logger pour l'API
api_logger = logging.getLogger("api")

# Logger pour la base de données
db_logger = logging.getLogger("database")