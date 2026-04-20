from sqlalchemy.orm import Session
from backend.models.ordem_servico import OrdemServico
from backend.models.ordem_servico_item import OrdemServicoItem


class OSController:

    # ===============================
    # LISTAR ORDENS
    # ===============================
    def listar(self, db: Session):
        return db.query(OrdemServico).all()

    # ===============================
    # BUSCAR POR ID
    # ===============================
    def buscar_por_id(self, db: Session, ordem_id: str):
        return db.query(OrdemServico).filter(OrdemServico.id == ordem_id).first()

    # ===============================
    # CRIAR ORDEM (COM ITENS)
    # ===============================
    def criar(self, db: Session, data):

        # cria ordem primeiro
        nova_ordem = OrdemServico(
            cliente_id=data.cliente_id,
            status="aberta",
            valor=0.0
        )

        db.add(nova_ordem)
        db.commit()
        db.refresh(nova_ordem)

        total = 0

        # adiciona os itens (serviços)
        for item in data.itens:

            novo_item = OrdemServicoItem(
                ordem_id=nova_ordem.id,
                descricao=item.descricao,
                valor=item.valor
            )

            total += item.valor

            db.add(novo_item)

        # atualiza valor total da ordem
        nova_ordem.valor = total

        db.commit()
        db.refresh(nova_ordem)

        return nova_ordem

    # ===============================
    # DELETAR ORDEM
    # ===============================
    def deletar(self, db: Session, ordem_id: str):

        ordem = self.buscar_por_id(db, ordem_id)

        if not ordem:
            return False

        db.delete(ordem)
        db.commit()

        return True