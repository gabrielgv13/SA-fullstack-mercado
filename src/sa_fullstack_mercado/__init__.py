from .app import app  # noqa: F401


def main() -> None:
    """Ponto de entrada CLI — inicia o servidor Flask."""
    app.run(debug=True)
