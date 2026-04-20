import uuid

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class Servico(Base):

    __tablename__ = "servicos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)

    cliente_id = Column(String, ForeignKey("clientes.id"))

    cliente = relationship("Cliente")

    def to_dict(self):

        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "cliente_id": self.cliente_id
        }