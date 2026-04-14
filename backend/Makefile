.PHONY: lint lint-fix format dev start install prepare init-db migrate test test-cov prestart

install:
	pip install -r requirements.txt

prepare:
	pre-commit install

init-db:
	python src/db/create_db.py

migrate:
	python -m alembic upgrade head

lint:
	ruff check .

lint-fix:
	ruff check --fix .

format:
	black .

dev:
	python dev.py

start:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

test:
	python -m pytest tests/ -q

test-cov:
	python -m pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=70

prestart:
	bash scripts/prestart.sh
