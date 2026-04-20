from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.services.relatorio_service import RelatorioService

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


def get_relatorio_service(db: Session = Depends(get_db)) -> RelatorioService:
    """Dependency injection for RelatorioService."""
    return RelatorioService(db)


@router.get("/dashboard")
def dashboard_stats(
    service: RelatorioService = Depends(get_relatorio_service)
):
    """Get dashboard statistics."""
    return service.get_dashboard_stats()


@router.get("/clientes")
def relatorio_clientes(
    service: RelatorioService = Depends(get_relatorio_service)
):
    """Get clientes report with stats."""
    return service.get_clientes_relatorio()


@router.get("/servicos")
def relatorio_servicos(
    service: RelatorioService = Depends(get_relatorio_service)
):
    """Get servicos report."""
    return service.get_servicos_relatorio()


@router.get("/pecas")
def relatorio_pecas(
    service: RelatorioService = Depends(get_relatorio_service)
):
    """Get pecas report with stock info."""
    return service.get_pecas_relatorio()


@router.get("/ordens")
def relatorio_ordens(
    status: Optional[str] = None,
    service: RelatorioService = Depends(get_relatorio_service)
):
    """Get ordens report optionally filtered by status."""
    return service.get_ordens_relatorio(status=status)