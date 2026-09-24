.PHONY: install validate analyze test notebook all

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

validate:
	python src/validate_data.py

analyze: validate
	python src/eda.py

test:
	python -m pytest -vv --cov=src --cov-report=term-missing tests

notebook:
	python -m jupyter lab --no-browser

all: validate analyze test
