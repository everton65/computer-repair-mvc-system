from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.services.ordem_service import OrdemService
from backend.schemas.os_schema import (
    OSCreate,
    OSUpdate,
    OSResponse,
    OSListResponse
)

router = APIRouter(prefix="/ordens", tags=["Ordens de Serviço"])


def get_ordem_service(db: Session = Depends(get_db)) -> OrdemService:
    """Dependency injection for OrdemService."""
    return OrdemService(db)


@router.get("/", response_model=OSListResponse)
def listar_ordens(
    cliente_id: Optional[str] = Query(None, description="Filter by cliente ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    service: OrdemService = Depends(get_ordem_service)
):
    """Get all ordens or filter by cliente/status."""
    try:
        if cliente_id:
            ordens = service.get_by_cliente(cliente_id)
        elif status:
            ordens = service.get_by_status(status)
        else:
            ordens = service.get_all()

        return OSListResponse(
            ordens=[service.to_dict(o) for o in ordens],
            total=len(ordens)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ordem_id}")
def buscar_ordem(
    ordem_id: str,
    service: OrdemService = Depends(get_ordem_service)
):
    """Get ordem by ID with all details."""
    try:
        ordem = service.get_by_id(ordem_id)
        return service.to_dict(ordem)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=201)
def criar_ordem(
    ordem: OSCreate,
    service: OrdemService = Depends(get_ordem_service)
):
    """Create a new ordem with items."""
    try:
        # Convert items to dict list
        itens_data = [
            {"descricao": item.descricao, "valor": item.valor}
            for item in ordem.itens
        ]

        nova = service.create(
            cliente_id=ordem.cliente_id,
            itens=itens_data,
            equipamento=ordem.equipamento,
            problema=ordem.problema
        )
        return service.to_dict(nova)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{ordem_id}")
def atualizar_ordem(
    ordem_id: str,
    ordem: OSUpdate,
    service: OrdemService = Depends(get_ordem_service)
):
    """Update an existing ordem."""
    try:
        atualizada = service.update(
            ordem_id=ordem_id,
            equipamento=ordem.equipamento,
            problema=ordem.problema,
            solucao=ordem.solucao,
            status=ordem.status
        )
        return service.to_dict(atualizada)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{ordem_id}")
def deletar_ordem(
    ordem_id: str,
    service: OrdemService = Depends(get_ordem_service)
):
    """Delete an ordem."""
    try:
        return service.delete(ordem_id)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))