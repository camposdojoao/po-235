"""
Módulo responsável pela renderização da barra lateral da aplicação Streamlit.

Este módulo contém a classe Sidebar que gerencia a exibição do logotipo,
navegação e menu lateral da aplicação.
"""

from pathlib import Path
from typing import Any

import streamlit as st


class Sidebar:
    def __init__(self) -> None:
        """
        Inicializa a Sidebar com configuração padrão.

        Configura o caminho do logotipo, dimensões, título da aplicação e
        todos os itens do menu de navegação com suas respectivas propriedades,
        incluindo títulos, descrições, textos de botões e mapeamento de views.
        """
        # Caminho absoluto para a imagem baseado na localização deste arquivo
        self.logo_path = str(Path(__file__).parent / "img" / "ITA.png")
        self.logo_width = 500

        self.navigation_items = {
            "models": {
                "title": "Models",
                "expanded": True,
                "description": "- Random Forest\n- XGBoost\n- Gradient Boost",
                "button_text": "Open Models",
                "button_key": "open-random-forest",
                "view": "models",
            },
            "dashboards": {
                "title": "Dashboards",
                "expanded": False,
                "description": "- Métricas,\n - Análise Exploratória",
                "button_text": "Open Dashboards",
                "button_key": "open-dashboards",
                "view": "dashboards",
            },
        }

    def _render_header(self) -> None:
        """
        Renderiza o cabeçalho da sidebar com logotipo e título.

        Cria um layout centralizado usando colunas do Streamlit para exibir
        o logotipo e título da aplicação. Utiliza um layout de 3 colunas com
        proporções [1, 2, 1] para centralizar o logotipo na coluna do meio.

        Returns:
            None
        """
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(self.logo_path, width=self.logo_width)
        st.markdown("---")

    def _render_navigation_item(
        self, _item_key: str, item_config: dict[str, Any]
    ) -> None:
        """
        Renderiza um único item de navegação (expander com botão).

        Cria uma seção expansível na sidebar para um item de navegação.
        Exibe o título do item, descrição (se disponível) e um botão
        (se configurado). Atualiza a view no session state quando o botão é clicado.

        Args:
            _item_key (str): Identificador único para o item de navegação (não utilizado).
            item_config (dict): Dicionário de configuração contendo:
                - title (str): Título de exibição para o expander.
                - expanded (bool): Se o expander deve estar aberto por padrão.
                - description (str, opcional): Texto de descrição a ser exibido.
                - button_text (str, opcional): Texto para o botão de ação.
                - button_key (str, opcional): Chave única para o botão.
                - view (str): View de destino para alternar quando o botão for clicado.

        Returns:
            None
        """
        with st.sidebar.expander(
            item_config["title"], expanded=item_config["expanded"]
        ):
            if item_config["description"]:
                st.markdown(item_config["description"])

            if item_config["button_text"] and item_config["button_key"]:
                if st.button(item_config["button_text"], key=item_config["button_key"]):
                    st.session_state["view"] = item_config["view"]

    def render(self) -> None:
        """
        Método principal para renderizar a sidebar completa.

        Orquestra a renderização de todos os componentes da sidebar na ordem correta:
        1. Cabeçalho com logotipo e título
        2. Itens do menu de navegação

        Returns:
            None
        """
        with st.sidebar:
            self._render_header()

            for item_key, item_config in self.navigation_items.items():
                self._render_navigation_item(item_key, item_config)
