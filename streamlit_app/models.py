"""
Module responsible for the Machine Learning model visualization.

This module contains the Models class that manages the display of the
data input form and prediction using Random Forest.
"""

import pandas as pd
import streamlit as st
from sklearn.base import BaseEstimator

from streamlit_app.model_loader import ModelLoader, get_model_version


class Models:
    def __init__(self) -> None:
        """
        Initialize the Models view with default configuration.

        Configures the display title for the wine quality prediction
        interface using Random Forest.

        Attributes:
            title (str): Page title.
            model: Random Forest model loaded from GitHub Releases.
            model_version (str): Model version in use.
        """
        self.title = "Wine Quality Classification"
        self.model_version = get_model_version()
        self.model = self._load_model()

    def _load_model(self) -> BaseEstimator | None:
        """
        Load the trained Random Forest model from GitHub Releases.

        The model is automatically downloaded from the latest available
        release and kept in local cache for better performance.

        Returns:
            Loaded Random Forest model ready to use.

        Raises:
            Exception: If there is an error downloading or loading the model.
        """
        try:
            loader = ModelLoader(model_version=self.model_version)
            # Update version after loader determines which one (may be the latest)
            self.model_version = loader.model_version

            model = loader.load_model("random_forest_model.pkl")
            return model
        except Exception as e:
            st.error(
                f"❌ Error loading model:\n{str(e)}\n\n"
                "Check if the release exists on GitHub and try again."
            )
            return None

    def _render_form(self) -> None:
        """
        Render the data input form for Random Forest.

        Returns:
            None
        """

        with st.form(key="form_random_forest_mandatory"):
            st.header("Required data:", divider="yellow", width="content")

            col_1, col_2, col_3 = st.columns(3)

            with col_1:
                volatile_acidity = st.number_input(
                    "Volatile Acidity *",
                    min_value=0.0,
                    format="%.4f",
                    help="Required field",
                )
                density = st.number_input(
                    "Density *", min_value=0.0, format="%.4f", help="Campo obrigatório"
                )

            with col_2:
                alcohol = st.number_input(
                    "Alcohol *", min_value=0.0, format="%.2f", help="Campo obrigatório"
                )
                total_sulfur_dioxide = st.number_input(
                    "Total Sulfur Dioxide *",
                    min_value=0.0,
                    format="%.2f",
                    help="Required field",
                )

            with col_3:
                chlorides = st.number_input(
                    "Chlorides *",
                    min_value=0.0,
                    format="%.4f",
                    help="Required field",
                )
                sulphates = st.number_input(
                    "Sulphates *",
                    min_value=0.0,
                    format="%.4f",
                    help="Required field",
                )

            st.header("Optional fields:", divider="yellow", width="content")

            col_4, col_5, col_6 = st.columns(3)

            with col_4:
                fixed_acidity = st.number_input(
                    "Fixed Acidity", min_value=0.0, value=0.0, format="%.2f"
                )
                citric_acid = st.number_input(
                    "Citric Acid", min_value=0.0, value=0.0, format="%.2f"
                )

            with col_5:
                residual_sugar = st.number_input(
                    "Residual Sugar", min_value=0.0, value=0.0, format="%.2f"
                )
                free_sulfur_dioxide = st.number_input(
                    "Free Sulfur Dioxide", min_value=0.0, value=0.0, format="%.1f"
                )

            with col_6:
                ph = st.number_input(
                    "pH", min_value=0.0, max_value=14.0, value=0.0, format="%.2f"
                )

            submitted = st.form_submit_button("Classify", type="primary")

            if submitted:
                campos_vazios = []
                if volatile_acidity == 0.0:
                    campos_vazios.append("Volatile Acidity")
                if density == 0.0:
                    campos_vazios.append("Density")
                if alcohol == 0.0:
                    campos_vazios.append("Alcohol")
                if total_sulfur_dioxide == 0.0:
                    campos_vazios.append("Total Sulfur Dioxide")
                if chlorides == 0.0:
                    campos_vazios.append("Chlorides")
                if sulphates == 0.0:
                    campos_vazios.append("Sulphates")

                if campos_vazios:
                    st.error(
                        f"❌ Please fill in the following required fields:\n"
                        f"- {', '.join(campos_vazios)}"
                    )
                else:
                    st.success("✅ All required fields have been filled!")

                    if self.model is None:
                        st.error(
                            "❌ Model not available. Unable to "
                            "load the model to perform prediction."
                        )
                    else:
                        # Prepare data for prediction
                        # Features must be in the same order as training
                        dados = pd.DataFrame(
                            [
                                {
                                    "volatile acidity": volatile_acidity,
                                    "density": density,
                                    "alcohol": alcohol,
                                    "total sulfur dioxide": total_sulfur_dioxide,
                                    "chlorides": chlorides,
                                    "sulphates": sulphates,
                                }
                            ]
                        )

                        # Perform prediction
                        with st.spinner("Processing classification..."):
                            resultado = self.model.predict(dados)
                            qualidade_map = {
                                0: "Poor (≤ 5)",
                                1: "Average (6)",
                                2: "Good (≥ 7)",
                            }
                            qualidade = qualidade_map.get(resultado[0], "Unknown")

                        # Display result
                        st.success(f"🍷 **Predicted quality:** {qualidade}")
                        st.info(f"Model used: Random Forest {self.model_version}")

    def render(self) -> None:
        """
        Render the prediction interface with Random Forest.

        Displays the title and data input form to perform
        wine quality classification using Random Forest.

        Returns:
            None
        """
        st.title(self.title, anchor=False)
        self._render_form()

        st.caption(f"Model version: {self.model_version}")
