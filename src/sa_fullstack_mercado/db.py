"""Funções que manipulam o banco de dados pgembed."""

import json
import os
from pathlib import Path

import pgembed
from pgembed.postgres_server import PostgresServer
import psycopg

from .schema import Produto, Compra

# Singleton do servidor pgembed
_server = None
_DATA_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) / "data_mercado"


def get_db_server() -> PostgresServer:
    """Retorna a instância singleton do servidor pgembed."""
    global _server
    if _server is None:
        _server = pgembed.get_server(_DATA_DIR, cleanup_mode=None)
    return _server


def start_server() -> PostgresServer:
    """Inicializa o pgdata e inicia o servidor pgembed."""
    server = get_db_server()
    server.ensure_pgdata_inited()
    server.ensure_postgres_running()
    return server


def stop_server() -> None:
    """Para o servidor pgembed."""
    global _server
    if _server is not None:
        _server.cleanup()
        _server = None


def get_connection(server: PostgresServer):
    """Retorna uma conexão psycopg usando a URI do servidor."""
    return psycopg.connect(server.get_uri(), autocommit=True)


# --- CRUD Produtos ---

def inserir_produto(conn, nome: str, marca: str, preco_unitario: float, quantidade: int) -> int:
    """Insere um novo produto e retorna o ID gerado."""
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO produtos (nome, marca, preco_unitario, quantidade) VALUES (%s, %s, %s, %s) RETURNING id;",
            (nome, marca, preco_unitario, quantidade),
        )
        return cur.fetchone()[0]


def listar_produtos(conn) -> list[Produto]:
    """Retorna todos os produtos como lista de objetos Produto."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, nome, marca, preco_unitario, quantidade FROM produtos ORDER BY id;")
        rows = cur.fetchall()
        return [Produto(id=r[0], nome=r[1], marca=r[2], preco_unitario=float(r[3]), quantidade=r[4]) for r in rows]


def buscar_produto(conn, produto_id: int) -> Produto | None:
    """Busca um produto por ID. Retorna None se não encontrado."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, nome, marca, preco_unitario, quantidade FROM produtos WHERE id = %s;", (produto_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return Produto(id=row[0], nome=row[1], marca=row[2], preco_unitario=float(row[3]), quantidade=row[4])


def atualizar_preco(conn, produto_id: int, novo_preco: float) -> None:
    """Atualiza o preço unitário de um produto."""
    with conn.cursor() as cur:
        cur.execute("UPDATE produtos SET preco_unitario = %s WHERE id = %s;", (novo_preco, produto_id))


def atualizar_quantidade(conn, produto_id: int, nova_quantidade: int) -> None:
    """Atualiza a quantidade em estoque de um produto."""
    with conn.cursor() as cur:
        cur.execute("UPDATE produtos SET quantidade = %s WHERE id = %s;", (nova_quantidade, produto_id))


# --- CRUD Compras ---

def inserir_compra(conn, itens: dict, total_final: float) -> int:
    """Insere uma nova compra e retorna o ID gerado.
    
    itens: dict no formato {"produto_id": {"nome": str, "quantidade": int, "preco_unitario": float, "subtotal": float}}
    """
    itens_json = json.dumps(itens)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO compras (itens, total_final) VALUES (%s, %s) RETURNING id;",
            (itens_json, total_final),
        )
        return cur.fetchone()[0]


def buscar_compra(conn, compra_id: int) -> Compra | None:
    """Busca uma compra por ID. Retorna None se não encontrada."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, itens, total_final FROM compras WHERE id = %s;", (compra_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return Compra(id=row[0], itens=row[1], total_final=float(row[2]))


def listar_compras(conn) -> list[Compra]:
    """Retorna todas as compras como lista de objetos Compra."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, itens, total_final FROM compras ORDER BY id;")
        rows = cur.fetchall()
        return [Compra(id=r[0], itens=r[1], total_final=float(r[2])) for r in rows]
