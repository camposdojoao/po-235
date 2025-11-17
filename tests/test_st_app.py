"""Unit tests for the Streamlit entrypoint."""

import importlib


def test_st_app_executa_sem_erros(streamlit_mocks: dict[str, object]) -> None:  # noqa: ARG001
    """
    Test if the Streamlit entrypoint executes without errors.

    Verifies that the st_app.py file can be imported and executed
    without raising exceptions, ensuring that the Streamlit application is
    functional and can be started.

    Args:
        streamlit_mocks: Dictionary with configured mocks for Streamlit (fixture).

    Note:
        This test uses mocks to avoid the need to initialize
        the actual Streamlit server during tests.

    Raises:
        Exception: If there is any error during entrypoint execution.
    """
    import entrypoints.st_app

    importlib.reload(entrypoints.st_app)
