"""Rotas e lógica de extração de dados — aplicação Flask."""

import os

from flask import Flask, render_template, request, redirect, url_for

from . import db
from .schema import Produto, init_schema
from .population import seed_data

# Configurar caminho dos templates relativo a este arquivo
_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

app = Flask(__name__, template_folder=_TEMPLATE_DIR)

# Iniciar servidor pgembed e criar schema ao carregar o módulo
_server = db.start_server()
_conn = db.get_connection(_server)
init_schema(_conn)


@app.teardown_appcontext
def _shutdown(exception=None):
    """Para o servidor pgembed quando a app encerra."""
    db.stop_server()


# --- Rotas ---

@app.route("/")
def index():
    """Página inicial com lista de produtos."""
    produtos = db.listar_produtos(_conn)
    compras = db.listar_compras(_conn)
    return render_template("index.html", produtos=produtos, compras=compras)


@app.route("/produtos/cadastrar", methods=["GET", "POST"])
def cadastrar_produto():
    """Formulário de cadastro de produto."""
    if request.method == "POST":
        nome = request.form["nome"]
        marca = request.form["marca"]
        preco_unitario = float(request.form["preco_unitario"])
        quantidade = int(request.form["quantidade"])

        produto = Produto(id=0, nome=nome, marca=marca, preco_unitario=preco_unitario, quantidade=quantidade)
        db.inserir_produto(_conn, produto.nome, produto.marca, produto.preco_unitario, produto.quantidade)

        return redirect(url_for("index"))

    return render_template("cadastrar_produto.html")


@app.route("/compra/criar", methods=["GET", "POST"])
def criar_compra():
    """Criar uma nova compra selecionando produtos e quantidades."""
    if request.method == "POST":
        itens = {}
        total_final = 0.0

        # Processar cada produto do formulário
        produtos = db.listar_produtos(_conn)
        for produto in produtos:
            qtd_key = f"qtd_{produto.id}"
            quantidade = int(request.form.get(qtd_key, 0))
            if quantidade > 0:
                subtotal = produto.calcular_preco(quantidade)
                itens[str(produto.id)] = {
                    "nome": produto.nome,
                    "quantidade": quantidade,
                    "preco_unitario": produto.preco_unitario,
                    "subtotal": subtotal,
                }
                total_final += subtotal

                # Atualizar estoque
                novo_estoque = produto.quantidade - quantidade
                db.atualizar_quantidade(_conn, produto.id, max(novo_estoque, 0))

        if itens:
            compra_id = db.inserir_compra(_conn, itens, total_final)
            return redirect(url_for("nota_fiscal", compra_id=compra_id))

        return redirect(url_for("criar_compra"))

    produtos = db.listar_produtos(_conn)
    return render_template("criar_compra.html", produtos=produtos)


@app.route("/compra/<int:compra_id>/nota")
def nota_fiscal(compra_id: int):
    """Exibir nota fiscal de uma compra."""
    compra = db.buscar_compra(_conn, compra_id)
    if compra is None:
        return "Compra não encontrada", 404
    return render_template("nota_fiscal.html", compra=compra)


# Seed via endpoints após todas as rotas estarem registradas
seed_data(app, _conn)
