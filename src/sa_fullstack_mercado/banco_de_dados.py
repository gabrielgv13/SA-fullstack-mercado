"""Funções que manipulam o banco de dados pgembed."""

import json
import os
import subprocess
import time
from pathlib import Path

import pgembed
from pgembed.postgres_server import PostgresServer
import psutil
import psycopg

from .modelos import Produto, Compra

# Singleton do servidor pgembed
_servidor = None
_DIRETORIO_DADOS = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) / "data_mercado"


def _status_postmaster() -> str | None:
    """Lê o status (8ª linha) do postmaster.pid, ou None se não existir."""
    pid_file = _DIRETORIO_DADOS / "postmaster.pid"
    try:
        linhas = pid_file.read_text().splitlines()
        if len(linhas) >= 8:
            return linhas[7].strip()
    except OSError:
        pass
    return None


def _aguardar_servidor_pronto(timeout: float = 90.0) -> None:
    """Aguarda o servidor PostgreSQL ficar 'ready' se ele estiver rodando mas
    ainda não pronto (ex.: após um backend ser morto por CTRL_C_EVENT no Windows).

    O pgembed lança AssertionError se encontrar um postmaster rodando com
    status != 'ready', então esperamos aqui antes de chamá-lo.
    """
    pid_file = _DIRETORIO_DADOS / "postmaster.pid"
    if not pid_file.exists():
        return

    try:
        pid = int(pid_file.read_text().splitlines()[0].strip())
    except (OSError, ValueError, IndexError):
        return

    if _status_postmaster() == "ready" or not psutil.pid_exists(pid):
        return

    print("[banco_de_dados] Servidor PostgreSQL ainda não pronto; aguardando...")
    inicio = time.time()
    while time.time() - inicio < timeout:
        time.sleep(1.0)
        if _status_postmaster() == "ready":
            print("[banco_de_dados] Servidor PostgreSQL pronto.")
            return
        if not psutil.pid_exists(pid):
            return  # processo morreu; o pgembed vai iniciar do zero

    # Timeout: derruba o servidor para o pgembed reiniciar de forma limpa.
    print("[banco_de_dados] Servidor não ficou pronto; reiniciando...")
    try:
        from pgembed._commands import POSTGRES_BIN_PATH

        pg_ctl = POSTGRES_BIN_PATH / ("pg_ctl.exe" if os.name == "nt" else "pg_ctl")
        subprocess.run(
            [str(pg_ctl), "-D", str(_DIRETORIO_DADOS), "-w", "stop"],
            timeout=30,
            capture_output=True,
            text=True,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[banco_de_dados] Falha ao parar servidor: {exc}")


def obter_servidor_banco() -> PostgresServer:
    """Retorna a instância singleton do servidor pgembed."""
    global _servidor
    if _servidor is None:
        _servidor = pgembed.get_server(_DIRETORIO_DADOS, cleanup_mode=None)
    return _servidor


def iniciar_servidor() -> PostgresServer:
    """Inicializa o pgdata e inicia o servidor pgembed."""
    _aguardar_servidor_pronto()
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
        cur.execute(
            "INSERT INTO produtos (nome, marca, preco_unitario, quantidade) VALUES (%s, %s, %s, %s) RETURNING id;",
            (nome, marca, preco_unitario, quantidade),
        )
        return cur.fetchone()[0]


def listar_produtos(conexao) -> list[Produto]:
    """Retorna todos os produtos como lista de objetos Produto."""
    with conexao.cursor() as cur:
        cur.execute("SELECT id, nome, marca, preco_unitario, quantidade FROM produtos ORDER BY id;")
        linhas = cur.fetchall()
        return [Produto(id=linha[0], nome=linha[1], marca=linha[2], preco_unitario=float(linha[3]), quantidade=linha[4]) for linha in linhas]


def buscar_produto(conexao, produto_id: int) -> Produto | None:
    """Busca um produto por ID. Retorna None se não encontrado."""
    with conexao.cursor() as cur:
        cur.execute("SELECT id, nome, marca, preco_unitario, quantidade FROM produtos WHERE id = %s;", (produto_id,))
        linha = cur.fetchone()
        if linha is None:
            return None
        return Produto(id=linha[0], nome=linha[1], marca=linha[2], preco_unitario=float(linha[3]), quantidade=linha[4])


def atualizar_preco(conexao, produto_id: int, novo_preco: float) -> None:
    """Atualiza o preço unitário de um produto."""
    with conexao.cursor() as cur:
        cur.execute("UPDATE produtos SET preco_unitario = %s WHERE id = %s;", (novo_preco, produto_id))


def atualizar_quantidade(conexao, produto_id: int, nova_quantidade: int) -> None:
    """Atualiza a quantidade em estoque de um produto."""
    with conexao.cursor() as cur:
        cur.execute("UPDATE produtos SET quantidade = %s WHERE id = %s;", (nova_quantidade, produto_id))


# --- CRUD Compras ---

def inserir_compra(conexao, itens: dict, total_final: float) -> int:
    """Insere uma nova compra e retorna o ID gerado.
    
    itens: dict no formato {"produto_id": {"nome": str, "quantidade": int, "preco_unitario": float, "subtotal": float}}
    """
    itens_json = json.dumps(itens)
    with conexao.cursor() as cur:
        cur.execute(
            "INSERT INTO compras (itens, total_final) VALUES (%s, %s) RETURNING id;",
            (itens_json, total_final),
        )
        return cur.fetchone()[0]


def buscar_compra(conexao, compra_id: int) -> Compra | None:
    """Busca uma compra por ID. Retorna None se não encontrada."""
    with conexao.cursor() as cur:
        cur.execute("SELECT id, itens, total_final FROM compras WHERE id = %s;", (compra_id,))
        linha = cur.fetchone()
        if linha is None:
            return None
        return Compra(id=linha[0], itens=linha[1], total_final=float(linha[2]))


def listar_compras(conexao) -> list[Compra]:
    """Retorna todas as compras como lista de objetos Compra."""
    with conexao.cursor() as cur:
        cur.execute("SELECT id, itens, total_final FROM compras ORDER BY id;")
        linhas = cur.fetchall()
        return [Compra(id=linha[0], itens=linha[1], total_final=float(linha[2])) for linha in linhas]


def listar_compras(conexao) -> list[Compra]:
    """Retorna todas as compras como lista de objetos Compra."""
    with conexao.cursor() as cur:
        cur.execute("SELECT id, itens, total_final FROM compras ORDER BY id;")
        linhas = cur.fetchall()
        return [Compra(id=linha[0], itens=linha[1], total_final=float(linha[2])) for linha in linhas]
