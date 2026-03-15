from utils.json_manager import JsonManager
from models.servico import Servico
from models.peca import Peca

SERVICOS_FILE = "data/servicos.json"
PECAS_FILE = "data/pecas.json"

class RelatorioController:
    def __init__(self):
        self.db_servicos = JsonManager(SERVICOS_FILE)
        self.db_pecas = JsonManager(PECAS_FILE)

    def servicos_prontos_para_retirada(self):
        data = self.db_servicos.load_all()
        return [Servico.from_dict(s) for s in data if s.get("status") == "Pronto para retirada"]

    def pecas_com_estoque_baixo(self, limite: int = 5):
        data = self.db_pecas.load_all()
        return [Peca.from_dict(p) for p in data if p.get("quantidade", 0) < limite]
