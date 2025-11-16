"""
Módulo responsável pela visualização do modelo de Machine Learning.

Este módulo contém a classe Models que gerencia a exibição do formulário
de entrada de dados e previsão usando Random Forest.
"""

import pandas as pd
import streamlit as st
from sklearn.base import BaseEstimator

from streamlit_app.model_loader import ModelLoader, get_model_version


class Models:
    def __init__(self) -> None:
        """
        Inicializa a view de Modelos com configuração padrão.

        Configura o título de exibição para a interface de previsão
        de qualidade de vinhos usando Random Forest.

        Attributes:
            title (str): Título da página.
            model: Modelo Random Forest carregado das GitHub Releases.
            model_version (str): Versão do modelo em uso.
        """
        self.title = "Classificação de Qualidade de Vinhos"
        self.model_version = get_model_version()
        self.model = self._load_model()

    def _load_model(self) -> BaseEstimator | None:
        """
        Carrega o modelo Random Forest treinado do GitHub Releases.

        O modelo é baixado automaticamente da última release disponível
        e mantido em cache local para melhor performance.

        Returns:
            Modelo Random Forest carregado e pronto para uso.

        Raises:
            Exception: Se houver erro ao baixar ou carregar o modelo.
        """
        try:
            loader = ModelLoader(model_version=self.model_version)
            # Atualiza a versão após o loader determinar qual é (pode ser a última)
            self.model_version = loader.model_version

            # Informa qual versão foi carregada
            if self.model_version:
                st.info(f"📦 Carregando modelo versão: **{self.model_version}**")

            model = loader.load_model("random_forest_model.pkl")
            return model
        except Exception as e:
            st.error(
                f"❌ Erro ao carregar modelo:\n{str(e)}\n\n"
                "Verifique se a release existe no GitHub e tente novamente."
            )
            return None

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
                        st.error(
                            "❌ Modelo não disponível. Não foi possível "
                            "carregar o modelo para realizar a predição."
                        )
                    else:
                        # Preparar dados para predição
                        # As features devem estar na mesma ordem do treinamento
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

                        # Realizar predição
                        with st.spinner("Processando classificação..."):
                            resultado = self.model.predict(dados)
                            qualidade_map = {
                                0: "Ruim (≤ 5)",
                                1: "Média (6)",
                                2: "Boa (≥ 7)",
                            }
                            qualidade = qualidade_map.get(resultado[0], "Desconhecida")

                        # Exibir resultado
                        st.success(f"🍷 **Qualidade prevista:** {qualidade}")
                        st.info(f"Modelo utilizado: Random Forest {self.model_version}")

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
