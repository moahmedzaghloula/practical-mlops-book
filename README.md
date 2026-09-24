# Practical MLOps — Hands-On Study Repository

[![Chapter 1 CI](https://github.com/moahmedzaghloula/practical-mlops-book/actions/workflows/ci.yml/badge.svg)](https://github.com/moahmedzaghloula/practical-mlops-book/actions/workflows/ci.yml)
[![Chapter 2 CI](https://github.com/moahmedzaghloula/practical-mlops-book/actions/workflows/chapter-02.yml/badge.svg)](https://github.com/moahmedzaghloula/practical-mlops-book/actions/workflows/chapter-02.yml)

A chapter-by-chapter, production-oriented study repository for *Practical MLOps*.
It connects machine learning workflows to the engineering practices used in
DevOps: reproducible environments, automated quality gates, CI/CD, containers,
testing, observability-minded APIs, and artifact lineage.

The long-term goal is to build a strong MLOps foundation before moving into
LLMOps.

> This repository contains original study notes and hands-on implementations.
> It does not redistribute the book or its copyrighted content.

## Learning Approach

Each chapter follows the same workflow:

1. Study the concepts in the book's original order.
2. Reproduce the examples locally on Fedora Linux.
3. Convert exploratory work into repeatable scripts.
4. Add formatting, linting, tests, and coverage.
5. Automate the workflow with Make and GitHub Actions.
6. Package deployable applications as containers where appropriate.
7. Record operational lessons that connect MLOps to DevOps and LLMOps.

## Study Progress

| Chapter | Topic | Status | Labs |
|---|---|---|---:|
| [01](chapters/01-introduction-to-mlops/) | Introduction to MLOps | Complete | 1 |
| [02](chapters/02-mlops-foundations/) | MLOps Foundations | In progress | 5 |
| 03 | Containers and Edge Devices | Not started | — |

## Repository Structure

```text
.
├── .github/workflows/
├── chapters/
│   ├── 01-introduction-to-mlops/
│   │   ├── README.md
│   │   ├── notes/
│   │   └── labs/python-ci-scaffold/
│   └── 02-mlops-foundations/
│       ├── README.md
│       └── labs/
│           ├── 01-bash-foundations/
│           ├── 02-python-foundations/
│           ├── 03-eda/
│           ├── 04-optimization/
│           └── 05-flask-ml-api/
├── .gitignore
└── README.md
```

## Implemented Labs

### Chapter 1

- Python project scaffold
- isolated environment and dependency files
- Black formatting and Pylint static analysis
- Pytest tests and coverage
- Make automation
- Python-version matrix CI
- container image build and execution

### Chapter 2

- Bash pipelines, redirection, sampling, and exit behavior
- Python scripting foundations
- reproducible EDA and dataset validation
- regression, KDE, and distribution visualizations
- greedy coin-change optimization
- TSP heuristics, random restarts, geocoding, and caching
- model training, metadata, and artifact generation
- Flask inference API with liveness and readiness endpoints
- API tests, Gunicorn serving, non-root containers, and CI

## Prerequisites

The local reference environment is Fedora Linux with Python 3.13+, Git, GNU
Make, and Podman or Docker.

```bash
sudo dnf install -y python3 python3-pip git make podman
```

## Running a Python Lab

```bash
cd chapters/02-mlops-foundations/labs/04-optimization
python3 -m venv .venv
source .venv/bin/activate
make install
make all
```

The common quality pipeline is:

```text
format check → lint → tests → coverage → runnable example
```

## Running the ML API

```bash
cd chapters/02-mlops-foundations/labs/05-flask-ml-api
python3 -m venv .venv
source .venv/bin/activate
make install
make all
make production
```

```bash
curl --silent http://127.0.0.1:8000/health
```

```bash
curl \
  --silent \
  --request POST \
  --header "Content-Type: application/json" \
  --data '{"height_inches":70}' \
  http://127.0.0.1:8000/predict
```

## Running the ML API Container

```bash
cd chapters/02-mlops-foundations/labs/05-flask-ml-api
podman build \
  --format docker \
  --tag practical-mlops/ch02-api:1.0.0 \
  .
```

```bash
podman run \
  --detach \
  --rm \
  --name ch02-ml-api \
  --publish 8000:8000 \
  practical-mlops/ch02-api:1.0.0
```

## Engineering Standards

- Keep each lab independently reproducible.
- Run every available quality gate before committing.
- Use dependency lock files for repeatable environments.
- Keep credentials, private datasets, virtual environments, and caches out of Git.
- Treat model files as generated artifacts unless a lab explicitly documents why
  a small artifact is versioned.
- Keep training, serving, validation, and testing concerns separated.
- Prefer deterministic experiments and record random seeds and model metadata.
- Do not upload book PDFs or copyrighted book figures.

## MLOps-to-DevOps Mapping

| DevOps practice | MLOps extension in this repository |
|---|---|
| Source control | Code, configuration, experiment metadata, and study history |
| CI | Code checks plus data, model, and API validation |
| Build artifact | Container image plus trained model artifact |
| Release metadata | Model version, metrics, dataset hash, and dependency versions |
| Health checks | Liveness and model-readiness endpoints |
| Reproducibility | Locked dependencies, seeds, deterministic scripts, and containers |

## Roadmap Toward LLMOps

- prompt and evaluation versioning
- embedding and vector-index lineage
- retrieval quality evaluation
- model and prompt serving
- token, latency, and cost monitoring
- safety and quality gates
- continuous evaluation and controlled rollout

## Disclaimer

This is an independent educational repository inspired by exercises studied
while reading *Practical MLOps*. It is not an official repository for the book.
