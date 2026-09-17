# Chapter 1 Notes

## Key Concepts

- MLOps applies software engineering and DevOps practices to machine learning systems.
- Reproducibility includes code, dependencies, data, models, configuration, and infrastructure.
- A Python scaffold gives the project a repeatable structure.
- Local quality checks should match CI quality checks.
- A failed quality gate must stop the pipeline.
- Virtual environments isolate Python dependencies.
- Container images isolate application runtime dependencies.

## Quality Gates

```bash
make format-check
make lint
make test
make all
```

## Current Lab Results

- Black: passed
- Pylint: 10.00/10
- Pytest: passed
- Test coverage: 75%
- Python CI matrix: 3.11, 3.12, and 3.13

## Improvement Backlog

- Increase test coverage from 75% to 100%.
- Validate the container build in CI.
- Add image vulnerability scanning in a later chapter.
- Separate development dependencies from runtime dependencies.
