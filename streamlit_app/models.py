import streamlit as st


class Models:
    def __init__(self) -> None:
        """
        Inicializa a view de Modelos com configuração padrão.

        Configura o título de exibição e altura dos gráficos para a
        interface de visualização de modelos de Machine Learning.

        Attributes:
            title (str): Título da página de modelos.
            chart_height (int): Altura dos gráficos em pixels.
        """
        self.title = "Modelos"
        self.chart_height = 500

    def _load_data(self) -> None:
        """
        Carrega os dados necessários para os modelos.

        Método placeholder para carregar dados dos modelos de ML.
        Atualmente não implementado.

        Returns:
            None
        """
        pass

    def render(self) -> None:
        """
        Renderiza a interface de visualização dos modelos.

        Cria e exibe as abas para os diferentes modelos de Machine Learning
        (Random Forest, XGBoost, Gradient Boost) na interface Streamlit.

        Returns:
            None
        """
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
