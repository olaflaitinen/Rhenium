# Makefile for LLM-Based DBMS
# Simple commands for common development tasks

.PHONY: help install install-dev test lint format clean run init-db docker-up docker-down

help:
	@echo "LLM-Based DBMS - Development Commands"
	@echo "======================================"
	@echo ""
	@echo "Installation:"
	@echo "  make install     - Install production dependencies"
	@echo "  make install-dev - Install dev dependencies"
	@echo ""
	@echo "Database:"
	@echo "  make init-db     - Initialize database with sample data"
	@echo ""
	@echo "Development:"
	@echo "  make run         - Start development server"
	@echo "  make test        - Run tests"
	@echo "  make test-cov    - Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint        - Run linters (ruff, mypy)"
	@echo "  make format      - Format code (black, isort)"
	@echo "  make check       - Run all checks (lint + format check)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up   - Start Docker services"
	@echo "  make docker-down - Stop Docker services"
	@echo "  make docker-logs - View Docker logs"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean       - Remove generated files"
	@echo ""

install:
	pip install -r requirements-minimal.txt

install-dev:
	pip install -r requirements-dev.txt

init-db:
	python scripts/create_large_db.py

run:
	python scripts/run_dev_server.py

test:
	pytest backend/tests/ -v

test-cov:
	pytest backend/tests/ -v --cov=backend --cov-report=html --cov-report=term

lint:
	ruff check backend/
	mypy backend/

format:
	black backend/
	isort backend/

check: format lint

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "Cleanup complete"
