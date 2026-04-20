import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.base import Base


class OrdemServico(Base):

    __tablename__ = "ordens_servico"

    # ID como UUID (padrão moderno)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    # relacionamento com cliente (UUID também)
    cliente_id = Column(String, ForeignKey("clientes.id"))

    equipamento = Column(String)
    problema = Column(String)
    solucao = Column(String)

    # status com valor padrão
    status = Column(String, default="aberta")

    valor = Column(Float, default=0.0)

    # timestamps (muito importante)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relacionamento
    cliente = relationship("Cliente", back_populates="ordens")

    
    # relacionamento com itens
    itens = relationship("OrdemServicoItem", back_populates="ordem", cascade="all, delete")
