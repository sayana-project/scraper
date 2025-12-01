# FastAPI Application (C5)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importer le routeur agrégé (C5)
from src.api.routes import api_router

app = FastAPI(
    title="Observatoire Immobilier API",
    description="API REST pour l'observatoire immobilier public",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Intégration des routes modulaires (C5)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)