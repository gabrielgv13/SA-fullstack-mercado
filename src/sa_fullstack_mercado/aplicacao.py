"""Rotas e lógica de extração de dados — aplicação Flask."""

import os

from flask import Flask, render_template, request, redirect, url_for

from . import banco_de_dados
from .modelos import Produto, iniciar_tabelas
from .popular_dados_iniciais import popular_dados_iniciais

# Configurar caminho dos templates relativo a este arquivo
_DIRETORIO_TEMPLATES = os.path.join(os.path.dirname(__file__), "templates")

app = Flask(__name__, template_folder=_DIRETORIO_TEMPLATES)

# Iniciar servidor pgembed e criar schema ao carregar o módulo
_servidor = banco_de_dados.iniciar_servidor()
_conexao = banco_de_dados.obter_conexao(_servidor)
iniciar_tabelas(_conexao)


@app.teardown_appcontext
def _encerrar(exception=None):
    """Para o servidor pgembed quando a app encerra."""
    banco_de_dados.parar_servidor()


# --- Rotas ---

@app.route("/")
def pagina_inicial():
    """Página inicial com lista de produtos."""
    produtos = banco_de_dados.listar_produtos(_conexao)
    compras = banco_de_dados.listar_compras(_conexao)
    return render_template("index.html", produtos=produtos, compras=compras)


@app.route("/produtos/cadastrar", methods=["GET", "POST"])
def cadastrar_produto():
    """Formulário de cadastro de produto."""
    if request.method == "POST":
        nome = request.form["nome"]               # tipo: str
        marca = request.form["marca"]              # tipo: str
        preco_unitario = float(request.form["preco_unitario"])  # tipo: float
        quantidade = int(request.form["quantidade"])            # tipo: int

        produto = Produto(id=0, nome=nome, marca=marca, preco_unitario=preco_unitario, quantidade=quantidade)
        banco_de_dados.inserir_produto(_conexao, produto.nome, produto.marca, produto.preco_unitario, produto.quantidade)

        return redirect(url_for("pagina_inicial"))

    return render_template("cadastrar_produto.html")


@app.route("/compra/criar", methods=["GET", "POST"])
def criar_compra():
    """Criar uma nova compra selecionando produtos e quantidades."""
    if request.method == "POST":
        itens = {}
        total_final = 0.0

        # Processar cada produto do formulário
        produtos = banco_de_dados.listar_produtos(_conexao)
        for produto in produtos:
            chave_quantidade = f"qtd_{produto.id}"
            quantidade = int(request.form.get(chave_quantidade, 0))  # tipo: int

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
                banco_de_dados.atualizar_quantidade(_conexao, produto.id, max(novo_estoque, 0))

        if itens:
            compra_id = banco_de_dados.inserir_compra(_conexao, itens, total_final)

        if itens:
            return redirect(url_for("nota_fiscal", compra_id=compra_id))

        return redirect(url_for("criar_compra"))

    produtos = banco_de_dados.listar_produtos(_conexao)
    return render_template("criar_compra.html", produtos=produtos)


@app.route("/compra/<int:compra_id>/nota")
def nota_fiscal(compra_id: int):
    """Exibir nota fiscal de uma compra."""
    compra = banco_de_dados.buscar_compra(_conexao, compra_id)
    if compra is None:
        return "Compra não encontrada", 404
    return render_template("nota_fiscal.html", compra=compra)


# Seed via endpoints após todas as rotas estarem registradas
popular_dados_iniciais(app, _conexao)
