.PHONY: format lint fix test build

build:
	@echo "==> Building Project..."
	pip install -r requirements-dev.txt
	pip install -e .
	@echo "✅ Building completed successfully."	

fix:
	@echo "==> Running Ruff lint fixes..."
	ruff check . --fix

	@echo ""
	@echo "==> Formatting code..."
	ruff format .

	@echo ""
	@echo "✅ Ruff completed successfully."

lint:
	@echo "==> Checking lint issues..."
	ruff check .

format:
	@echo "==> Formatting code..."
	ruff format .

test:
	@echo "==> Running tests..."
	pytest tests/