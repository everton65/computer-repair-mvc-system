from controllers.servico_controller import ServicoController
from controllers.cliente_controller import ClienteController

class ServicosView:
    def __init__(self):
        self.controller = ServicoController()
        self.clientes = ClienteController()

    def exibir_menu(self):
        while True:
            print("\n===== MENU SERVIÇOS =====")
            print("1. Cadastrar serviço")
            print("2. Listar serviços")
            print("3. Buscar por cliente")
            print("4. Atualizar status do serviço")
            print("0. Voltar")

            opcao = input("Escolha uma opção: ").strip()
            if opcao == "1":
                self.cadastrar_servico()
            elif opcao == "2":
                self.listar_servicos()
            elif opcao == "3":
                self.buscar_por_cliente()
            elif opcao == "4":
                self.atualizar_status()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")

    def cadastrar_servico(self):
        print("\n--- CADASTRAR SERVIÇO ---")
        self.clientes.mostrar_todos()
        try:
            cliente_id = str(input("ID do cliente: "))
        except ValueError:
            print("ID inválido!")
            return

        descricao = input("Descrição do problema: ").strip()
        try:
            valor = float(input("Valor do serviço: R$ ").strip())
        except ValueError:
            print("Valor inválido!")
            return

        servico = self.controller.cadastrar(cliente_id, descricao, valor)
        print(f"Serviço #{servico.id} cadastrado com sucesso!")

    def listar_servicos(self):
        print("\n--- LISTA DE SERVIÇOS ---")
        servicos = self.controller.listar()
        if not servicos:
            print("Nenhum serviço cadastrado.")
            return
        for s in servicos:
            print(s)

    def buscar_por_cliente(self):
        print("\n--- BUSCAR SERVIÇOS POR CLIENTE ---")
        self.clientes.mostrar_todos()
        try:
            cliente_id = str(input("ID do cliente: "))
        except ValueError:
            print("ID inválido!")
            return

        servicos = self.controller.buscar_por_cliente(cliente_id)
        if not servicos:
            print("Nenhum serviço encontrado para este cliente.")
        else:
            for s in servicos:
                print(s)

    def atualizar_status(self):
        print("\n--- ATUALIZAR STATUS ---")
        self.listar_servicos()
        try:
            id_servico = int(input("ID do serviço: "))
        except ValueError:
            print("ID inválido!")
            return

        print("Escolha o novo status:")
        print("1. Na bancada")
        print("2. Aguardando peça")
        print("3. Pronto para retirada")
        print("4. Entregue")

        opcoes = {
            "1": "Na bancada",
            "2": "Aguardando peça",
            "3": "Pronto para retirada",
            "4": "Entregue"
        }

        opcao = input("Digite a opção: ").strip()
        novo_status = opcoes.get(opcao)
        if not novo_status:
            print("Status inválido!")
            return

        if self.controller.atualizar_status(id_servico, novo_status):
            print("Status atualizado com sucesso!")
        else:
            print("Serviço não encontrado.")
