"""Funções que manipulam o banco de dados pgembed."""

import json
import os
from pathlib import Path

import pgembed
from pgembed.postgres_server import PostgresServer
import psycopg

from .modelos import Produto, Compra

# Singleton do servidor pgembed
_servidor = None
_DIRETORIO_DADOS = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) / "data_mercado"


def obter_servidor_banco() -> PostgresServer:
    """Retorna a instância singleton do servidor pgembed."""
    global _servidor
    if _servidor is None:
        _servidor = pgembed.get_server(_DIRETORIO_DADOS, cleanup_mode=None)
    return _servidor


def iniciar_servidor() -> PostgresServer:
    """Inicializa o pgdata e inicia o servidor pgembed."""
    servidor = obter_servidor_banco()
    servidor.ensure_pgdata_inited()
    servidor.ensure_postgres_running()
    return servidor


def parar_servidor() -> None:
    """Para o servidor pgembed."""
    global _servidor
    if _servidor is not None:
        _servidor.cleanup()
        _servidor = None


def obter_conexao(servidor: PostgresServer):
    """Retorna uma conexão psycopg usando a URI do servidor."""
    return psycopg.connect(servidor.get_uri(), autocommit=True)


# --- CRUD Produtos ---

def inserir_produto(conexao, nome: str, marca: str, preco_unitario: float, quantidade: int) -> int:
    """Insere um novo produto e retorna o ID gerado."""
    with conexao.cursor() as cur:
        # TODO: Insira um novo produto na tabela 'produtos' com os campos:
        #       nome, marca, preco_unitario e quantidade.
        #       Use RETURNING id para retornar o ID gerado automaticamente.
        #       Os parâmetros devem ser passados como tupla: (nome, marca, preco_unitario, quantidade)
        cur.execute("""   """)
        return cur.fetchone()[0]


def listar_produtos(conexao) -> list[Produto]:
    """Retorna todos os produtos como lista de objetos Produto."""
    with conexao.cursor() as cur:
        # TODO: Selecione todos os produtos da tabela 'produtos', ordenados por id.
        #       Retorne as colunas: id, nome, marca, preco_unitario, quantidade.
        cur.execute("""   """)
        linhas = cur.fetchall()
        return [Produto(id=linha[0], nome=linha[1], marca=linha[2], preco_unitario=float(linha[3]), quantidade=linha[4]) for linha in linhas]


def buscar_produto(conexao, produto_id: int) -> Produto | None:
    """Busca um produto por ID. Retorna None se não encontrado."""
    with conexao.cursor() as cur:
        # TODO: Busque um produto pelo seu ID na tabela 'produtos'.
        #       Retorne as colunas: id, nome, marca, preco_unitario, quantidade.
        #       Filtre usando WHERE id = %s passando (produto_id,) como parâmetro.
        cur.execute("""   """)
        linha = cur.fetchone()
        if linha is None:
            return None
        return Produto(id=linha[0], nome=linha[1], marca=linha[2], preco_unitario=float(linha[3]), quantidade=linha[4])


def atualizar_preco(conexao, produto_id: int, novo_preco: float) -> None:
    """Atualiza o preço unitário de um produto."""
    with conexao.cursor() as cur:
        # TODO: Atualize o preco_unitario de um produto na tabela 'produtos'.
        #       Filtre pelo id do produto.
        #       Parâmetros: (novo_preco, produto_id)
        cur.execute("""   """)


def atualizar_quantidade(conexao, produto_id: int, nova_quantidade: int) -> None:
    """Atualiza a quantidade em estoque de um produto."""
    with conexao.cursor() as cur:
        # TODO: Atualize a quantidade de um produto na tabela 'produtos'.
        #       Filtre pelo id do produto.
        #       Parâmetros: (nova_quantidade, produto_id)
        cur.execute("""   """)


# --- CRUD Compras ---

def inserir_compra(conexao, itens: dict, total_final: float) -> int:
    """Insere uma nova compra e retorna o ID gerado.
    
    itens: dict no formato {"produto_id": {"nome": str, "quantidade": int, "preco_unitario": float, "subtotal": float}}
    """
    itens_json = json.dumps(itens)
    with conexao.cursor() as cur:
        # TODO: Insira uma nova compra na tabela 'compras' com os campos:
        #       itens (JSONB) e total_final.
        #       Use RETURNING id para retornar o ID gerado automaticamente.
        #       Parâmetros: (itens_json, total_final)
        cur.execute("""   """)
        return cur.fetchone()[0]


def buscar_compra(conexao, compra_id: int) -> Compra | None:
    """Busca uma compra por ID. Retorna None se não encontrada."""
    with conexao.cursor() as cur:
        # TODO: Busque uma compra pelo seu ID na tabela 'compras'.
        #       Retorne as colunas: id, itens, total_final.
        #       Filtre usando WHERE id = %s passando (compra_id,) como parâmetro.
        cur.execute("""   """)
        linha = cur.fetchone()
        if linha is None:
            return None
        return Compra(id=linha[0], itens=linha[1], total_final=float(linha[2]))


def listar_compras(conexao) -> list[Compra]:
    """Retorna todas as compras como lista de objetos Compra."""
    with conexao.cursor() as cur:
        # TODO: Selecione todas as compras da tabela 'compras', ordenadas por id.
        #       Retorne as colunas: id, itens, total_final.
        cur.execute("""   """)
        linhas = cur.fetchall()
        return [Compra(id=linha[0], itens=linha[1], total_final=float(linha[2])) for linha in linhas]
