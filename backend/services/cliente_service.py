from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.cliente import Cliente
from backend.core.exceptions import NotFoundException, ValidationException, DatabaseException
from backend.utils.logger import get_logger, log_db_operation

logger = get_logger(__name__)


class ClienteService:
    """Service for Cliente business logic."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Cliente]:
        """Get all clientes.

        Returns:
            List of Cliente objects
        """
        try:
            clientes = self.db.query(Cliente).all()
            logger.info(f"Retrieved {len(clientes)} clientes")
            return clientes
        except Exception as e:
            logger.error(f"Error getting clientes: {e}")
            raise DatabaseException("Erro ao buscar clientes")

    def get_by_id(self, cliente_id: str) -> Cliente:
        """Get cliente by ID.

        Args:
            cliente_id: Cliente UUID

        Returns:
            Cliente object

        Raises:
            NotFoundException: If cliente not found
        """
        try:
            cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
            if not cliente:
                raise NotFoundException("Cliente", cliente_id)
            log_db_operation("READ", "clientes", cliente_id)
            return cliente
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error getting cliente {cliente_id}: {e}")
            raise DatabaseException("Erro ao buscar cliente")

    def create(self, nome: str, telefone: str, email: str) -> Cliente:
        """Create a new cliente.

        Args:
            nome: Client name
            telefone: Phone number
            email: Email address

        Returns:
            Created Cliente object

        Raises:
            ValidationException: If validation fails
            DatabaseException: If database error
        """
        try:
            # Validate email
            if not Cliente.validar_email(email):
                raise ValidationException("Email inválido")

            # Validate telefone
            if not Cliente.validar_telefone(telefone):
                raise ValidationException("Telefone inválido. Deve ter pelo menos 10 dígitos")

            cliente = Cliente(
                nome=nome.strip(),
                telefone=Cliente.formatar_telefone(telefone),
                email=email.strip().lower()
            )

            self.db.add(cliente)
            self.db.commit()
            self.db.refresh(cliente)

            log_db_operation("CREATE", "clientes", cliente.id)
            logger.info(f"Created cliente: {cliente.id} - {cliente.nome}")

            return cliente

        except ValidationException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating cliente: {e}")
            raise DatabaseException("Erro ao criar cliente")

    def update(
        self,
        cliente_id: str,
        nome: Optional[str] = None,
        telefone: Optional[str] = None,
        email: Optional[str] = None
    ) -> Cliente:
        """Update an existing cliente.

        Args:
            cliente_id: Cliente UUID
            nome: Optional new name
            telefone: Optional new phone
            email: Optional new email

        Returns:
            Updated Cliente object

        Raises:
            NotFoundException: If cliente not found
            ValidationException: If validation fails
            DatabaseException: If database error
        """
        try:
            cliente = self.get_by_id(cliente_id)

            if nome is not None:
                cliente.nome = nome.strip()

            if telefone is not None:
                if not Cliente.validar_telefone(telefone):
                    raise ValidationException("Telefone inválido")
                cliente.telefone = Cliente.formatar_telefone(telefone)

            if email is not None:
                if not Cliente.validar_email(email):
                    raise ValidationException("Email inválido")
                cliente.email = email.strip().lower()

            self.db.commit()
            self.db.refresh(cliente)

            log_db_operation("UPDATE", "clientes", cliente_id)
            logger.info(f"Updated cliente: {cliente_id}")

            return cliente

        except (NotFoundException, ValidationException):
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating cliente {cliente_id}: {e}")
            raise DatabaseException("Erro ao atualizar cliente")

    def delete(self, cliente_id: str) -> dict:
        """Delete a cliente.

        Args:
            cliente_id: Cliente UUID

        Returns:
            Success message

        Raises:
            NotFoundException: If cliente not found
            DatabaseException: If database error
        """
        try:
            cliente = self.get_by_id(cliente_id)

            self.db.delete(cliente)
            self.db.commit()

            log_db_operation("DELETE", "clientes", cliente_id)
            logger.info(f"Deleted cliente: {cliente_id}")

            return {"message": "Cliente removido com sucesso", "id": cliente_id}

        except NotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting cliente {cliente_id}: {e}")
            raise DatabaseException("Erro ao deletar cliente")

    def search(self, query: str) -> List[Cliente]:
        """Search clientes by name or email.

        Args:
            query: Search query

        Returns:
            List of matching Cliente objects
        """
        try:
            search_term = f"%{query}%"
            clientes = self.db.query(Cliente).filter(
                (Cliente.nome.ilike(search_term)) |
                (Cliente.email.ilike(search_term))
            ).all()
            logger.info(f"Found {len(clientes)} clientes matching '{query}'")
            return clientes
        except Exception as e:
            logger.error(f"Error searching clientes: {e}")
            raise DatabaseException("Erro ao buscar clientes")