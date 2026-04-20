import re
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class ClienteBase(BaseModel):
    """Base schema for Cliente with common fields."""
    nome: str
    telefone: str
    email: EmailStr

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Nome não pode estar vazio")
        if len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        return v.strip()

    @field_validator("telefone")
    @classmethod
    def validate_telefone(cls, v: str) -> str:
        # Remove non-digits
        telefone_limpo = re.sub(r"\D", "", v)
        if len(telefone_limpo) < 10:
            raise ValueError("Telefone deve ter pelo menos 10 dígitos")
        return telefone_limpo


class ClienteCreate(ClienteBase):
    """Schema for creating a new cliente."""
    pass


class ClienteUpdate(BaseModel):
    """Schema for updating an existing cliente."""
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("Nome não pode estar vazio")
            if len(v.strip()) < 3:
                raise ValueError("Nome deve ter pelo menos 3 caracteres")
            return v.strip()
        return v

    @field_validator("telefone")
    @classmethod
    def validate_telefone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            telefone_limpo = re.sub(r"\D", "", v)
            if len(telefone_limpo) < 10:
                raise ValueError("Telefone deve ter pelo menos 10 dígitos")
            return telefone_limpo
        return v


class ClienteResponse(BaseModel):
    """Schema for cliente response."""
    id: str
    nome: str
    telefone: str
    email: str

    class Config:
        from_attributes = True


class ClienteListResponse(BaseModel):
    """Schema for list of clientes."""
    clientes: list[ClienteResponse]
    total: int