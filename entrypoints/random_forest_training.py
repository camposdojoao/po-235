import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from models.random_forest import Modelo
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

variavel = 'RomForestClassifier(random_state=42)'

if variavel == 'RandomForestClassifier(random_state=42)':
    model = Modelo(
        'src/winequality-red.csv',
        'src/winequality-white.csv',
        RandomForestClassifier(random_state=42)
    )
elif variavel == 'XGBClassifier(random_state=42)':
    model = Modelo(
        'src/winequality-red.csv',
        'src/winequality-white.csv',
        XGBClassifier(random_state=42)
    )
elif variavel == 'radientBoostingClassifier(random_state=42)':
    model = Modelo(
        'src/winequality-red.csv',
        'src/winequality-white.csv',
        GradientBoostingClassifier(random_state=42)
    )
else:
    print("passou errado aí")

try:
    model.train()
except:
    raise("deu errado")
