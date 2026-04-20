from pydantic import BaseModel, field_validator
from typing import Optional


class ServicoBase(BaseModel):
    """Base schema for Servico with common fields."""
    cliente_id: str
    descricao: str
    valor: float

    @field_validator("descricao")
    @classmethod
    def validate_descricao(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Descrição não pode estar vazia")
        if len(v.strip()) < 3:
            raise ValueError("Descrição deve ter pelo menos 3 caracteres")
        return v.strip()

    @field_validator("valor")
    @classmethod
    def validate_valor(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Valor não pode ser negativo")
        return v


class ServicoCreate(ServicoBase):
    """Schema for creating a new servico."""
    pass


class ServicoUpdate(BaseModel):
    """Schema for updating an existing servico."""
    descricao: Optional[str] = None
    valor: Optional[float] = None

    @field_validator("descricao")
    @classmethod
    def validate_descricao(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("Descrição não pode estar vazia")
            if len(v.strip()) < 3:
                raise ValueError("Descrição deve ter pelo menos 3 caracteres")
            return v.strip()
        return v

    @field_validator("valor")
    @classmethod
    def validate_valor(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("Valor não pode ser negativo")
        return v


class ServicoResponse(BaseModel):
    """Schema for servico response."""
    id: str
    cliente_id: str
    descricao: str
    valor: float

    class Config:
        from_attributes = True


class ServicoListResponse(BaseModel):
    """Schema for list of servicos."""
    servicos: list[ServicoResponse]
    total: int