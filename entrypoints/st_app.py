import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from streamlit_app.sidebar import Sidebar
from streamlit_app.models import Models

if "view" not in st.session_state:
    st.session_state["view"] = "models"

view = st.session_state.get("view", "models")

Sidebar().render()

if view == "models":
    Models().render()
# elif view == "dashboards":
#     Dashboard().render()