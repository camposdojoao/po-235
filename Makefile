.PHONY: streamlit install install-uv check format tests test-ci run-ci


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

tests:
	uv run pytest tests/ -v --cov=models --cov=entrypoints --cov-report=term-missing --cov-fail-under=75

test-ci:
	uv run pytest tests/ --cov=models --cov=entrypoints --cov-fail-under=75 --tb=short

run-ci: check test-ci