from controllers.relatorio_controller import RelatorioController

class RelatorioView:
    def __init__(self):
        self.controller = RelatorioController()

    def exibir_menu(self):
        while True:
            print("""
=== MENU DE RELATÓRIOS ===
1. Serviços prontos para retirada
2. Peças com estoque baixo
0. Voltar
""")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.exibir_servicos_prontos()
            elif opcao == "2":
                self.exibir_pecas_baixo_estoque()
            elif opcao == "0":
                break
            else:
                print("Opção inválida, tente novamente.")

    def exibir_servicos_prontos(self):
        print("\n=== SERVIÇOS PRONTOS PARA RETIRADA ===")
        servicos = self.controller.servicos_prontos_para_retirada()
        if not servicos:
            print("Nenhum serviço pronto para retirada.")
        else:
            for s in servicos:
                print(f"ID: {s.id} | Cliente: {s.cliente_id} | "
                      f"Descrição: {s.descricao} | Valor: R${s.valor:.2f} | Status: {s.status}")
        print("=========================================\n")

    def exibir_pecas_baixo_estoque(self):
        print("\n=== PEÇAS COM ESTOQUE BAIXO (MENOS DE 5) ===")
        pecas = self.controller.pecas_com_estoque_baixo()
        if not pecas:
            print("Nenhuma peça com estoque baixo.")
        else:
            for p in pecas:
                print(f"ID: {p.id} | Nome: {p.nome} | Quantidade: {p.quantidade} | Preço: R${p.preco:.2f}")
        print("==============================================\n")
