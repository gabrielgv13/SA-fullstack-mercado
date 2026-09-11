"""População inicial do banco de dados via requisições POST aos endpoints."""


def seed_data(app, conn):
    """Popula o banco via POST nos endpoints, simulando uso manual da interface.

    Args:
        app: Instância da aplicação Flask (necessária para test_client e url_for).
        conn: Conexão psycopg ativa com o banco de dados.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM produtos;")
        if cur.fetchone()[0] > 0:
            return  # Já possui dados, não semear novamente

    with app.test_client() as client:
        # Cadastrar 5 produtos via POST /produtos/cadastrar
        produtos_seed = [
            {"nome": "Arroz", "marca": "Tio João", "preco_unitario": "5.49", "quantidade": "100"},
            {"nome": "Feijão", "marca": "Camil", "preco_unitario": "8.99", "quantidade": "80"},
            {"nome": "Macarrão", "marca": "Barilla", "preco_unitario": "4.29", "quantidade": "60"},
            {"nome": "Leite", "marca": "Piracanjuba", "preco_unitario": "4.59", "quantidade": "120"},
            {"nome": "Café", "marca": "Pilão", "preco_unitario": "12.90", "quantidade": "50"},
        ]
        for produto in produtos_seed:
            client.post("/produtos/cadastrar", data=produto)

        # Criar 2 compras via POST /compra/criar
        # Compra 1: Arroz (id=1) x2 + Leite (id=4) x3
        client.post("/compra/criar", data={
            "qtd_1": "2", "qtd_2": "0", "qtd_3": "0", "qtd_4": "3", "qtd_5": "0",
        })

        # Compra 2: Feijão (id=2) x1 + Macarrão (id=3) x4 + Café (id=5) x1
        client.post("/compra/criar", data={
            "qtd_1": "0", "qtd_2": "1", "qtd_3": "4", "qtd_4": "0", "qtd_5": "1",
        })
