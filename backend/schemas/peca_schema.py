from pydantic import BaseModel, field_validator
from typing import Optional


class PecaBase(BaseModel):
    """Base schema for Peca with common fields."""
    nome: str
    preco: float
    quantidade: int

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Nome não pode estar vazio")
        if len(v.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        return v.strip()

    @field_validator("preco")
    @classmethod
    def validate_preco(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Preço não pode ser negativo")
        return v

    @field_validator("quantidade")
    @classmethod
    def validate_quantidade(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Quantidade não pode ser negativa")
        return v


class PecaCreate(PecaBase):
    """Schema for creating a new peca."""
    pass


class PecaUpdate(BaseModel):
    """Schema for updating an existing peca."""
    nome: Optional[str] = None
    preco: Optional[float] = None
    quantidade: Optional[int] = None

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("Nome não pode estar vazio")
            if len(v.strip()) < 2:
                raise ValueError("Nome deve ter pelo menos 2 caracteres")
            return v.strip()
        return v

    @field_validator("preco")
    @classmethod
    def validate_preco(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("Preço não pode ser negativo")
        return v

    @field_validator("quantidade")
    @classmethod
    def validate_quantidade(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError("Quantidade não pode ser negativa")
        return v


# ✅ ADICIONADO: Schema para atualização de estoque (usado no router /stock)
class StockUpdate(BaseModel):
    """Schema for updating peca stock quantity."""
    quantity: int

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        if v == 0:
            raise ValueError("Quantidade não pode ser zero")
        return v


class PecaResponse(BaseModel):
    """Schema for peca response."""
    id: str
    nome: str
    preco: float
    quantidade: int

    class Config:
        from_attributes = True


class PecaListResponse(BaseModel):
    """Schema for list of pecas."""
    pecas: list[PecaResponse]
    total: int