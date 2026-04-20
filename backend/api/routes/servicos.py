from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.services.servico_service import ServicoService
from backend.schemas.servico_schema import (
    ServicoCreate,
    ServicoUpdate,
    ServicoResponse,
    ServicoListResponse
)

router = APIRouter(prefix="/servicos", tags=["Serviços"])


def get_servico_service(db: Session = Depends(get_db)) -> ServicoService:
    """Dependency injection for ServicoService."""
    return ServicoService(db)


@router.get("/", response_model=ServicoListResponse)
def listar_servicos(
    cliente_id: Optional[str] = Query(None, description="Filter by cliente ID"),
    service: ServicoService = Depends(get_servico_service)
):
    """Get all servicos or filter by cliente."""
    try:
        if cliente_id:
            servicos = service.get_by_cliente(cliente_id)
        else:
            servicos = service.get_all()

        return ServicoListResponse(
            servicos=servicos,
            total=len(servicos)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# IMPORTANT: This route must come BEFORE /{servico_id} to avoid path parameter conflict
@router.get("/total/valor")
def total_valor(
    service: ServicoService = Depends(get_servico_service)
):
    """Get total value of all servicos."""
    try:
        total = service.get_total_valor()
        return {"total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{servico_id}", response_model=ServicoResponse)
def buscar_servico(
    servico_id: str,
    service: ServicoService = Depends(get_servico_service)
):
    """Get servico by ID."""
    try:
        servico = service.get_by_id(servico_id)
        return ServicoResponse.model_validate(servico)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ServicoResponse, status_code=201)
def criar_servico(
    servico: ServicoCreate,
    service: ServicoService = Depends(get_servico_service)
):
    """Create a new servico."""
    try:
        novo = service.create(
            descricao=servico.descricao,
            valor=servico.valor,
            cliente_id=servico.cliente_id
        )
        return ServicoResponse.model_validate(novo)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{servico_id}", response_model=ServicoResponse)
def atualizar_servico(
    servico_id: str,
    servico: ServicoUpdate,
    service: ServicoService = Depends(get_servico_service)
):
    """Update an existing servico."""
    try:
        atualizado = service.update(
            servico_id=servico_id,
            descricao=servico.descricao,
            valor=servico.valor
        )
        return ServicoResponse.model_validate(atualizado)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{servico_id}")
def deletar_servico(
    servico_id: str,
    service: ServicoService = Depends(get_servico_service)
):
    """Delete a servico."""
    try:
        return service.delete(servico_id)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))