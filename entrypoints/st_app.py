from pathlib import Path
import sys
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
