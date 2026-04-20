import uuid

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class OrdemServicoItem(Base):

    __tablename__ = "ordem_servico_itens"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    ordem_id = Column(String, ForeignKey("ordens_servico.id"))
    descricao = Column(String)
    valor = Column(Float)

    # relacionamento
    ordem = relationship("OrdemServico", back_populates="itens")