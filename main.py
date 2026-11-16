
import json
import os
import tempfile

ARQUIVO_DADOS = "catalogo.json"


def validar_catalogo(dados):
    """Verifica se todos os registros possuem dados válidos."""

    if not isinstance(dados, list):
        return False

    identificadores = set()

    for item in dados:
        if not isinstance(item, dict):
            return False

        identificador = item.get("id")
        nome = item.get("nome")
        quantidade = item.get("quantidade")

        if type(identificador) is not int or identificador <= 0:
            return False

        if identificador in identificadores:
            return False

        if not isinstance(nome, str) or not nome.strip():
            return False

        if type(quantidade) is not int or quantidade < 0:
            return False

        identificadores.add(identificador)

    return True


def carregar_catalogo():
    """Carrega e valida os dados armazenados."""

    if not os.path.exists(ARQUIVO_DADOS):
        return [], True

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        print("\nERRO: Não foi possível ler o arquivo do catálogo.")
        print("O arquivo original será preservado.")
        return [], False

    if not validar_catalogo(dados):
        print("\nERRO: O arquivo contém registros inválidos.")
        print("O arquivo original será preservado.")
        return [], False

    print(f"\n{len(dados)} material(is) carregado(s) com sucesso.")

    return dados, True


def salvar_catalogo(catalogo, permissao_salvar):
    """Salva os dados sem substituir o arquivo em caso de falha."""

    if not permissao_salvar:
        print("\nERRO: O salvamento foi bloqueado.")
        print("O arquivo original não será substituído.")
        return False

    if not validar_catalogo(catalogo):
        print("\nERRO: Os dados do catálogo são inválidos.")
        print("O arquivo original foi preservado.")
        return False

    diretorio = os.path.dirname(os.path.abspath(ARQUIVO_DADOS))
    arquivo_temporario = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=diretorio,
            prefix=".catalogo_",
            suffix=".tmp",
            delete=False
        ) as arquivo:
            arquivo_temporario = arquivo.name

            json.dump(
                catalogo,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

            arquivo.flush()
            os.fsync(arquivo.fileno())

        os.replace(arquivo_temporario, ARQUIVO_DADOS)

        print("\nCatálogo salvo com sucesso!")
        return True

    except OSError:
        print("\nERRO: Não foi possível salvar o catálogo.")
        print("O arquivo original foi preservado.")
        return False

    finally:
        if arquivo_temporario and os.path.exists(arquivo_temporario):
            try:
                os.remove(arquivo_temporario)
            except OSError:
                pass


def gerar_identificador(catalogo):
    """Gera um identificador único."""

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

    print("\nMaterial cadastrado com sucesso!")
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

    item_encontrado = None

    for item in catalogo:
        if item["id"] == identificador:
            item_encontrado = item
            break

    if item_encontrado is None:
        print("Material não encontrado.")
        return

    print("\nMaterial encontrado!")
    print(f"Nome: {item_encontrado['nome']}")
    print(f"Quantidade: {item_encontrado['quantidade']}")

    print("\nO que deseja alterar?")
    print("1 - Nome")
    print("2 - Quantidade")
    print("3 - Nome e quantidade")

    opcao = input("\nEscolha: ").strip()

    if opcao not in ("1", "2", "3"):
        print("Opção inválida.")
        return

    # Os novos valores são preparados antes de modificar o item.
    novo_nome = item_encontrado["nome"]
    nova_quantidade = item_encontrado["quantidade"]

    if opcao in ("1", "3"):
        novo_nome = input("Novo nome: ").strip()

        if not novo_nome:
            print("O nome não pode ficar vazio.")
            print("Nenhuma alteração foi realizada.")
            return

    if opcao in ("2", "3"):
        try:
            nova_quantidade = int(input("Nova quantidade: "))

            if nova_quantidade < 0:
                print("A quantidade não pode ser negativa.")
                print("Nenhuma alteração foi realizada.")
                return

        except ValueError:
            print("Digite uma quantidade inteira válida.")
            print("Nenhuma alteração foi realizada.")
            return

    # As alterações só acontecem depois de todas as validações.
    item_encontrado["nome"] = novo_nome
    item_encontrado["quantidade"] = nova_quantidade

    print("\nMaterial atualizado com sucesso!")


def menu():
    catalogo, permissao_salvar = carregar_catalogo()

    print("\n" + "=" * 40)
    print("   CATÁLOGO DE MATERIAIS DE ESTUDO")
    print("=" * 40)

    if not permissao_salvar:
        print("\nATENÇÃO: O arquivo original está protegido.")
        print("O catálogo não poderá ser salvo nesta execução.")

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
            if salvar_catalogo(catalogo, permissao_salvar):
                print("Até a próxima!")
                break

            if not permissao_salvar:
                print("\nSaindo sem modificar o arquivo original.")
                break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
