"""Entrypoint para treinamento de modelos de classificação de vinhos."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from models.model import Modelo


def main(modelo_tipo: str = "random_forest") -> None:
    """
    Executa o treinamento do modelo.

    Args:
        modelo_tipo: Tipo de modelo a ser treinado.

    Raises:
        Exception: Se houver erro durante o treinamento.
    """
    try:
        model = Modelo(modelo_tipo)
        model.train()
    except Exception as e:
        raise Exception(f"Erro durante o treinamento: {str(e)}") from e


if __name__ == "__main__":
    main()
