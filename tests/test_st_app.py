"""Testes unitários para o entrypoint Streamlit."""

import importlib


def test_st_app_executa_sem_erros(streamlit_mocks: dict[str, object]) -> None:  # noqa: ARG001
    """
    Testa se o entrypoint Streamlit executa sem erros.

    Verifica se o arquivo st_app.py pode ser importado e executado
    sem lançar exceções, garantindo que a aplicação Streamlit está
    funcional e pode ser iniciada.

    Args:
        streamlit_mocks: Dicionário com mocks configurados para Streamlit (fixture).

    Note:
        Este teste usa mocks para evitar a necessidade de inicializar
        o servidor Streamlit real durante os testes.

    Raises:
        Exception: Se houver qualquer erro durante a execução do entrypoint.
    """
    import entrypoints.st_app

    importlib.reload(entrypoints.st_app)
