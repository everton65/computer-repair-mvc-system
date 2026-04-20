from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.services.cliente_service import ClienteService
from backend.schemas.cliente_schema import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteListResponse
)

router = APIRouter(prefix="/clientes", tags=["Clientes"])


def get_cliente_service(db: Session = Depends(get_db)) -> ClienteService:
    """Dependency injection for ClienteService."""
    return ClienteService(db)


@router.get("/", response_model=ClienteListResponse)
def listar_clientes(
    search: Optional[str] = Query(None, description="Search by name or email"),
    service: ClienteService = Depends(get_cliente_service)
):
    """Get all clientes or search by name/email."""
    try:
        if search:
            clientes = service.search(search)
        else:
            clientes = service.get_all()

        return ClienteListResponse(
            clientes=[ClienteResponse.model_validate(c) for c in clientes],
            total=len(clientes)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(
    cliente_id: str,
    service: ClienteService = Depends(get_cliente_service)
):
    """Get cliente by ID."""
    try:
        cliente = service.get_by_id(cliente_id)
        return ClienteResponse.model_validate(cliente)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ClienteResponse, status_code=201)
def criar_cliente(
    cliente: ClienteCreate,
    service: ClienteService = Depends(get_cliente_service)
):
    """Create a new cliente."""
    try:
        novo = service.create(
            nome=cliente.nome,
            telefone=cliente.telefone,
            email=cliente.email
        )
        return ClienteResponse.model_validate(novo)
    except Exception as e:
        if "inválido" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(
    cliente_id: str,
    cliente: ClienteUpdate,
    service: ClienteService = Depends(get_cliente_service)
):
    """Update an existing cliente."""
    try:
        atualizado = service.update(
            cliente_id=cliente_id,
            nome=cliente.nome,
            telefone=cliente.telefone,
            email=cliente.email
        )
        return ClienteResponse.model_validate(atualizado)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        if "inválido" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{cliente_id}")
def deletar_cliente(
    cliente_id: str,
    service: ClienteService = Depends(get_cliente_service)
):
    """Delete a cliente."""
    try:
        return service.delete(cliente_id)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))