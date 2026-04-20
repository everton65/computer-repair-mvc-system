from fastapi import HTTPException
from database.connection import SessionLocal
from backend.models.peca import Peca


class PecaController:

    def listar(self):

        db = SessionLocal()

        pecas = db.query(Peca).all()

        db.close()

        return pecas


    def cadastrar(self, nome, preco, quantidade):

        db = SessionLocal()

        nova_peca = Peca(
            nome=nome,
            preco=preco,
            quantidade=quantidade
        )

        db.add(nova_peca)
        db.commit()
        db.refresh(nova_peca)

        db.close()

        return nova_peca


    def atualizar(self, peca_id, nome=None, preco=None, quantidade=None):

        db = SessionLocal()

        peca = db.query(Peca).filter(Peca.id == peca_id).first()

        if not peca:
            db.close()
            raise HTTPException(status_code=404, detail="Peça não encontrada")

        if nome:
            peca.nome = nome

        if preco:
            peca.preco = preco

        if quantidade:
            peca.quantidade = quantidade

        db.commit()
        db.refresh(peca)

        db.close()

        return peca


    def deletar(self, peca_id):

        db = SessionLocal()

        peca = db.query(Peca).filter(Peca.id == peca_id).first()

        if not peca:
            db.close()
            raise HTTPException(status_code=404, detail="Peça não encontrada")

        db.delete(peca)
        db.commit()

        db.close()

        return {"message": "Peça removida"}