import streamlit as st


class Models:
    def __init__(self):
        """
        Initialize the ObservabilityView with default configuration.

        Sets up the display title, chart dimensions, and dataframe height
        for the observability and cost monitoring interface.
        """
        self.title = "Modelos"
        self.chart_height = 500

    def _load_data(self):
        pass

    def render(self):
        st.title(self.title, anchor=False)

        rf_tab, xgb_tab, gb_tab = st.tabs(
            ["Random Forest", "XGBoost", "Gradient Boost"]
        )

        with rf_tab:
            st.warning("tamo fazendo ainda, calma aí")

        with xgb_tab:
            st.warning("calma aí po")

        with gb_tab:
            st.warning("aí é foda")
