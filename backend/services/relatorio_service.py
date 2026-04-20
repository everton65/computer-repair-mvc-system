from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models.cliente import Cliente
from backend.models.servico import Servico
from backend.models.peca import Peca
from backend.models.ordem_servico import OrdemServico
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class RelatorioService:
    """Service for reports and statistics."""

    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics.

        Returns:
            Dict with total counts and revenue
        """
        try:
            total_clientes = self.db.query(func.count(Cliente.id)).scalar() or 0
            total_servicos = self.db.query(func.count(Servico.id)).scalar() or 0
            total_pecas = self.db.query(func.count(Peca.id)).scalar() or 0
            total_ordens = self.db.query(func.count(OrdemServico.id)).scalar() or 0

            faturamento = self.db.query(func.sum(Servico.valor)).scalar() or 0
            faturamento = float(faturamento) if faturamento else 0.0

            pecas_estoque = self.db.query(func.sum(Peca.quantidade)).scalar() or 0

            stats = {
                "total_clientes": total_clientes,
                "total_servicos": total_servicos,
                "total_pecas": total_pecas,
                "total_ordens": total_ordens,
                "faturamento": faturamento,
                "pecas_estoque": pecas_estoque
            }

            logger.info(f"Dashboard stats: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Error getting dashboard stats: {e}")
            return {
                "total_clientes": 0,
                "total_servicos": 0,
                "total_pecas": 0,
                "total_ordens": 0,
                "faturamento": 0.0,
                "pecas_estoque": 0
            }

    def get_clientes_relatorio(self) -> List[Dict[str, Any]]:
        """Get clientes report with order counts.

        Returns:
            List of cliente dicts with stats
        """
        try:
            clientes = self.db.query(Cliente).all()

            result = []
            for cliente in clientes:
                ordens_count = self.db.query(func.count(OrdemServico.id)).filter(
                    OrdemServico.cliente_id == cliente.id
                ).scalar() or 0

                servicos_total = self.db.query(func.sum(Servico.valor)).filter(
                    Servico.cliente_id == cliente.id
                ).scalar() or 0

                result.append({
                    "id": cliente.id,
                    "nome": cliente.nome,
                    "telefone": cliente.telefone,
                    "email": cliente.email,
                    "total_ordens": ordens_count,
                    "total_servicos": float(servicos_total) if servicos_total else 0.0
                })

            logger.info(f"Generated report for {len(result)} clientes")
            return result

        except Exception as e:
            logger.error(f"Error generating clientes report: {e}")
            return []

    def get_servicos_relatorio(self) -> List[Dict[str, Any]]:
        """Get servicos report.

        Returns:
            List of servico dicts
        """
        try:
            servicos = self.db.query(Servico).all()

            result = []
            for servico in servicos:
                result.append({
                    "id": servico.id,
                    "descricao": servico.descricao,
                    "valor": servico.valor,
                    "cliente_id": servico.cliente_id,
                    "cliente_nome": servico.cliente.nome if servico.cliente else None
                })

            logger.info(f"Generated report for {len(result)} servicos")
            return result

        except Exception as e:
            logger.error(f"Error generating servicos report: {e}")
            return []

    def get_pecas_relatorio(self) -> List[Dict[str, Any]]:
        """Get pecas report with stock info.

        Returns:
            List of peca dicts
        """
        try:
            pecas = self.db.query(Peca).all()

            result = []
            for peca in pecas:
                valor_estoque = peca.preco * peca.quantidade
                result.append({
                    "id": peca.id,
                    "nome": peca.nome,
                    "preco": peca.preco,
                    "quantidade": peca.quantidade,
                    "valor_estoque": valor_estoque
                })

            logger.info(f"Generated report for {len(result)} pecas")
            return result

        except Exception as e:
            logger.error(f"Error generating pecas report: {e}")
            return []

    def get_ordens_relatorio(self, status: str = None) -> List[Dict[str, Any]]:
        """Get ordens report optionally filtered by status.

        Args:
            status: Optional status filter

        Returns:
            List of ordem dicts
        """
        try:
            query = self.db.query(OrdemServico)

            if status:
                query = query.filter(OrdemServico.status == status)

            ordens = query.all()

            result = []
            for ordem in ordens:
                result.append({
                    "id": ordem.id,
                    "cliente_id": ordem.cliente_id,
                    "cliente_nome": ordem.cliente.nome if ordem.cliente else None,
                    "equipamento": ordem.equipamento,
                    "problema": ordem.problema,
                    "solucao": ordem.solucao,
                    "status": ordem.status,
                    "valor": ordem.valor,
                    "criado_em": ordem.criado_em.isoformat() if ordem.criado_em else None,
                    "total_itens": len(ordem.itens)
                })

            logger.info(f"Generated report for {len(result)} ordens")
            return result

        except Exception as e:
            logger.error(f"Error generating ordens report: {e}")
            return []

    def get_faturamento_por_periodo(self, data_inicio=None, data_fim=None) -> Dict[str, Any]:
        """Get revenue by period.

        Args:
            data_inicio: Start date
            data_fim: End date

        Returns:
            Dict with revenue stats
        """
        try:
            query = self.db.query(func.sum(Servico.valor))

            # TODO: Implement date filtering when Servico has date field

            total = query.scalar() or 0

            return {
                "total": float(total) if total else 0.0,
                "data_inicio": data_inicio,
                "data_fim": data_fim
            }

        except Exception as e:
            logger.error(f"Error getting faturamento: {e}")
            return {"total": 0.0}