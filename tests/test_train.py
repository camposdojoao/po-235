"""Unit tests for the training entrypoint."""


def test_train_executa_sem_erros(train_mocks: dict[str, object]) -> None:  # noqa: ARG001
    """
    Test if the training entrypoint executes without errors.

    Verifies that the main() function of the train.py entrypoint can be executed
    without raising exceptions, ensuring that the training pipeline is
    functional and can be started.

    Args:
        train_mocks: Dictionary with configured mocks for the model (fixture).

    Note:
        This test uses mocks to avoid actual model training,
        which would be time-consuming and unnecessary to verify if the entrypoint
        is working correctly.

    Raises:
        Exception: If there is any error during entrypoint execution.
    """
    from entrypoints.train import main

    main()
