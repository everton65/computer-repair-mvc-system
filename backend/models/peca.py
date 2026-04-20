import uuid

from sqlalchemy import Column, String, Float, Integer
from database.base import Base


class Peca(Base):

    __tablename__ = "pecas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)

    def to_dict(self):

        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade
        }