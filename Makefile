######################################
## ENV SETUP COMMANDS ##

.PHONY: streamlit

install-uv:
	curl -LsSf https://astral.sh/uv/0.8.23/install.sh | sh

install:
	uv lock
	uv sync

streamlit:
	uv run streamlit run entrypoints/st_app.py