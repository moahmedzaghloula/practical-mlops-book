PYTHON ?= python
MODEL_VERSION ?= 1.0.0
IMAGE ?= localhost/ch03-model-api:1.0.0
PYTHON_FILES = app.py train.py tests

.PHONY: install train format format-check lint test all container-build

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements-dev.txt

train:
	MODEL_VERSION=$(MODEL_VERSION) $(PYTHON) train.py

format:
	$(PYTHON) -m black $(PYTHON_FILES)

format-check:
	$(PYTHON) -m black --check $(PYTHON_FILES)

lint:
	$(PYTHON) -m ruff check $(PYTHON_FILES)

test: train
	$(PYTHON) -m pytest \
		-vv \
		--cov=app \
		--cov=train \
		--cov-report=term-missing \
		tests

all: format-check lint test

container-build:
	podman build \
		--build-arg MODEL_VERSION=$(MODEL_VERSION) \
		--tag $(IMAGE) \
		.
