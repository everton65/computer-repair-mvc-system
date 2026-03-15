import os
import json
from models.servico import Servico

DATA_PATH = "data"
SERVICOS_FILE = os.path.join(DATA_PATH, "servicos.json")

class ServicoController:
    def __init__(self):
        os.makedirs(DATA_PATH, exist_ok=True)
        if not os.path.exists(SERVICOS_FILE):
            with open(SERVICOS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load(self):
        with open(SERVICOS_FILE, "r", encoding="utf-8") as f:
            return [Servico.from_dict(s) for s in json.load(f)]

    def _save(self, servicos):
        with open(SERVICOS_FILE, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in servicos], f, indent=2, ensure_ascii=False)

    def cadastrar(self, cliente_id, descricao, valor):
        servicos = self._load()
        novo_id = max([s.id for s in servicos], default=0) + 1
        servico = Servico(novo_id, cliente_id, descricao, valor)
        servicos.append(servico)
        self._save(servicos)
        return servico

    def listar(self):
        return self._load()

    def atualizar_status(self, id_servico, novo_status):
        servicos = self._load()
        for s in servicos:
            if s.id == id_servico:
                s.status = novo_status
                self._save(servicos)
                return True
        return False

    def buscar_por_cliente(self, cliente_id):
        return [s for s in self._load() if s.cliente_id == cliente_id]