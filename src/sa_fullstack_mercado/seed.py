"""Popula o banco de dados via POST requests, simulando uso da interface."""

import urllib.request
import urllib.parse

BASE_URL = "http://127.0.0.1:5000"


def post_form(url: str, data: dict) -> None:
    """Envia um POST com dados de formulário para a URL."""
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=encoded, method="POST")
    try:
        urllib.request.urlopen(req)
        print(f"  OK: {url} -> {data.get('nome', data)}")
    except urllib.error.HTTPError as e:
        print(f"  ERRO: {url} -> {e.code} {e.reason}")


def seed_produtos():
    """Cadastra produtos via POST /produtos/cadastrar."""
    print("Cadastrando produtos...")
    produtos = [
        {"nome": "Arroz", "marca": "Tio João", "preco_unitario": "5.49", "quantidade": "100"},
        {"nome": "Feijão", "marca": "Camil", "preco_unitario": "8.99", "quantidade": "80"},
        {"nome": "Macarrão", "marca": "Barilla", "preco_unitario": "4.29", "quantidade": "60"},
        {"nome": "Leite", "marca": "Piracanjuba", "preco_unitario": "4.59", "quantidade": "120"},
        {"nome": "Café", "marca": "Pilão", "preco_unitario": "12.90", "quantidade": "50"},
    ]
    for p in produtos:
        post_form(f"{BASE_URL}/produtos/cadastrar", p)


def seed_compras():
    """Cria compras via POST /compra/criar."""
    print("\nCriando compras...")

    # Compra 1: Arroz (id=1) x2 + Leite (id=4) x3
    compra1 = {"qtd_1": "2", "qtd_2": "0", "qtd_3": "0", "qtd_4": "3", "qtd_5": "0"}
    post_form(f"{BASE_URL}/compra/criar", compra1)

    # Compra 2: Feijão (id=2) x1 + Macarrão (id=3) x4 + Café (id=5) x1
    compra2 = {"qtd_1": "0", "qtd_2": "1", "qtd_3": "4", "qtd_4": "0", "qtd_5": "1"}
    post_form(f"{BASE_URL}/compra/criar", compra2)


if __name__ == "__main__":
    print(f"Populando dados em {BASE_URL}\n")
    seed_produtos()
    seed_compras()
    print("\nConcluído!")
