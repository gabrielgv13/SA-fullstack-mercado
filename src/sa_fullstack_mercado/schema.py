"""Classes e objetos do sistema + criação de tabelas."""


class Produto:
    """Representa um produto no mercado."""

    def __init__(self, id: int, nome: str, marca: str, preco_unitario: float, quantidade: int):
        self.id = id
        self.nome = nome
        self.marca = marca
        self.preco_unitario = preco_unitario
        self.quantidade = quantidade

    def alterar_preco(self, novo_preco: float) -> None:
        """Altera o preço unitário do produto."""
        self.preco_unitario = novo_preco

    def alterar_quantidade(self, nova_quantidade: int) -> None:
        """Altera a quantidade em estoque do produto."""
        self.quantidade = nova_quantidade

    def calcular_preco(self, unidades: int) -> float:
        """Calcula o preço total para N unidades compradas."""
        return unidades * self.preco_unitario

    def __repr__(self) -> str:
        return f"Produto(id={self.id}, nome='{self.nome}', marca='{self.marca}', preco={self.preco_unitario}, qtd={self.quantidade})"


class Compra:
    """Representa uma compra (nota fiscal)."""

    def __init__(self, id: int, itens: dict, total_final: float):
        self.id = id
        # itens: {"produto_id": {"nome": str, "quantidade": int, "preco_unitario": float, "subtotal": float}}
        self.itens = itens
        self.total_final = total_final

    def __repr__(self) -> str:
        return f"Compra(id={self.id}, total={self.total_final}, itens={len(self.itens)})"


def init_schema(conn) -> None:
    """Cria as tabelas do banco de dados."""
    with conn.cursor() as cur:
        # Tabela de produtos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(200) NOT NULL,
                marca VARCHAR(200) NOT NULL,
                preco_unitario NUMERIC(10, 2) NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0
            );
        """)

        # Tabela de compras
        cur.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                id SERIAL PRIMARY KEY,
                itens JSONB NOT NULL,
                total_final NUMERIC(10, 2) NOT NULL
            );
        """)
