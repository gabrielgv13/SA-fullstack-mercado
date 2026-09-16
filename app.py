"""Iniciador da aplicação — execute a partir da raiz do projeto.

Uso:
    uv run python app.py
"""

from sa_fullstack_mercado.aplicacao import app

if __name__ == "__main__":
    app.run(debug=True)