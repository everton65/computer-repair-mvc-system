from controllers.cliente_controller import ClienteController

class ClienteView:
    def __init__(self):
        self.controller = ClienteController()

    def exibir_menu(self):
        while True:
            print("\n===== MENU CLIENTES =====")
            print("1. Cadastrar cliente")
            print("2. Listar clientes")
            print("3. Buscar cliente por nome")
            print("4. Atualizar cliente")
            print("5. Remover cliente")
            print("0. Voltar ao menu principal")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.cadastrar_cliente()
            elif opcao == "2":
                self.controller.mostrar_todos()
            elif opcao == "3":
                self.buscar_cliente()
            elif opcao == "4":
                self.atualizar_cliente()
            elif opcao == "5":
                self.remover_cliente()
            elif opcao == "0":
                break
            else:
                print("Opção inválida, tente novamente.")

    def cadastrar_cliente(self):
         print("\n--- CADASTRO DE CLIENTE ---")
         nome = input("Nome: ").strip()
         telefone = input("Telefone: ").strip()
         email = input("E-mail: ").strip()

         try:
             cliente = self.controller.cadastrar(nome, telefone, email)
             print(f"Cliente '{cliente.nome}' cadastrado com sucesso!")
         except ValueError as e:
             print(f"Erro: {e}")       

    def buscar_cliente(self):
        termo = input("\nDigite o nome para busca: ").strip()
        resultados = self.controller.buscar_por_nome(termo)
        if resultados:
            print("\n=== RESULTADOS ===")
            for c in resultados:
                print(c)
        else:
            print("Nenhum cliente encontrado com esse nome.")
    
    def atualizar_cliente(self):
        id_cliente = input("Digite o ID do cliente a atualizar: ").strip()
        nome = input("Novo nome (deixe vazio para manter): ").strip() or None
        telefone = input("Novo telefone (deixe vazio para manter): ").strip() or None
        email = input("Novo e-mail (deixe vazio para manter): ").strip() or None

        if self.controller.atualizar(id_cliente, nome, telefone, email):
            print("Cliente atualizado com sucesso!")
        else:
            print("Cliente não encontrado!")

    def remover_cliente(self):
        id_cliente = input("Digite o ID do cliente para remover: ").strip()
        if self.controller.deletar(id_cliente):
            print("Cliente removido com sucesso!")
        else:
            print("Cliente não encontrado!")

