from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.peca import Peca
from backend.core.exceptions import NotFoundException, DatabaseException
from backend.utils.logger import get_logger, log_db_operation

logger = get_logger(__name__)


class PecaService:
    """Service for Peca business logic."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Peca]:
        """Get all pecas.

        Returns:
            List of Peca objects
        """
        try:
            pecas = self.db.query(Peca).all()
            logger.info(f"Retrieved {len(pecas)} pecas")
            return pecas
        except Exception as e:
            logger.error(f"Error getting pecas: {e}")
            raise DatabaseException("Erro ao buscar peças")

    def get_by_id(self, peca_id: str) -> Peca:
        """Get peca by ID.

        Args:
            peca_id: Peca UUID

        Returns:
            Peca object

        Raises:
            NotFoundException: If peca not found
        """
        try:
            peca = self.db.query(Peca).filter(Peca.id == peca_id).first()
            if not peca:
                raise NotFoundException("Peça", peca_id)
            log_db_operation("READ", "pecas", peca_id)
            return peca
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error getting peca {peca_id}: {e}")
            raise DatabaseException("Erro ao buscar peça")

    def create(self, nome: str, preco: float, quantidade: int) -> Peca:
        """Create a new peca.

        Args:
            nome: Part name
            preco: Price
            quantidade: Quantity in stock

        Returns:
            Created Peca object

        Raises:
            DatabaseException: If database error
        """
        try:
            peca = Peca(
                nome=nome.strip(),
                preco=float(preco),
                quantidade=int(quantidade)
            )

            self.db.add(peca)
            self.db.commit()
            self.db.refresh(peca)

            log_db_operation("CREATE", "pecas", peca.id)
            logger.info(f"Created peca: {peca.id} - {peca.nome}")

            return peca

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating peca: {e}")
            raise DatabaseException("Erro ao criar peça")

    def update(
        self,
        peca_id: str,
        nome: Optional[str] = None,
        preco: Optional[float] = None,
        quantidade: Optional[int] = None
    ) -> Peca:
        """Update an existing peca.

        Args:
            peca_id: Peca UUID
            nome: Optional new name
            preco: Optional new price
            quantidade: Optional new quantity

        Returns:
            Updated Peca object

        Raises:
            NotFoundException: If peca not found
            DatabaseException: If database error
        """
        try:
            peca = self.get_by_id(peca_id)

            if nome is not None:
                peca.nome = nome.strip()

            if preco is not None:
                peca.preco = float(preco)

            if quantidade is not None:
                peca.quantidade = int(quantidade)

            self.db.commit()
            self.db.refresh(peca)

            log_db_operation("UPDATE", "pecas", peca_id)
            logger.info(f"Updated peca: {peca_id}")

            return peca

        except NotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating peca {peca_id}: {e}")
            raise DatabaseException("Erro ao atualizar peça")

    def delete(self, peca_id: str) -> dict:
        """Delete a peca.

        Args:
            peca_id: Peca UUID

        Returns:
            Success message

        Raises:
            NotFoundException: If peca not found
            DatabaseException: If database error
        """
        try:
            peca = self.get_by_id(peca_id)

            self.db.delete(peca)
            self.db.commit()

            log_db_operation("DELETE", "pecas", peca_id)
            logger.info(f"Deleted peca: {peca_id}")

            return {"message": "Peça removida com sucesso", "id": peca_id}

        except NotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting peca {peca_id}: {e}")
            raise DatabaseException("Erro ao deletar peça")

    def search(self, query: str) -> List[Peca]:
        """Search pecas by name.

        Args:
            query: Search query

        Returns:
            List of matching Peca objects
        """
        try:
            search_term = f"%{query}%"
            pecas = self.db.query(Peca).filter(
                Peca.nome.ilike(search_term)
            ).all()
            logger.info(f"Found {len(pecas)} pecas matching '{query}'")
            return pecas
        except Exception as e:
            logger.error(f"Error searching pecas: {e}")
            raise DatabaseException("Erro ao buscar peças")

    def update_stock(self, peca_id: str, quantity_change: int) -> Peca:
        """Update peca stock quantity.

        Args:
            peca_id: Peca UUID
            quantity_change: Quantity to add (positive) or remove (negative)

        Returns:
            Updated Peca object

        Raises:
            NotFoundException: If peca not found
            ValidationException: If stock would go negative
        """
        try:
            peca = self.get_by_id(peca_id)
            new_quantity = peca.quantidade + quantity_change

            if new_quantity < 0:
                from backend.core.exceptions import ValidationException
                raise ValidationException(
                    f"Estoque insuficiente. Disponível: {peca.quantidade}"
                )

            peca.quantidade = new_quantity
            self.db.commit()
            self.db.refresh(peca)

            log_db_operation("UPDATE", "pecas", peca_id)
            logger.info(f"Updated stock for peca {peca_id}: {quantity_change:+d}")

            return peca

        except (NotFoundException, ValidationException):
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating stock for peca {peca_id}: {e}")
            raise DatabaseException("Erro ao atualizar estoque")