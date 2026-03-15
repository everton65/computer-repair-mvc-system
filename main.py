from views.cliente_view import ClienteView
from views.servico_view import ServicosView
from views.peca_view import PecaView
from views.relatorio_view import RelatorioView

def main_menu():
    while True:
        print("\n===== CLEITINHO TI - MENU PRINCIPAL =====")
        print("1. Clientes")
        print("2. Serviços")
        print("3. Peças / Estoque")
        print("4. Relatórios")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            ClienteView().exibir_menu()
        elif opcao == "2":
            ServicosView().exibir_menu()
        elif opcao == "3":
            PecaView().exibir_menu()
        elif opcao == "4":
            RelatorioView().exibir_menu()
        elif opcao == "0":
            print("Saindo... até mais, Cleitinho!")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main_menu()