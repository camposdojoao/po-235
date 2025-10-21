.PHONY: streamlit


######################################
## ENV SETUP COMMANDS ##

install-uv:
	curl -LsSf https://astral.sh/uv/0.8.23/install.sh | sh

install:
	uv lock
	uv sync

######################################
## STREAMLIT COMMANDS ##

streamlit:
	uv run streamlit run entrypoints/st_app.py


######################################
## RUFF FORMAT COMMANDS ##

check:
	uv run ruff check . --fix
	uv run ruff format . --check

format:
	uv run ruff format .

######################################
## TESTS COMMANDS ##

run-ci: check