.PHONY: all install lint test format format-check

all: install format-check lint test

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

lint:
	python -m pylint --disable=R,C hello.py test_hello.py

test:
	python -m pytest -vv --cov=hello --cov-report=term-missing test_hello.py

format:
	python -m black hello.py test_hello.py

format-check:
	python -m black --check hello.py test_hello.py
