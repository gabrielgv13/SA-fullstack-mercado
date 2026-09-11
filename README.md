# 🛒 Caixa Eletrônico do Mercado — Atividade Prática

Atividade prática para a turma de **Técnico em Desenvolvimento de Sistemas**. O projeto é um sistema de caixa de supermercado com cadastro de produtos, criação de compras e emissão de nota fiscal.

> **O que você vai praticar:** Lógica de Backend — processamento dos dados recebidos dos formulários e queries SQL no PostgreSQL.
>
> **O que NÃO é necessário saber:** HTML, Jinja2, Flask, rotas ou requisições HTTP. Tudo isso já está pronto.

## Tecnologias

- **Flask** — framework web (já configurado)
- **HTML puro** — templates prontos (não é preciso alterar)
- **pgembed** — PostgreSQL embarcado (similar ao SQLite)
- **psycopg** — driver PostgreSQL
- **uv** — gerenciador de pacotes e execução

## Estrutura do Projeto

```
src/sa_fullstack_mercado/
├── __init__.py                  # Ponto de entrada CLI + expõe a app Flask
├── aplicacao.py                 # Rotas da aplicação (⚠️ CONTÉM TODOs PARA VOCÊ)
├── banco_de_dados.py            # Funções CRUD do banco (⚠️ CONTÉM TODOs PARA VOCÊ)
├── modelos.py                   # Classes Produto e Compra + criação de tabelas (PRONTO)
├── popular_dados_iniciais.py    # Popula o banco com dados de teste (PRONTO)
└── templates/                   # Páginas HTML (PRONTAS — não altere)
    ├── base.html                # Layout base com navegação
    ├── index.html               # Lista de produtos e compras
    ├── cadastrar_produto.html   # Formulário de cadastro
    ├── criar_compra.html        # Seleção de produtos para compra
    └── nota_fiscal.html         # Exibição da nota fiscal
```

## 📝 O Que Você Deve Implementar

Os arquivos `aplicacao.py` e `banco_de_dados.py` possuem comentários marcados com `TODO` e `pass`. Cada `TODO` contém um enunciado explicando exatamente o que deve ser feito. Substitua o `pass` pelo código correspondente.

### Em `aplicacao.py` — Lógica de Processamento

Você vai implementar a **lógica de backend** dentro das rotas que já estão definidas:

- **Cadastrar produto:** criar um objeto `Produto` com os dados do formulário, salvar no banco e redirecionar para a página inicial.
- **Criar compra:** percorrer os produtos, calcular subtotais, montar o dicionário de itens, atualizar o estoque e registrar a compra no banco.

> 💡 Dica: os dados do formulário já são extraídos para variáveis (`nome`, `marca`, `preco_unitario`, etc.). Você só precisa usar essas variáveis na lógica.

### Em `banco_de_dados.py` — Queries SQL

Você vai escrever as **queries SQL** dentro de cada função CRUD:

- `inserir_produto` — INSERT com RETURNING
- `listar_produtos` — SELECT ordenado por id
- `buscar_produto` — SELECT com WHERE por id
- `atualizar_preco` — UPDATE do preço unitário
- `atualizar_quantidade` — UPDATE da quantidade em estoque
- `inserir_compra` — INSERT com JSONB e RETURNING
- `buscar_compra` — SELECT com WHERE por id
- `listar_compras` — SELECT ordenado por id

> 💡 Dica: use `%s` como placeholder nos parâmetros e passe os valores como tupla. Exemplo: `cur.execute("SELECT * FROM tabela WHERE id = %s", (valor_id,))`

## Classes Disponíveis (modelos.py)

A classe `Produto` possui os métodos:
- `calcular_preco(unidades)` → retorna `unidades × preco_unitario`
- `alterar_preco(novo_preco)` — altera o preço unitário
- `alterar_quantidade(nova_quantidade)` — altera o estoque

A classe `Compra` armazena: `id`, dicionário de `itens` e `total_final`.

## ✅ Checklist de Funcionalidades

O programa só vai funcionar corretamente quando **todos** os itens abaixo estiverem implementados. Use esta lista para acompanhar seu progresso:

### Queries SQL (`banco_de_dados.py`)

- [ ] `inserir_produto` — insere um produto na tabela `produtos` e retorna o ID gerado
- [ ] `listar_produtos` — seleciona todos os produtos ordenados por ID
- [ ] `buscar_produto` — seleciona um produto filtrando pelo ID
- [ ] `atualizar_preco` — atualiza o preço unitário de um produto pelo ID
- [ ] `atualizar_quantidade` — atualiza a quantidade em estoque de um produto pelo ID
- [ ] `inserir_compra` — insere uma compra (itens em JSONB + total) e retorna o ID gerado
- [ ] `buscar_compra` — seleciona uma compra filtrando pelo ID
- [ ] `listar_compras` — seleciona todas as compras ordenadas por ID

### Lógica de Backend (`aplicacao.py`)

- [ ] `cadastrar_produto` — cria um objeto `Produto` com os dados do formulário e salva no banco
- [ ] `criar_compra` (dentro do loop) — calcula subtotal, monta o dicionário de itens, soma ao total e atualiza o estoque
- [ ] `criar_compra` (após o loop) — chama a função que insere a compra no banco e guarda o ID retornado

### Teste Final

- [ ] O servidor inicia sem erros (`uv run sa-fullstack-mercado`)
- [ ] A página inicial lista os 5 produtos cadastrados automaticamente
- [ ] É possível cadastrar um novo produto pelo formulário
- [ ] É possível criar uma compra selecionando quantidades
- [ ] A nota fiscal exibe os itens e o total correto
- [ ] O estoque dos produtos diminui após uma compra

---

## 🧠 Passo a Passo: Como Pensar na Solução

### Parte 1 — Comece pelas Queries SQL

As funções de `banco_de_dados.py` são independentes entre si. Você pode implementar em qualquer ordem, mas a sugestão é começar pelas mais simples:

1. **`listar_produtos`** — Pense: "quero todas as linhas da tabela `produtos`, em ordem". Qual comando SQL faz isso? Quais colunas preciso retornar?
2. **`buscar_produto`** — Igual ao anterior, mas com um filtro. Como filtro por um valor específico em SQL? Lembre-se de usar `%s` como placeholder.
3. **`inserir_produto`** — Preciso adicionar uma linha nova. Qual comando SQL faz inserção? Como faço para o banco me devolver o ID que ele acabou de gerar?
4. **`atualizar_preco` e `atualizar_quantidade`** — Preciso modificar uma linha existente. Qual comando SQL altera dados? Como garanto que só a linha certa será alterada?
5. **`inserir_compra`** — Similar a `inserir_produto`, mas um dos campos é um JSON (já convertido para string pela função). O raciocínio é o mesmo: inserir e retornar o ID.
6. **`buscar_compra` e `listar_compras`** — Mesma lógica de `buscar_produto` e `listar_produtos`, mas na tabela `compras`.

> 💡 **Dica geral:** Cada `cur.execute(""" """)` recebe dois argumentos: a string SQL e uma tupla com os parâmetros. Se não houver parâmetros, passe apenas a string.

### Parte 2 — Depois vá para a Lógica de Backend

Com as queries funcionando, abra `aplicacao.py`:

#### Cadastrar Produto

1. Os dados do formulário já estão nas variáveis `nome`, `marca`, `preco_unitario` e `quantidade`.
2. Pense: como crio um objeto usando uma classe que já existe? Olhe a classe `Produto` em `modelos.py` — quais argumentos o construtor recebe?
3. Depois de criar o objeto, pense: qual função de `banco_de_dados.py` salva um produto? Quais argumentos ela precisa?
4. O redirecionamento já está pronto — você só precisa garantir que o produto foi salvo antes dele executar.

#### Criar Compra

1. O loop já percorre todos os produtos e extrai a quantidade desejada de cada um.
2. Pense: se a quantidade for zero, devo fazer algo? E se for maior que zero?
3. Para cada produto comprado, preciso calcular quanto custa aquela quantidade. A classe `Produto` já tem um método para isso — qual é?
4. Preciso guardar as informações de cada item comprado. O dicionário `itens` já está criado — como adiciono uma nova entrada nele?
5. Preciso acumular o valor total. A variável `total_final` já existe — como somo um valor a ela?
6. O estoque precisa diminuir. Pense: quanto tinha antes, quanto foi comprado, quanto sobra? Qual função de `banco_de_dados.py` atualiza a quantidade?
7. Após o loop, a chamada para salvar a compra já tem um espaço marcado. Qual função de `banco_de_dados.py` insere uma compra? O que ela retorna?

> 💡 **Dica geral:** Não tente resolver tudo de uma vez. Implemente uma coisa, teste, e só depois vá para a próxima. Se o servidor der erro, leia a mensagem — ela geralmente diz exatamente onde está o problema.

---

## Como Executar

```bash
# Instalar dependências
uv sync

# Rodar a aplicação
uv run sa-fullstack-mercado
```

Acesse `http://localhost:5000` no navegador.

## Dados Iniciais

Na primeira execução, o sistema popula automaticamente o banco com **5 produtos** e **2 compras** de exemplo. Os dados persistem no diretório `data_mercado/` entre reinicializações.