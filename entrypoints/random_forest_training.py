import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from models.random_forest import Modelo
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

variavel = 'random_forest'

try:
    if variavel == 'random_forest':
        model = Modelo(
            'src/winequality-red.csv',
            'src/winequality-white.csv',
            RandomForestClassifier(random_state=42)
        )
    elif variavel == 'xgboost':
        model = Modelo(
            'src/winequality-red.csv',
            'src/winequality-white.csv',
            XGBClassifier(random_state=42)
        )
    elif variavel == 'gradient_boosting':
        model = Modelo(
            'src/winequality-red.csv',
            'src/winequality-white.csv',
            GradientBoostingClassifier(random_state=42)
        )
    else:
        print("passou errado aí")

    model.train()
except:
    raise("deu errado")
