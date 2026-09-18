from .aplicacao import app  # noqa: F401


def main() -> None:
    """Ponto de entrada CLI — inicia o servidor Flask."""
    # use_reloader=False: no Windows o reloader do Flask envia CTRL_C_EVENT para
    # o grupo de processos, matando os backends do PostgreSQL embutido (pgembed)
    # e deixando o servidor num estado inconsistente (AssertionError no pgembed).
    app.run(debug=True, use_reloader=False)
