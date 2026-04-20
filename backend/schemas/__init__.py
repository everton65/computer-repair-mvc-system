from .cliente_schema import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteListResponse
)
from .peca_schema import (
    PecaCreate,
    PecaUpdate,
    PecaResponse,
    PecaListResponse
)
from .servico_schema import (
    ServicoCreate,
    ServicoUpdate,
    ServicoResponse,
    ServicoListResponse
)
from .os_schema import (
    OSItemCreate,
    OSItemResponse,
    OSCreate,
    OSUpdate,
    OSResponse,
    OSListResponse
)

__all__ = [
    # Cliente
    "ClienteCreate",
    "ClienteUpdate",
    "ClienteResponse",
    "ClienteListResponse",
    # Peca
    "PecaCreate",
    "PecaUpdate",
    "PecaResponse",
    "PecaListResponse",
    # Servico
    "ServicoCreate",
    "ServicoUpdate",
    "ServicoResponse",
    "ServicoListResponse",
    # OS
    "OSItemCreate",
    "OSItemResponse",
    "OSCreate",
    "OSUpdate",
    "OSResponse",
    "OSListResponse"
]