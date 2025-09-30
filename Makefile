# Makefile para Virtual Power Meter

.PHONY: help install install-dev test lint format clean run run-verbose run-dual

# Variables
PYTHON := python
PIP := pip
SRC_DIR := src
TEST_DIR := tests

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias de producción
	$(PIP) install -r requirements.txt

install-dev: ## Instalar dependencias de desarrollo
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

test: ## Ejecutar tests
	$(PYTHON) -m pytest $(TEST_DIR) -v

test-cov: ## Ejecutar tests con cobertura
	$(PYTHON) -m pytest $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing

lint: ## Ejecutar linter
	flake8 $(SRC_DIR) $(TEST_DIR)
	mypy $(SRC_DIR)

format: ## Formatear código
	black $(SRC_DIR) $(TEST_DIR) *.py

format-check: ## Verificar formato
	black --check $(SRC_DIR) $(TEST_DIR) *.py

clean: ## Limpiar archivos generados
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/

run: ## Ejecutar simulador (1 dispositivo)
	$(PYTHON) virtual_pm_CLI_refactored.py

run-verbose: ## Ejecutar simulador en modo verbose
	$(PYTHON) virtual_pm_CLI_refactored.py --verbose

run-dual: ## Ejecutar simulador (2 dispositivos)
	$(PYTHON) virtual_pm_CLI_refactored.py --devices 2 --verbose

run-rtu: ## Ejecutar simulador RTU (requiere puerto serial)
	$(PYTHON) virtual_pm_CLI_refactored.py --protocol rtu --port-serial COM3

# Comandos de desarrollo
dev-setup: install-dev ## Configuración completa de desarrollo
	@echo "✅ Entorno de desarrollo configurado"

check-all: format-check lint test ## Verificar todo (formato, lint, tests)

build: clean ## Construir distribución
	$(PYTHON) -m build

# Comandos específicos del proyecto
show-registers: ## Mostrar registros disponibles
	@echo "Registros PM21XX:"
	@$(PYTHON) -c "import json; print(json.dumps(json.load(open('config/register_table_PM21XX.json')), indent=2)[:1000] + '...')"
	@echo "\nRegistros Generic:"
	@$(PYTHON) -c "import json; print(json.dumps(json.load(open('config/register_table_generic.json')), indent=2)[:1000] + '...')"

validate-config: ## Validar archivos de configuración
	@$(PYTHON) -c "from src.data_generation.register_loader import load_register_table; print('✅ PM21XX:', len(load_register_table('config/register_table_PM21XX.json')), 'registros'); print('✅ Generic:', len(load_register_table('config/register_table_generic.json')), 'registros')"