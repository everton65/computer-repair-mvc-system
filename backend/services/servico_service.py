from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.servico import Servico
from backend.models.cliente import Cliente
from backend.core.exceptions import NotFoundException, DatabaseException
from backend.utils.logger import get_logger, log_db_operation

logger = get_logger(__name__)


class ServicoService:
    """Service for Servico business logic."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[dict]:
        """Get all servicos with cliente info.

        Returns:
            List of servico dicts with cliente name
        """
        try:
            servicos = self.db.query(Servico).all()
            result = []

            for s in servicos:
                result.append({
                    "id": s.id,
                    "descricao": s.descricao,
                    "valor": s.valor,
                    "cliente_id": s.cliente_id,
                    "cliente_nome": s.cliente.nome if s.cliente else None
                })

            logger.info(f"Retrieved {len(servicos)} servicos")
            return result

        except Exception as e:
            logger.error(f"Error getting servicos: {e}")
            raise DatabaseException("Erro ao buscar serviços")

    def get_by_id(self, servico_id: str) -> Servico:
        """Get servico by ID.

        Args:
            servico_id: Servico UUID

        Returns:
            Servico object

        Raises:
            NotFoundException: If servico not found
        """
        try:
            servico = self.db.query(Servico).filter(Servico.id == servico_id).first()
            if not servico:
                raise NotFoundException("Serviço", servico_id)
            log_db_operation("READ", "servicos", servico_id)
            return servico
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error getting servico {servico_id}: {e}")
            raise DatabaseException("Erro ao buscar serviço")

    def create(self, descricao: str, valor: float, cliente_id: str) -> Servico:
        """Create a new servico.

        Args:
            descricao: Service description
            valor: Service value
            cliente_id: Client UUID

        Returns:
            Created Servico object

        Raises:
            NotFoundException: If cliente not found
            DatabaseException: If database error
        """
        try:
            # Verify cliente exists
            cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
            if not cliente:
                raise NotFoundException("Cliente", cliente_id)

            servico = Servico(
                descricao=descricao.strip(),
                valor=float(valor),
                cliente_id=cliente_id
            )

            self.db.add(servico)
            self.db.commit()
            self.db.refresh(servico)

            log_db_operation("CREATE", "servicos", servico.id)
            logger.info(f"Created servico: {servico.id} - {servico.descricao}")

            return servico

        except NotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating servico: {e}")
            raise DatabaseException("Erro ao criar serviço")

    def update(
        self,
        servico_id: str,
        descricao: Optional[str] = None,
        valor: Optional[float] = None
    ) -> Servico:
        """Update an existing servico.

        Args:
            servico_id: Servico UUID
            descricao: Optional new description
            valor: Optional new value

        Returns:
            Updated Servico object

        Raises:
            NotFoundException: If servico not found
            DatabaseException: If database error
        """
        try:
            servico = self.get_by_id(servico_id)

            if descricao is not None:
                servico.descricao = descricao.strip()

            if valor is not None:
                servico.valor = float(valor)

            self.db.commit()
            self.db.refresh(servico)

            log_db_operation("UPDATE", "servicos", servico_id)
            logger.info(f"Updated servico: {servico_id}")

            return servico

        except NotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating servico {servico_id}: {e}")
            raise DatabaseException("Erro ao atualizar serviço")

    def delete(self, servico_id: str) -> dict:
        """Delete a servico.

        Args:
            servico_id: Servico UUID

        Returns:
            Success message

        Raises:
            NotFoundException: If servico not found
            DatabaseException: If database error
        """
        try:
            servico = self.get_by_id(servico_id)

            self.db.delete(servico)
            self.db.commit()

            log_db_operation("DELETE", "servicos", servico_id)
            logger.info(f"Deleted servico: {servico_id}")

            return {"message": "Serviço removido com sucesso", "id": servico_id}

        except NotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting servico {servico_id}: {e}")
            raise DatabaseException("Erro ao deletar serviço")

    def get_by_cliente(self, cliente_id: str) -> List[Servico]:
        """Get all servicos for a specific cliente.

        Args:
            cliente_id: Cliente UUID

        Returns:
            List of Servico objects
        """
        try:
            servicos = self.db.query(Servico).filter(
                Servico.cliente_id == cliente_id
            ).all()
            logger.info(f"Retrieved {len(servicos)} servicos for cliente {cliente_id}")
            return servicos
        except Exception as e:
            logger.error(f"Error getting servicos for cliente {cliente_id}: {e}")
            raise DatabaseException("Erro ao buscar serviços do cliente")

    def get_total_valor(self) -> float:
        """Get total value of all servicos.

        Returns:
            Total value
        """
        try:
            from sqlalchemy import func
            result = self.db.query(func.sum(Servico.valor)).scalar()
            return float(result or 0)
        except Exception as e:
            logger.error(f"Error getting total valor: {e}")
            return 0.0