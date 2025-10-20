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

format:
	uv run ruff check . --select I --fix
	uv run ruff format .

check:
	uv run ruff format . --check

######################################
## TESTS COMMANDS ##

run-ci: format check