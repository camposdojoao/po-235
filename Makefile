######################################
## ENV SETUP COMMANDS ##

install-uv:
	curl -LsSf https://astral.sh/uv/0.8.23/install.sh | sh

install-dev:
	uv lock --frozen
	uv sync --no-upgrade --extra spark