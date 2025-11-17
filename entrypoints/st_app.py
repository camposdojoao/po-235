"""
Main Streamlit application for wine quality prediction.

This module serves as the entry point for the Streamlit application,
rendering the classification interface with Random Forest.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st

from streamlit_app.models import Models

st.set_page_config(page_title="Wine Quality Prediction", page_icon="🍷", layout="wide")

Models().render()
