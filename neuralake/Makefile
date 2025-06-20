.PHONY: lint format check install test help

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	poetry install

lint:  ## Run linting and formatting
	python3 scripts/lint.py --fix

check:  ## Check code quality without fixing
	python3 scripts/lint.py

format:  ## Format code only
	python3 scripts/lint.py --format-only

test:  ## Run tests (when implemented)
	poetry run pytest

clean:  ## Clean cache files
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".ruff_cache" -delete
	find . -type f -name "*.pyc" -delete 