from controllers.peca_controller import PecaController

class PecaView:
    def __init__(self):
        self.controller = PecaController()

    def exibir_menu(self):
        while True:
            print("\n=== MENU DE PEÇAS ===")
            print("1 - Cadastrar nova peça")
            print("2 - Listar todas as peças")
            print("3 - Buscar peça por nome")
            print("4 - Atualizar peça")
            print("5 - Excluir peça")
            print("6 - Baixar estoque")
            print("0 - Voltar ao menu principal")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.cadastrar()
            elif opcao == "2":
                self.controller.mostrar_todas()
            elif opcao == "3":
                self.buscar_por_nome()
            elif opcao == "4":
                self.atualizar()
            elif opcao == "5":
                self.deletar()
            elif opcao == "6":
                self.baixar_estoque()
            elif opcao == "0":
                print("Voltando ao menu principal...")
                break
            else:
                print("Opção inválida. Tente novamente.")

    def cadastrar(self):
        nome = input("Nome da peça: ").strip()
        try:
            preco = float(input("Preço de custo (R$): "))
            quantidade = int(input("Quantidade em estoque: "))
            nova = self.controller.cadastrar(nome, preco, quantidade)
            print(f"Peça cadastrada com sucesso! ID: {nova.id}")
        except ValueError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def buscar_por_nome(self):
        termo = input("Digite o nome da peça para buscar: ").strip()
        pecas = self.controller.buscar_por_nome(termo)
        if not pecas:
            print("Nenhuma peça encontrada.")
            return
        print("\n=== RESULTADOS DA BUSCA ===")
        for p in pecas:
            print(p)

    def atualizar(self):
        id_peca = input("Digite o ID da peça para atualizar: ").strip()
        nome = input("Novo nome (ou Enter para manter): ").strip() or None
        preco_str = input("Novo preço (ou Enter para manter): ").strip()
        quantidade_str = input("Nova quantidade (ou Enter para manter): ").strip()

        preco = float(preco_str) if preco_str else None
        quantidade = int(quantidade_str) if quantidade_str else None

        sucesso = self.controller.atualizar(id_peca, nome, preco, quantidade)
        if sucesso:
            print("Peça atualizada com sucesso!")
        else:
            print("Peça não encontrada.")

    def deletar(self):
        id_peca = input("Digite o ID da peça para excluir: ").strip()
        if self.controller.deletar(id_peca):
            print("Peça excluída com sucesso!")
        else:
            print("Peça não encontrada.")

    def baixar_estoque(self):
        id_peca = input("Digite o ID da peça para baixar do estoque: ").strip()
        try:
            qtd = int(input("Quantidade a dar baixa: "))
            sucesso = self.controller.baixar_estoque(id_peca, qtd)
            if sucesso:
                print(f"Estoque atualizado com sucesso (-{qtd} unidades)!")
            else:
                print("Peça não encontrada.")
        except ValueError:
            print("Erro: Digite um número válido para a quantidade.")

