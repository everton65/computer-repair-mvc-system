import uuid

class Peca:
    def __init__(self, id: str, nome: str, preco: float, quantidade: int):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
    
    @classmethod
    def nova(cls, nome: str, preco: float, quantidade: int):
        return cls(str(uuid.uuid4()), nome, preco, quantidade)
    
    def atualizar(self, nome=None, preco=None, quantidade=None):
        if nome:
            self.nome = nome
        if preco is not None:
            self.preco = preco
        if quantidade is not None:
            self.quantidade = quantidade

    def baixar_estoque(self, quantidade_baixa: int):
        if quantidade_baixa <= 0:
            raise ValueError("A quantidade para baixa deve ser maior que zero.")
        if quantidade_baixa > self.quantidade:
            raise ValueError("Quantidade para baixa maior que o estoque disponível.")
        self.quantidade -= quantidade_baixa

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            nome=data["nome"],
            preco=data["preco"],
            quantidade=data["quantidade"]
        )

    def __str__(self):
        return f"ID: {self.id}\nNome: {self.nome}\nPreço: R$ {self.preco:.2f}\nQuantidade: {self.quantidade}\n"
    
