"""
Módulo responsável pela visualização do modelo de Machine Learning.

Este módulo contém a classe Models que gerencia a exibição do formulário
de entrada de dados e previsão usando Random Forest.
"""

import streamlit as st


class Models:
    def __init__(self) -> None:
        """
        Inicializa a view de Modelos com configuração padrão.

        Configura o título de exibição para a interface de previsão
        de qualidade de vinhos usando Random Forest.

        Attributes:
            title (str): Título da página.
            model: Modelo Random Forest carregado (será carregado das GitHub Releases).
        """
        self.title = "Classificação de Qualidade de Vinhos"
        self.model = None  # Será carregado das GitHub Releases
        self._load_model()

    def _load_model(self) -> None:
        """
        Carrega o modelo Random Forest treinado.

        TODO: Implementar carregamento do modelo versionado via GitHub Releases.
        O modelo será baixado da última release do repositório e carregado
        usando joblib ou pickle.

        Returns:
            None
        """
        # TODO: Implementar carregamento do modelo das GitHub Releases
        # Exemplo:
        # from models.inferences import Inferences
        # inference = Inferences()
        # model_path = download_model_from_github_release(version="latest")
        # self.model = inference.load_model(model_path)
        pass

    def _render_form(self) -> None:
        """
        Renderiza o formulário de entrada de dados para o Random Forest.

        Returns:
            None
        """
        st.header("Dados obrigatórios:", divider="yellow", width="content")

        st.warning(
            "Estes são os dados mínimos para fazer a classificação.\n"
            "Para ter um melhor desempenho, preencha todos os campos."
        )

        with st.form(key="form_random_forest_mandatory"):
            col_1, col_2, col_3 = st.columns(3)

            with col_1:
                volatile_acidity = st.number_input(
                    "Volatile Acidity *",
                    min_value=0.0,
                    format="%.4f",
                    help="Campo obrigatório",
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
                    help="Campo obrigatório",
                )

            with col_3:
                chlorides = st.number_input(
                    "Chlorides *",
                    min_value=0.0,
                    format="%.4f",
                    help="Campo obrigatório",
                )
                sulphates = st.number_input(
                    "Sulphates *",
                    min_value=0.0,
                    format="%.4f",
                    help="Campo obrigatório",
                )

            st.header("Campos opcionais:", divider="yellow", width="content")

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

            submitted = st.form_submit_button("Classificar", type="primary")

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
                        f"❌ Por favor, preencha os seguintes campos obrigatórios:\n"
                        f"- {', '.join(campos_vazios)}"
                    )
                else:
                    st.success("✅ Todos os campos obrigatórios foram preenchidos!")

                    if self.model is None:
                        st.warning(
                            "⚠️ Modelo não carregado. "
                            "O modelo será baixado automaticamente das "
                            "GitHub Releases na próxima versão."
                        )
                    else:
                        st.info("Processando classificação com Random Forest...")

                        # TODO: Implementar predição quando modelo estiver carregado
                        # import pandas as pd
                        # dados = pd.DataFrame([{
                        #     "fixed acidity": fixed_acidity,
                        #     "volatile acidity": volatile_acidity,
                        #     "citric acid": citric_acid,
                        #     "residual sugar": residual_sugar,
                        #     "chlorides": chlorides,
                        #     "free sulfur dioxide": free_sulfur_dioxide,
                        #     "total sulfur dioxide": total_sulfur_dioxide,
                        #     "density": density,
                        #     "pH": ph,
                        #     "sulphates": sulphates,
                        #     "alcohol": alcohol,
                        # }])
                        # resultado = self.model.predict(dados)
                        # st.success(f"🍷 Qualidade prevista: {resultado[0]}")

    def render(self) -> None:
        """
        Renderiza a interface de previsão com Random Forest.

        Exibe o título e o formulário de entrada de dados para realizar
        a classificação da qualidade do vinho usando Random Forest.

        Returns:
            None
        """
        st.title(self.title, anchor=False)
        self._render_form()
