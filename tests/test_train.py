"""Testes unitários para o entrypoint de treinamento."""


def test_train_executa_sem_erros(train_mocks: dict[str, object]) -> None:  # noqa: ARG001
    """
    Testa se o entrypoint de treinamento executa sem erros.

    Verifica se a função main() do entrypoint train.py pode ser executada
    sem lançar exceções, garantindo que o pipeline de treinamento está
    funcional e pode ser iniciado com um tipo de modelo válido.

    Args:
        train_mocks: Dicionário com mocks configurados para o modelo (fixture).

    Note:
        Este teste usa mocks para evitar o treinamento real do modelo,
        que seria demorado e desnecessário para verificar se o entrypoint
        está funcionando corretamente.

    Raises:
        Exception: Se houver qualquer erro durante a execução do entrypoint.
    """
    from entrypoints.train import main

    main("random_forest")
