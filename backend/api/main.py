from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.core.exceptions import AppException, exception_handler
from database.connection import init_db
from backend.api.routes import clientes, pecas, servicos, relatorios, ordens


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    init_db()
    yield
    # Shutdown (if needed)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clientes.router, prefix=settings.API_PREFIX)
app.include_router(pecas.router, prefix=settings.API_PREFIX)
app.include_router(servicos.router, prefix=settings.API_PREFIX)
app.include_router(relatorios.router, prefix=settings.API_PREFIX)
app.include_router(ordens.router, prefix=settings.API_PREFIX)


@app.get("/")
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/health")
def health():
    """Alias for health check."""
    return {"status": "healthy"}