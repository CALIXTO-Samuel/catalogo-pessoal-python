
import json
import os

ARQUIVO_DADOS = "catalogo.json"


def carregar_catalogo():
    """Carrega os materiais salvos no arquivo JSON."""
    if not os.path.exists(ARQUIVO_DADOS):
        return []

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if isinstance(dados, list):
            return dados

        print("Aviso: formato do catálogo inválido.")
        return []

    except (json.JSONDecodeError, OSError):
        print("Aviso: não foi possível carregar o catálogo.")
        return []


def salvar_catalogo(catalogo):
    """Salva todos os materiais no arquivo JSON."""
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(catalogo, arquivo, ensure_ascii=False, indent=4)

        return True

    except OSError:
        print("Erro ao salvar o catálogo.")
        return False


def gerar_identificador(catalogo):
    """Gera um identificador único para cada material."""
    identificadores = [
        item["id"] for item in catalogo
    ]

    return max(identificadores, default=0) + 1


def cadastrar_item(catalogo):
    print("\n--- CADASTRAR MATERIAL ---")

    nome = input("Nome do material: ").strip()

    if not nome:
        print("O nome não pode ficar vazio.")
        return

    try:
        quantidade = int(input("Quantidade: "))

        if quantidade < 0:
            print("A quantidade não pode ser negativa.")
            return

    except ValueError:
        print("Digite uma quantidade inteira válida.")
        return

    identificador = gerar_identificador(catalogo)

    item = {
        "id": identificador,
        "nome": nome,
        "quantidade": quantidade
    }

    catalogo.append(item)

    print(f"\nMaterial cadastrado com sucesso!")
    print(f"Identificador: {identificador}")


def listar_itens(catalogo):
    print("\n--- MATERIAIS CADASTRADOS ---")

    if not catalogo:
        print("O catálogo está vazio.")
        return

    for item in catalogo:
        print(f"\nIdentificador: {item['id']}")
        print(f"Nome: {item['nome']}")
        print(f"Quantidade: {item['quantidade']}")
        print("-" * 30)


def localizar_item(catalogo):
    print("\n--- LOCALIZAR MATERIAL ---")

    try:
        identificador = int(input("Identificador: "))
    except ValueError:
        print("Digite um identificador válido.")
        return

    for item in catalogo:
        if item["id"] == identificador:
            print("\nMaterial encontrado!")
            print(f"Identificador: {item['id']}")
            print(f"Nome: {item['nome']}")
            print(f"Quantidade: {item['quantidade']}")
            return

    print("Material não encontrado.")


def alterar_item(catalogo):
    print("\n--- ALTERAR MATERIAL ---")

    try:
        identificador = int(input("Identificador do material: "))
    except ValueError:
        print("Digite um identificador válido.")
        return

    for item in catalogo:
        if item["id"] == identificador:
            print("\nMaterial encontrado!")
            print(f"Nome: {item['nome']}")
            print(f"Quantidade: {item['quantidade']}")

            print("\nO que deseja alterar?")
            print("1 - Nome")
            print("2 - Quantidade")
            print("3 - Nome e quantidade")

            opcao = input("\nEscolha: ").strip()

            if opcao in ("1", "3"):
                novo_nome = input("Novo nome: ").strip()

                if not novo_nome:
                    print("O nome não pode ficar vazio.")
                    return

                item["nome"] = novo_nome

            if opcao in ("2", "3"):
                try:
                    nova_quantidade = int(
                        input("Nova quantidade: ")
                    )

                    if nova_quantidade < 0:
                        print("A quantidade não pode ser negativa.")
                        return

                    item["quantidade"] = nova_quantidade

                except ValueError:
                    print("Digite uma quantidade inteira válida.")
                    return

            if opcao not in ("1", "2", "3"):
                print("Opção inválida.")
                return

            print("\nMaterial atualizado com sucesso!")
            return

    print("Material não encontrado.")


def menu():
    catalogo = carregar_catalogo()

    print("=" * 40)
    print("   CATÁLOGO DE MATERIAIS DE ESTUDO")
    print("=" * 40)

    while True:
        print("\n1 - Cadastrar material")
        print("2 - Listar materiais")
        print("3 - Localizar material")
        print("4 - Alterar material")
        print("5 - Salvar e sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_item(catalogo)

        elif opcao == "2":
            listar_itens(catalogo)

        elif opcao == "3":
            localizar_item(catalogo)

        elif opcao == "4":
            alterar_item(catalogo)

        elif opcao == "5":
            if salvar_catalogo(catalogo):
                print("\nCatálogo salvo com sucesso!")
                print("Até a próxima!")
                break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
