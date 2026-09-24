# Chapter 1 — Introduction to MLOps

Chapter 1 establishes the engineering baseline used throughout this repository:
a small Python project that is reproducible, testable, automated, and ready for
continuous integration.

## Learning Objectives

- distinguish MLOps from traditional DevOps without treating them as unrelated
- scaffold a maintainable Python project
- isolate dependencies with a virtual environment
- automate developer tasks with Make
- enforce formatting and static-analysis rules
- run tests and measure coverage
- validate multiple Python versions in CI
- package a Python application in a container image

## Concepts Covered

- MLOps and the machine learning lifecycle
- DevOps practices applied to ML systems
- Python project scaffolding and virtual environments
- dependency files and dependency locking
- Black, Pylint, Pytest, and coverage
- Make targets and GitHub Actions matrix builds
- container images

## Chapter Structure

```text
01-introduction-to-mlops/
├── README.md
├── notes/chapter-notes.md
└── labs/python-ci-scaffold/
    ├── Dockerfile
    ├── Makefile
    ├── hello.py
    ├── requirements.lock.txt
    ├── requirements.txt
    └── test_hello.py
```

## Run the Hands-On Lab

```bash
cd chapters/01-introduction-to-mlops/labs/python-ci-scaffold
python3 -m venv .venv
source .venv/bin/activate
make all
```

`make all` installs dependencies, verifies formatting, runs static analysis,
and executes tests with coverage.

## Individual Quality Gates

```bash
make install
make format-check
make lint
make test
```

Apply formatting with:

```bash
make format
```

## Container Lab

```bash
podman build \
  --tag practical-mlops/ch01:dev \
  chapters/01-introduction-to-mlops/labs/python-ci-scaffold
```

```bash
podman run --rm practical-mlops/ch01:dev
```

## Continuous Integration

The workflow at [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)
validates the lab across Python 3.11, 3.12, and 3.13. A separate job builds and
runs the container image.

## Production Connection

```text
source code → format → lint → test → coverage → container
```

Later chapters extend this delivery contract with datasets, trained models,
model metadata, inference APIs, and deployment checks.

## Key Takeaways

- A repeatable project structure is part of the product.
- Local and CI commands should share the same automation entry points.
- Dependency isolation prevents system packages from hiding failures.
- A container packages the runtime, but tests define expected behavior.
- MLOps builds on DevOps and adds data and model lifecycle concerns.
