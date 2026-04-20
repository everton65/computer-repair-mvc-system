from typing import List, Optional
from sqlalchemy.orm import Session, joinedload  # ✅ adicionar joinedload
from datetime import datetime

from backend.models.ordem_servico import OrdemServico
from backend.models.ordem_servico_item import OrdemServicoItem
from backend.models.cliente import Cliente
from backend.core.exceptions import NotFoundException, DatabaseException
from backend.utils.logger import get_logger, log_db_operation

logger = get_logger(__name__)


class OrdemService:

    def __init__(self, db: Session):
        self.db = db

    def _query_with_relations(self):
        """Query base com eager loading de cliente e itens."""
        return self.db.query(OrdemServico).options(
            joinedload(OrdemServico.cliente),   # ✅ carrega cliente junto
            joinedload(OrdemServico.itens)      # ✅ carrega itens junto
        )

    def get_all(self) -> List[OrdemServico]:
        try:
            # ✅ CORRIGIDO: eager loading evita lazy load error
            ordens = self._query_with_relations().all()
            logger.info(f"Retrieved {len(ordens)} ordens")
            return ordens
        except Exception as e:
            logger.error(f"Error getting ordens: {e}")
            raise DatabaseException("Erro ao buscar ordens de serviço")

    def get_by_id(self, ordem_id: str) -> OrdemServico:
        try:
            # ✅ CORRIGIDO: eager loading
            ordem = self._query_with_relations().filter(
                OrdemServico.id == ordem_id
            ).first()

            if not ordem:
                raise NotFoundException("Ordem de Serviço", ordem_id)

            log_db_operation("READ", "ordens_servico", ordem_id)
            return ordem

        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error getting ordem {ordem_id}: {e}")
            raise DatabaseException("Erro ao buscar ordem de serviço")

    def get_by_cliente(self, cliente_id: str) -> List[OrdemServico]:
        try:
            # ✅ CORRIGIDO: eager loading
            ordens = self._query_with_relations().filter(
                OrdemServico.cliente_id == cliente_id
            ).all()
            logger.info(f"Retrieved {len(ordens)} ordens for cliente {cliente_id}")
            return ordens
        except Exception as e:
            logger.error(f"Error getting ordens for cliente {cliente_id}: {e}")
            raise DatabaseException("Erro ao buscar ordens do cliente")

    def get_by_status(self, status: str) -> List[OrdemServico]:
        try:
            # ✅ CORRIGIDO: eager loading
            ordens = self._query_with_relations().filter(
                OrdemServico.status == status
            ).all()
            logger.info(f"Retrieved {len(ordens)} ordens with status {status}")
            return ordens
        except Exception as e:
            logger.error(f"Error getting ordens with status {status}: {e}")
            raise DatabaseException("Erro ao buscar ordens por status")

    def create(
        self,
        cliente_id: str,
        itens: List[dict],
        equipamento: Optional[str] = None,
        problema: Optional[str] = None
    ) -> OrdemServico:
        try:
            cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
            if not cliente:
                raise NotFoundException("Cliente", cliente_id)

            total = sum(item.get("valor", 0) for item in itens)

            ordem = OrdemServico(
                cliente_id=cliente_id,
                equipamento=equipamento,
                problema=problema,
                status="aberta",
                valor=total
            )

            self.db.add(ordem)
            self.db.flush()

            for item_data in itens:
                item = OrdemServicoItem(
                    ordem_id=ordem.id,
                    descricao=item_data.get("descricao"),
                    valor=item_data.get("valor", 0)
                )
                self.db.add(item)

            self.db.commit()

            # ✅ CORRIGIDO: recarrega com relações após commit
            return self.get_by_id(str(ordem.id))

        except NotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating ordem: {e}")
            raise DatabaseException("Erro ao criar ordem de serviço")

    def update(
        self,
        ordem_id: str,
        equipamento: Optional[str] = None,
        problema: Optional[str] = None,
        solucao: Optional[str] = None,
        status: Optional[str] = None
    ) -> OrdemServico:
        try:
            ordem = self.get_by_id(ordem_id)

            if equipamento is not None:
                ordem.equipamento = equipamento
            if problema is not None:
                ordem.problema = problema
            if solucao is not None:
                ordem.solucao = solucao
            if status is not None:
                ordem.status = status

            ordem.atualizado_em = datetime.utcnow()

            self.db.commit()

            # ✅ CORRIGIDO: recarrega com relações após commit
            return self.get_by_id(ordem_id)

        except NotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating ordem {ordem_id}: {e}")
            raise DatabaseException("Erro ao atualizar ordem de serviço")

    def delete(self, ordem_id: str) -> dict:
        try:
            ordem = self.get_by_id(ordem_id)
            self.db.delete(ordem)
            self.db.commit()

            log_db_operation("DELETE", "ordens_servico", ordem_id)
            logger.info(f"Deleted ordem: {ordem_id}")

            return {"message": "Ordem de serviço removida com sucesso", "id": ordem_id}

        except NotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting ordem {ordem_id}: {e}")
            raise DatabaseException("Erro ao deletar ordem de serviço")

    def to_dict(self, ordem: OrdemServico) -> dict:
        return {
            "id": str(ordem.id),
            "cliente_id": str(ordem.cliente_id),
            "cliente_nome": ordem.cliente.nome if ordem.cliente else "Desconhecido",
            "equipamento": ordem.equipamento,
            "problema": ordem.problema,
            "solucao": ordem.solucao,
            "status": ordem.status,
            "valor": float(ordem.valor) if ordem.valor else 0.0,
            "criado_em": ordem.criado_em.isoformat() if ordem.criado_em else None,
            "atualizado_em": ordem.atualizado_em.isoformat() if ordem.atualizado_em else None,
            "itens": [
                {
                    "id": str(item.id),
                    "ordem_id": str(item.ordem_id),  # ✅ campo faltando
                    "descricao": item.descricao,
                    "valor": float(item.valor) if item.valor else 0.0
                }
                for item in (ordem.itens or [])
            ]
        }