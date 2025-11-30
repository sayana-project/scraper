# Point d'entrée principal pour lancement
import uvicorn
from src.api.app import app
from src.utils.logging import api_logger

if __name__ == "__main__":
    api_logger.info("Démarrage de l'API Observatoire Immobilier")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)