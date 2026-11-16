
# 📚 Catálogo Pessoal de Materiais de Estudo

Projeto desenvolvido em Python para a atividade da **Neps Academy**.

O objetivo é criar um sistema de catálogo que permita cadastrar, consultar e atualizar materiais de estudo, mantendo as informações salvas entre diferentes execuções.

## Funcionalidades

- **Cadastro:** adiciona novos materiais com identificadores únicos.
- **Listagem:** apresenta todos os materiais cadastrados.
- **Localização:** encontra materiais pelo identificador.
- **Alteração:** permite modificar o nome, a quantidade ou ambos.
- **Persistência:** salva e recupera os dados utilizando um arquivo JSON.

## Tecnologias utilizadas

- Python 3
- JSON
- Biblioteca padrão do Python

## Estrutura dos arquivos

```text
catalogo-pessoal-python/
│
├── main.py
├── instructions.txt
└── README.md
```

O arquivo `catalogo.json` é criado automaticamente durante a execução, quando os dados são salvos pela primeira vez.

## Como executar

É necessário ter o Python 3 instalado.

No terminal, acesse a pasta do projeto e execute:

```bash
python3 main.py
```

No Windows:

```bash
python main.py
```

## Armazenamento

Os dados são armazenados em `catalogo.json`, utilizando o formato JSON.

O programa carrega os registros existentes ao iniciar e permite salvar as alterações ao selecionar a opção **Salvar e sair**.

## Regras do catálogo

- Cada material possui identificador, nome e quantidade.
- Os identificadores são únicos e gerados automaticamente.
- A quantidade deve ser um número inteiro não negativo.
- A quantidade zero é permitida.
- Alterar um material não modifica os demais.

---

**Projeto acadêmico — Neps Academy**

Desenvolvido em Python.
