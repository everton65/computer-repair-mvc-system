from database.connection import SessionLocal
from backend.models.cliente import Cliente
from backend.models.servico import Servico
from backend.models.peca import Peca


class RelatorioController:

    def relatorio_clientes(self):

        db = SessionLocal()

        clientes = db.query(Cliente).all()

        db.close()

        return clientes


    def relatorio_servicos(self):

        db = SessionLocal()

        servicos = db.query(Servico).all()

        db.close()

        return servicos


    def relatorio_pecas(self):

        db = SessionLocal()

        pecas = db.query(Peca).all()

        db.close()

        return pecas