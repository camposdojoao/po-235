"""Entrypoint para treinamento de modelos de classificação de vinhos."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from models.model import Modelo

variavel = "random_forest"

try:
    model = Modelo(variavel)
    model.train()
except Exception as e:
    raise Exception(f"Erro durante o treinamento: {str(e)}") from e
