from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import re
import uuid

EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")

@dataclass
class cliente:

    id: str
    nome: str
    telefone: str
    email: str

    @staticmethod
    def novo(nome: str, telefone: str, email: str) -> "cliente":
          
        return cliente(
        id=str(uuid.uuid4()),
        nome=nome.strip(),
        telefone=telefone.strip(),
        email=email.strip()
        )
    
    @staticmethod
    def validar_email(email: str) -> bool:
        return bool(EMAIL_RE.match(email.strip()))
          
    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        digits = re.sub(r"\D", "", telefone)
        return len(digits) >= 6

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "cliente":
        return cliente(
            id=str(data.get("id")),
            nome=str(data.get("nome", "")),
            telefone=str(data.get("telefone", "")),
            email=str(data.get("email", ""))
        )

    def __str__(self) -> str:
        return f"[{self.id}] {self.nome} | Tel: {self.telefone} | Email: {self.email}"

    def atualizar(self, nome: Optional[str] = None, telefone: Optional[str] = None, email: Optional[str] = None) -> None:
        if nome is not None and nome.strip():
            self.nome = nome.strip()
        
        if telefone is not None and telefone.strip():
            if not cliente.validar_telefone(telefone):
                raise ValueError("Telefone inválido (deve ter ao menos 6 dígitos).")
            self.telefone = telefone.strip()

        if email is not None and email.strip():
            if not cliente.validar_email(email):
                raise ValueError("E-mail inválido.")
            self.email = email.strip()

if __name__ == "__main__":
    c = cliente.novo("João Silva", "(81) 99999-9999", "joao@example.com")
    print("Criado:", c)
    d = c.to_dict()
    print("Dict:", d)
    c2 = cliente.from_dict(d)
    print("From dict:", c2)
    try:
        c2.atualizar(nome="João S.", telefone="123")
    except ValueError as e:
        print("Erro ao atualizar telefone:", e)
    c2.atualizar(telefone="81 98888-7777", email="joao.s@example.com")
    print("Atualizado:", c2)
