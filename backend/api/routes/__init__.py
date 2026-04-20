from .clientes import router as clientes_router
from .pecas import router as pecas_router
from .servicos import router as servicos_router
from .ordens import router as ordens_router
from .relatorios import router as relatorios_router

__all__ = [
    "clientes_router",
    "pecas_router",
    "servicos_router",
    "ordens_router",
    "relatorios_router"
]