from fastapi import HTTPException
from database.connection import SessionLocal
from backend.models.servico import Servico


class ServicoController:

    def listar(self):

        db = SessionLocal()

        servicos = db.query(Servico).all()

        resultado = []

        for s in servicos:
            resultado.append({
                "id": s.id,
                "descricao": s.descricao,
                "valor": s.valor,
                "cliente": s.cliente.nome if s.cliente else None
            })

        db.close()

        return resultado

    def cadastrar(self, descricao, valor, cliente_id):

        db = SessionLocal()

        novo_servico = Servico(
            descricao=descricao,
            valor=valor,
            cliente_id=cliente_id
        )

        db.add(novo_servico)
        db.commit()
        db.refresh(novo_servico)

        db.close()

        return novo_servico


    def deletar(self, servico_id):

        db = SessionLocal()

        servico = db.query(Servico).filter(Servico.id == servico_id).first()

        if not servico:
            db.close()
            raise HTTPException(status_code=404, detail="Serviço não encontrado")

        db.delete(servico)
        db.commit()

        db.close()

        return {"message": "Serviço removido"}