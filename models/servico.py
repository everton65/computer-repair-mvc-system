import datetime

class Servico:
    def __init__(self, id, cliente_id, descricao, valor, status="Na bancada", data_registro=None):
        self.id = id
        self.cliente_id = cliente_id
        self.descricao = descricao
        self.valor = valor
        self.status = status
        self.data_registro = data_registro or datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "descricao": self.descricao,
            "valor": self.valor,
            "status": self.status,
            "data_registro": self.data_registro
        }

    @staticmethod
    def from_dict(data):
        return Servico(**data)

    def __str__(self):
        return (f"[{self.id}] Cliente ID: {self.cliente_id} | Desc: {self.descricao} | "
                f"R${self.valor:.2f} | Status: {self.status} | Criado em: {self.data_registro}")