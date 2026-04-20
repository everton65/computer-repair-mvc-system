from fastapi import HTTPException
from database.connection import SessionLocal
from backend.models.cliente import Cliente


class ClienteController:

    def listar(self):

        db = SessionLocal()

        clientes = db.query(Cliente).all()

        db.close()

        return clientes


    def cadastrar(self, nome, telefone, email):

        if not Cliente.validar_email(email):
            raise HTTPException(status_code=400, detail="Email inválido")

        if not Cliente.validar_telefone(telefone):
            raise HTTPException(status_code=400, detail="Telefone inválido")

        db = SessionLocal()

        novo_cliente = Cliente(
            nome=nome,
            telefone=telefone,
            email=email
        )

        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)

        db.close()

        return novo_cliente


    def atualizar(self, cliente_id, nome=None, telefone=None, email=None):

        db = SessionLocal()

        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

        if not cliente:
            db.close()
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        if nome:
            cliente.nome = nome

        if telefone:
            cliente.telefone = telefone

        if email:
            cliente.email = email

        db.commit()
        db.refresh(cliente)

        db.close()

        return cliente


    def deletar(self, cliente_id):

        db = SessionLocal()

        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

        if not cliente:
            db.close()
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        db.delete(cliente)
        db.commit()

        db.close()

        return {"message": "Cliente removido"}