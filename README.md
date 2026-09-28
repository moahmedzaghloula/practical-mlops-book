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
| [02](chapters/02-mlops-foundations/) | MLOps Foundations | Complete | 5 |
| [03](chapters/03-containers-and-edge-devices/) | MLOps for Containers and Edge Devices | In progress | 5 |

`In progress` means the chapter implementation is being built and verified lab
by lab. A chapter is marked `Complete` only after its required local checks and
GitHub Actions workflows pass.

## Repository Structure

```text
.
├── .github/workflows/
├── chapters/
│   ├── 01-introduction-to-mlops/
│   │   ├── README.md
│   │   ├── notes/
│   │   └── labs/python-ci-scaffold/
│   ├── 02-mlops-foundations/
│   │   ├── README.md
│   │   └── labs/
│   │       ├── 01-bash-foundations/
│   │       ├── 02-python-foundations/
│   │       ├── 03-eda/
│   │       ├── 04-optimization/
│   │       └── 05-flask-ml-api/
│   └── 03-containers-and-edge-devices/
│       ├── README.md
│       └── labs/
│           ├── 01-container-basics/
│           ├── 02-container-quality-security/
│           ├── 03-model-serving-container/
│           ├── 04-edge-inference-cpu/
│           └── 05-edge-tpu-compiler/
├── .gitignore
└── README.md
```

## Labs and Study Coverage

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

### Chapter 3 — In Progress

- Fedora-native, rootless container workflows with Podman
- image layers, tags, digests, OCI labels, and registry concepts
- Dockerfile `RUN`, `ENTRYPOINT`, and `CMD` behavior
- interactive debugging with `podman exec`
- Dockerfile linting with Hadolint
- OCI image export and vulnerability scanning with Grype
- non-root and read-only container hardening
- deterministic model training and artifact metadata
- Flask and Gunicorn model serving with input validation
- liveness, readiness, metadata, and prediction endpoints
- TensorFlow Lite conversion and quantization concepts
- CPU-based edge inference simulation
- legacy Coral Edge TPU compiler workflow and compatibility limits
- managed-ML container patterns and build-once/run-many tradeoffs

## Prerequisites

The local reference environment is Fedora Linux with Python 3.13+, Git, GNU
Make, and rootless Podman. Docker-compatible files are retained because the
same images are validated by GitHub Actions with Docker.

```bash
sudo dnf install -y \
  python3 \
  python3-pip \
  git \
  make \
  podman \
  buildah \
  skopeo \
  fuse-overlayfs \
  curl \
  jq
```

Verify the local container environment:

```bash
podman version
podman info --format '{{.Host.Security.Rootless}}'
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

## Running the Chapter 3 Container Labs

Build and run the container-fundamentals image:

```bash
cd chapters/03-containers-and-edge-devices/labs/01-container-basics
podman build \
  --tag localhost/ch03-container-basics:1.0.0 \
  .
podman run \
  --rm \
  localhost/ch03-container-basics:1.0.0
```

Run the Dockerfile quality checks and non-root smoke test:

```bash
cd ../02-container-quality-security
make verify
```

Build, test, and containerize the model-serving API:

```bash
cd ../03-model-serving-container
python3 -m venv .venv
source .venv/bin/activate
make install
make format
make all
make container-build
```

Start the model API:

```bash
podman run \
  --detach \
  --name ch03-model-api \
  --publish 8000:8000 \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --cap-drop=all \
  --security-opt=no-new-privileges \
  localhost/ch03-model-api:1.0.0
```

Validate the running service:

```bash
curl --fail --silent \
  http://127.0.0.1:8000/health \
  | jq .
```

```bash
curl \
  --fail \
  --silent \
  --request POST \
  --header 'Content-Type: application/json' \
  --data '{"height_cm":175.0}' \
  http://127.0.0.1:8000/predict \
  | jq .
```

Stop and remove the named container after testing:

```bash
podman stop ch03-model-api
podman rm ch03-model-api
```

## Edge Lab Scope

The CPU edge-inference lab is reproducible without specialized hardware. The
Coral Edge TPU lab is explicitly marked as conditional because it depends on
legacy upstream packages, a compatible compiler, and optional USB hardware. A
legacy upstream failure is documented as a compatibility constraint rather
than hidden with an unsupported host modification.

## Engineering Standards

- Keep each lab independently reproducible.
- Run every available quality gate before committing.
- Use dependency lock files for repeatable environments.
- Keep credentials, private datasets, virtual environments, and caches out of Git.
- Treat model files as generated artifacts unless a lab explicitly documents why
  a small artifact is versioned.
- Run containers as a non-root user and drop unnecessary privileges where
  practical.
- Lint Dockerfiles and scan images for known vulnerabilities before release.
- Never place credentials in Dockerfile `ARG`, `ENV`, image layers, or Git.
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
| Supply-chain checks | Dockerfile linting, dependency pinning, and CVE scanning |
| Runtime hardening | Non-root users, read-only filesystems, reduced capabilities |
| Edge delivery | Quantized models, hardware compatibility, and offline inference |

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
