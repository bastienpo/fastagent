.PHONY: run audit fix clean

all: help

run:
	@uv run granian app.main:api

audit:
	@echo "Checking code for linting errors (ruff)..."
	uv tool run ruff check . --config .ruff.toml
	@echo "Checking code for formatting errors (ruff)..."
	uv tool run ruff format . --check --config .ruff.toml

fix:
	@echo "Fixing code for linting errors (ruff)..."
	uv tool run ruff check . --config .ruff.toml --select I --fix
	@echo "Fixing code for formatting errors (ruff)..."
	uv tool run ruff format . --config .ruff.toml
	

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache

help:
	@echo "Usage: make <target>"
	@echo "  run      Run the application"
	@echo "  audit    Check the code quality"
	@echo "  fix      Fix the code quality"
	@echo "  clean    Clean the project files"
