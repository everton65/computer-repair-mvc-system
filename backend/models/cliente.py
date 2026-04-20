import uuid
import re
from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database.base import Base

# 👇 evita import circular e ajuda o SQLAlchemy
if TYPE_CHECKING:
    from backend.models.ordem_servico import OrdemServico


class Cliente(Base):

    __tablename__ = "clientes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # 🔥 RELACIONAMENTO CORRETO
    ordens = relationship(
        "OrdemServico",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )

    # ===============================
    # SERIALIZAÇÃO
    # ===============================
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email
        }

    # ===============================
    # VALIDAÇÕES
    # ===============================
    @staticmethod
    def validar_email(email):
        padrao = r"^[^@]+@[^@]+\.[^@]+$"
        return re.match(padrao, email) is not None

    @staticmethod
    def validar_telefone(telefone):
        telefone_limpo = re.sub(r"\D", "", telefone)
        return len(telefone_limpo) >= 10

    @staticmethod
    def formatar_telefone(telefone):
        telefone_limpo = re.sub(r"\D", "", telefone)

        if len(telefone_limpo) == 11:
            return f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
        elif len(telefone_limpo) == 10:
            return f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
        
        return telefone