"""Entrypoint for training the Random Forest wine classification model."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from models.model import Modelo


def main() -> None:
    """
    Execute the Random Forest model training.

    Raises:
        Exception: If there is an error during training.
    """
    try:
        model = Modelo()
        model.train()
    except Exception as e:
        raise Exception(f"Error during training: {str(e)}") from e


if __name__ == "__main__":
    main()
