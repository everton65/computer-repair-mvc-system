from typing import List
from models.peca import Peca
from utils.json_manager import JsonManager

PECAS_FILE = "data/pecas.json"

class PecaController:
    def __init__(self):
        self.db = JsonManager(PECAS_FILE)

    def listar(self) -> List[Peca]:
        data = self.db.load_all()
        return [Peca.from_dict(d) for d in data]

    def cadastrar(self, nome: str, preco: float, quantidade: int) -> Peca:
        if preco < 0:
            raise ValueError("O preço não pode ser negativo.")
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")

        nova = Peca.nova(nome, preco, quantidade)
        self.db.add(nova.to_dict())
        return nova

    def atualizar(self, id_peca: str, nome=None, preco=None, quantidade=None) -> bool:
        pecas = self.listar()
        for p in pecas:
            if p.id == id_peca:
                p.atualizar(nome, preco, quantidade)
                self.db.update(p.id, p.to_dict())
                return True
        return False

    def deletar(self, id_peca: str) -> bool:
        return self.db.delete(id_peca)

    def buscar_por_nome(self, termo: str) -> List[Peca]:
        termo = termo.lower().strip()
        return [p for p in self.listar() if termo in p.nome.lower()]

    def baixar_estoque(self, id_peca: str, quantidade: int) -> bool:
        pecas = self.listar()
        for p in pecas:
            if p.id == id_peca:
                p.baixar_estoque(quantidade)
                self.db.update(p.id, p.to_dict())
                return True
        return False

    def mostrar_todas(self) -> None:
        pecas = self.listar()
        if not pecas:
            print("Nenhuma peça cadastrada.")
            return

        print("\n=== LISTA DE PEÇAS ===")
        for p in pecas:
            print(p)
        print("======================\n")
