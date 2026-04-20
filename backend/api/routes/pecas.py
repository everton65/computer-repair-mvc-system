from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.services.peca_service import PecaService
from backend.schemas.peca_schema import (
    PecaCreate,
    PecaUpdate,
    PecaResponse,
    PecaListResponse,
    StockUpdate  
)

router = APIRouter(prefix="/pecas", tags=["Peças"])


# ✅ NOVO: Schema para receber quantity no body
class StockUpdate(BaseModel):
    quantity: int


def get_peca_service(db: Session = Depends(get_db)) -> PecaService:
    """Dependency injection for PecaService."""
    return PecaService(db)


@router.get("/", response_model=PecaListResponse)
def listar_pecas(
    search: Optional[str] = Query(None, description="Search by name"),
    service: PecaService = Depends(get_peca_service)
):
    """Get all pecas or search by name."""
    try:
        if search:
            pecas = service.search(search)
        else:
            pecas = service.get_all()

        return PecaListResponse(
            pecas=[PecaResponse.model_validate(p) for p in pecas],
            total=len(pecas)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{peca_id}", response_model=PecaResponse)
def buscar_peca(
    peca_id: str,
    service: PecaService = Depends(get_peca_service)
):
    """Get peca by ID."""
    try:
        peca = service.get_by_id(peca_id)
        return PecaResponse.model_validate(peca)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=PecaResponse, status_code=201)
def criar_peca(
    peca: PecaCreate,
    service: PecaService = Depends(get_peca_service)
):
    """Create a new peca."""
    try:
        nova = service.create(
            nome=peca.nome,
            preco=peca.preco,
            quantidade=peca.quantidade
        )
        return PecaResponse.model_validate(nova)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{peca_id}", response_model=PecaResponse)
def atualizar_peca(
    peca_id: str,
    peca: PecaUpdate,
    service: PecaService = Depends(get_peca_service)
):
    """Update an existing peca."""
    try:
        atualizada = service.update(
            peca_id=peca_id,
            nome=peca.nome,
            preco=peca.preco,
            quantidade=peca.quantidade
        )
        return PecaResponse.model_validate(atualizada)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{peca_id}")
def deletar_peca(
    peca_id: str,
    service: PecaService = Depends(get_peca_service)
):
    """Delete a peca."""
    try:
        return service.delete(peca_id)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{peca_id}/stock", response_model=PecaResponse)
def atualizar_estoque(
    peca_id: str,
    stock_update: StockUpdate,  # ✅ CORRIGIDO: body em vez de query param
    service: PecaService = Depends(get_peca_service)
):
    """Update peca stock quantity."""
    try:
        atualizada = service.update_stock(peca_id, stock_update.quantity)
        return PecaResponse.model_validate(atualizada)
    except Exception as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        if "insuficiente" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))