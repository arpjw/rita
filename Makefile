.PHONY: dev build test lint

dev:
	docker-compose up --build

build:
	docker-compose build

test:
	python -m pytest tests/ -v

lint:
	ruff check .
