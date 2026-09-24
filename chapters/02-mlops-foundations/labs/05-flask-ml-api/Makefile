.PHONY: install train format format-check lint test run production all

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

train:
	python train.py

format:
	python -m black app.py train.py tests

format-check:
	python -m black --check app.py train.py tests

lint:
	python -m ruff check app.py train.py tests

test: train
	python -m pytest -vv --cov=app --cov=train --cov-report=term-missing tests

run: train
	python -m flask --app app run --debug

production: train
	python -m gunicorn --bind 0.0.0.0:8000 --workers 2 --threads 4 app:app

all: format-check lint test
