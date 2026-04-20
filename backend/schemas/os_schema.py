from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


class OSItemBase(BaseModel):
    """Base schema for OS Item."""
    descricao: str
    valor: float

    @field_validator("descricao")
    @classmethod
    def validate_descricao(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Descrição não pode estar vazia")
        return v.strip()

    @field_validator("valor")
    @classmethod
    def validate_valor(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Valor não pode ser negativo")
        return v


class OSItemCreate(OSItemBase):
    """Schema for creating a new OS item."""
    pass


class OSItemResponse(BaseModel):
    """Schema for OS item response."""
    id: str
    ordem_id: str
    descricao: str
    valor: float

    class Config:
        from_attributes = True


class OSBase(BaseModel):
    """Base schema for Ordem de Servico."""
    cliente_id: str
    equipamento: Optional[str] = None
    problema: Optional[str] = None
    solucao: Optional[str] = None
    status: str = "aberta"

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        valid_statuses = ["aberta", "em_andamento", "aguardando_pecas", "concluida", "cancelada"]
        if v not in valid_statuses:
            raise ValueError(f"Status deve ser um de: {', '.join(valid_statuses)}")
        return v


class OSCreate(BaseModel):
    """Schema for creating a new OS."""
    cliente_id: str
    itens: list[OSItemCreate]
    equipamento: Optional[str] = None
    problema: Optional[str] = None

    @field_validator("itens")
    @classmethod
    def validate_itens(cls, v: list) -> list:
        if not v or len(v) == 0:
            raise ValueError("OS deve ter pelo menos um item")
        return v


class OSUpdate(BaseModel):
    """Schema for updating an existing OS."""
    equipamento: Optional[str] = None
    problema: Optional[str] = None
    solucao: Optional[str] = None
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            valid_statuses = ["aberta", "em_andamento", "aguardando_pecas", "concluida", "cancelada"]
            if v not in valid_statuses:
                raise ValueError(f"Status deve ser um de: {', '.join(valid_statuses)}")
        return v


class OSResponse(BaseModel):
    """Schema for OS response."""
    id: str
    cliente_id: str
    equipamento: Optional[str]
    problema: Optional[str]
    solucao: Optional[str]
    status: str
    valor: float
    criado_em: datetime
    atualizado_em: Optional[datetime]
    itens: list[OSItemResponse] = []

    class Config:
        from_attributes = True


class OSListResponse(BaseModel):
    """Schema for list of OS."""
    ordens: list[OSResponse]
    total: int