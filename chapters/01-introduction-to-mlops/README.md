# Chapter 1 — Introduction to MLOps

## Topics Covered

- What MLOps means
- The relationship between DevOps and MLOps
- Python project scaffolding
- Virtual environments
- Dependency management
- Formatting with Black
- Static analysis with Pylint
- Testing with Pytest
- Test coverage
- Automation with Make
- CI with GitHub Actions
- Containerizing a Python application

## Hands-On Lab

The Python CI scaffold is located at:

```text
labs/python-ci-scaffold/
```

## Lab Quality Gates

```bash
cd labs/python-ci-scaffold
source .venv/bin/activate
make all
```

The CI workflow validates the project across Python 3.11, 3.12, and 3.13.
