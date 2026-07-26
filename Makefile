.PHONY: build up down shell test check chapter6-deps

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

shell: up
	docker compose exec dev bash

test:
	docker compose run --rm dev python -m compileall -q chapter4 chapter6 chapter7
	docker compose run --rm dev env PYTHONPATH=/workspace/chapter7:/workspace pytest -q chapter7/tests

check: test

chapter6-deps: up
	docker compose exec dev pip install -r chapter6/LangGraph/requirements.txt -r chapter6/AutoGen/requirements.txt
