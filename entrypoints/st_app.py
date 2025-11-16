"""
Aplicação principal Streamlit para previsão de qualidade de vinhos.

Este módulo serve como ponto de entrada para a aplicação Streamlit,
renderizando a interface de classificação com Random Forest.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st

from streamlit_app.models import Models

st.set_page_config(
    page_title="Wine Quality Prediction",
    page_icon="🍷",
    layout="wide"
)

Models().render()
