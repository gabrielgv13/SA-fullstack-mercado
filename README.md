# SA-fullstack-mercado

Prompt:
Crie um projeto simples de sistema de caixa eletrônico de mercado, utilizando Flask, html puro (sem css), pgembed (fork da biblioteca pgserver, similar ao sqlite, banco de dados integrado) e psycopg como bibliotecas, para instalação das bibliotecas utilize o "uv add". Separe a lógica em 3 arquivos: db.py (funções que manipulam o banco de dados pgembed), app.py (rotas e lógica de extração de dados) e schema.py (classe e objetos + criação de alguns produtos e notas fiscais já feitas). Mais instruções de funcionalides estão localizadas no arquivo README.MD .

Funcionalidades:
Cadastrar Produto (Via formulário) - Requer os campos:
id - auto increment (sem interação com usuário), nome, marca, preço unitário, quantidade
Cria um objeto para este produto.
Cada objeto produto deve possuir os seguintes métodos:
Alterar preço, Alterar Quantidade, Calculo de preco (recebe uma unidades compradas como parametro, retorna a multiplicação de unidades compradas pelo preço do próprio objeto).

Criar compra:
Seleciona produtos por lista ou id e então seleciona quantidade de unidades.
Ao terminar de selecionar produtos, cria um objeto compra
com os seguintes campos:
id (autoincrement), dicionário com produtos + quantidade do produto + preço total, total final da compra. Mostra na tela a "nota fiscal".

Utilizando o pgembed + psycopg:

import pgembed
import psycopg

server = pgembed.get_server("./meu_banco_dados")
server.start()

try:
    with psycopg.connect(server.get_uri(), autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            print(cur.fetchone())
finally:
    # Garante que o banco fecha mesmo se ocorrer um erro acima
    server.stop()

pgembed.get_server("./pasta"): Inicializa o ciclo de vida. Se o diretório estiver vazio, ele roda o initdb do PostgreSQL por baixo dos panos e escolhe uma porta de rede aleatória que esteja livre no seu sistema operacional.server.get_uri(): Retorna a string de conexão exata (geralmente algo como postgresql://postgres@127.0.0.1:PORTA/postgres), permitindo que você conecte qualquer driver de mercado, como o psycopg.server.stop(): Finaliza os processos em segundo plano do PostgreSQL de maneira limpa.