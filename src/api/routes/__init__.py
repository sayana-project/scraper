# API Routes (C5)
from fastapi import APIRouter
from .properties import router as properties_router
from .analytics import router as analytics_router
from .auth import router as auth_router
from .health import router as health_router
from .init import router as init_router

# Route principale API
api_router = APIRouter(prefix="/api/v1")

# Inclusion des sous-routes
api_router.include_router(init_router, tags=["Initialisation"])
api_router.include_router(auth_router, tags=["Authentification"])
api_router.include_router(properties_router, tags=["Propriétés"])
api_router.include_router(analytics_router, tags=["Analytics"])
api_router.include_router(health_router, tags=["Health"])