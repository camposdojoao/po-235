"""
Aplicação principal Streamlit para visualização de modelos de Machine Learning.

Este módulo serve como ponto de entrada para a aplicação Streamlit, gerenciando
a navegação entre diferentes views e renderizando os componentes principais da
interface (sidebar e modelos).
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st

from streamlit_app.models import Models
from streamlit_app.sidebar import Sidebar

if "view" not in st.session_state:
    st.session_state["view"] = "models"

view = st.session_state.get("view", "models")

Sidebar().render()

if view == "models":
    Models().render()
# elif view == "dashboards":
#     Dashboard().render()
