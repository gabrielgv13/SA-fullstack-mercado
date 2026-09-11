# 🛒 Caixa Eletrônico do Mercado

Sistema simples de caixa de supermercado com cadastro de produtos, criação de compras e emissão de nota fiscal.

## Tecnologias

- **Flask** — framework web
- **HTML puro** — templates sem CSS
- **pgembed** — PostgreSQL embarcado (similar ao SQLite)
- **psycopg** — driver PostgreSQL
- **uv** — gerenciador de pacotes e execução

## Estrutura do Projeto

```
src/sa_fullstack_mercado/
├── __init__.py       # Entry point CLI + expõe a app Flask
├── app.py            # Rotas e lógica de requisições
├── db.py             # Funções CRUD e ciclo de vida do pgembed
├── schema.py         # Classes Produto/Compra + criação de tabelas
├── population.py     # Seed de dados via POST nos endpoints
└── templates/
    ├── base.html              # Layout base com navegação
    ├── index.html             # Lista de produtos e compras
    ├── cadastrar_produto.html # Formulário de cadastro
    ├── criar_compra.html      # Seleção de produtos para compra
    └── nota_fiscal.html       # Exibição da nota fiscal
```

## Funcionalidades

### Cadastrar Produto
Formulário com os campos: **nome**, **marca**, **preço unitário** e **quantidade**. O `id` é gerado automaticamente (auto-increment).

A classe `Produto` possui os métodos:
- `alterar_preco(novo_preco)` — altera o preço unitário
- `alterar_quantidade(nova_qtd)` — altera o estoque
- `calcular_preco(unidades)` — retorna `unidades × preço_unitário`

### Criar Compra
Exibe todos os produtos disponíveis com campos de quantidade. Ao finalizar:
- Calcula subtotais usando `Produto.calcular_preco()`
- Deduz o estoque automaticamente
- Gera uma nota fiscal com itens detalhados e total final

A classe `Compra` armazena: `id` (auto-increment), dicionário de itens (produto, quantidade, preço unitário, subtotal) e total final.

## Como Executar

```bash
# Instalar dependências
uv sync

# Rodar a aplicação
uv run flask --app sa_fullstack_mercado.app run

# Ou via entry point
uv run sa-fullstack-mercado
```

Acesse `http://localhost:5000` no navegador.

## Dados Iniciais

Na primeira execução, o sistema popula automaticamente o banco com **5 produtos** e **2 notas fiscais** de exemplo, simulando requisições POST pelos próprios endpoints da aplicação. Os dados persistem no diretório `data_mercado/` entre reinicializações.