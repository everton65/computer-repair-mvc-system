from typing import List
from models.cliente import cliente
from utils.json_manager import JsonManager

CLIENTES_FILE = "data/clientes.json"

class ClienteController:
    def __init__(self):
        self.db = JsonManager(CLIENTES_FILE)

    def listar(self) -> List[cliente]:
        data = self.db.load_all()
        return [cliente.from_dict(d) for d in data]

    def cadastrar(self, nome: str, telefone: str, email: str) -> cliente:
        if not cliente.validar_email(email):
            raise ValueError("E-mail inválido.")
        if not cliente.validar_telefone(telefone):
            raise ValueError("Telefone inválido.")    
        
        novo = cliente.novo(nome, telefone, email)
        self.db.add(novo.to_dict())
        return novo
    
    def atualizar(self, id_cliente: str, nome=None, telefone=None, email=None) -> bool:
         clientes = self.listar()
         for c in clientes:
            if c.id == id_cliente:
                c.atualizar(nome, telefone, email)
                self.db.update(c.id, c.to_dict())
                return True
         return False
    
    def deletar(self, id_cliente: str) -> bool:
        return self.db.delete(id_cliente)
    
    def buscar_por_nome(self, termo: str) -> List[cliente]:
        termo = termo.lower().strip()
        return [c for c in self.listar() if termo in c.nome.lower()]
    
    def mostrar_todos(self) -> None:
        clientes = self.listar()
        if not clientes:
            print("Nenhum cliente cadastrado.")
            return
        print("\n=== LISTA DE CLIENTES ===")
        for c in clientes:
            print(c)
        print("=========================\n")

