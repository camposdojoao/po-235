import streamlit as st
from pathlib import Path

class Sidebar:

    def __init__(self):
        """
        Initialize the Sidebar with default configuration.
        
        Sets up the logo path, dimensions, application title, and configures
        all navigation menu items with their respective properties including
        titles, descriptions, button texts, and view mappings.
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
                "view": "models"
            },
            "dashboards": {
                "title": "Dashboards",
                "expanded": False,
                "description": "- Métricas,\n - Análise Exploratória",
                "button_text": "Open Dashboards",
                "button_key": "open-dashboards",
                "view": "dashboards"
            }
        }

    def _render_header(self):
        """
        Render the sidebar header with logo and title.
        
        Creates a centered layout using Streamlit columns to display the
        application logo and title. Uses a 3-column layout with proportions
        [1.75, 2, 1] to center the logo in the middle column.
        
        Returns:
            None
        """
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(self.logo_path, width=self.logo_width)
        st.markdown("---")

    def _render_navigation_item(self, item_key, item_config):
        """
        Render a single navigation item (expander with button).
        
        Creates an expandable section in the sidebar for a navigation item.
        Displays the item's title, description (if available), and a button
        (if configured). Updates the session state view when the button is clicked.
        
        Args:
            item_key (str): Unique identifier for the navigation item
            item_config (dict): Configuration dictionary containing:
                - title (str): Display title for the expander
                - expanded (bool): Whether the expander should be open by default
                - description (str, optional): Description text to display
                - button_text (str, optional): Text for the action button
                - button_key (str, optional): Unique key for the button
                - view (str): Target view to switch to when button is clicked
        
        Returns:
            None
        """
        with st.sidebar.expander(item_config["title"], expanded=item_config["expanded"]):
            if item_config["description"]:
                st.markdown(item_config["description"])
            
            if item_config["button_text"] and item_config["button_key"]:
                if st.button(item_config["button_text"], key=item_config["button_key"]):
                    st.session_state["view"] = item_config["view"]

    def render(self):
        """
        Main method to render the complete sidebar.
        
        Orchestrates the rendering of all sidebar components in the correct order:
        1. Header with logo and title
        2. Databricks connection status
        3. Navigation menu items (including Confluence documentation)
        
        Returns:
            None
        """
        with st.sidebar:
            self._render_header()
            
            for item_key, item_config in self.navigation_items.items():
                self._render_navigation_item(item_key, item_config)