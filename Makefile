.PHONY: test test-cov clean dev-setup open-cov setup

test:
	pytest

test-cov:
	pytest --cov=src --cov-report=term --cov-report=html

clean:
	rm -rf .coverage htmlcov/ .pytest_cache/ __pycache__/ tests/__pycache__/ src/__pycache__/

dev-setup:
	pip install -r requirements-dev.txt

setup:
	pip install -r requirements-dev.txt
	find src -name requirements.txt -exec pip install -r {} \;

open-cov:
	@if [ "$(shell uname)" = "Darwin" ]; then \
		open htmlcov/index.html; \
	elif [ "$(shell uname)" = "Linux" ]; then \
		xdg-open htmlcov/index.html 2>/dev/null || sensible-browser htmlcov/index.html 2>/dev/null || echo "Could not open browser automatically. Please open htmlcov/index.html manually."; \
	else \
		start htmlcov/index.html 2>/dev/null || echo "Could not open browser automatically. Please open htmlcov/index.html manually."; \
	fi