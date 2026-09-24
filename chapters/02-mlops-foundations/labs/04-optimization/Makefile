.PHONY: install format format-check lint test coin tsp restaurant-tsp all

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
format:
	python -m black coin_change.py tsp.py restaurant_tsp.py tests

format-check:
	python -m black --check coin_change.py tsp.py restaurant_tsp.py tests

lint:
	python -m ruff check coin_change.py tsp.py restaurant_tsp.py tests

test:
	python -m pytest -vv --cov=coin_change --cov=tsp --cov-report=term-missing tests

coin:
	python coin_change.py 99

tsp:
	python tsp.py --iterations 1000 --seed 42

restaurant-tsp:
	python restaurant_tsp.py

all: format-check lint test coin tsp
