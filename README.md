# Practical MLOps — Hands-On Study Repository

This repository contains my chapter-by-chapter study notes and hands-on labs for the book *Practical MLOps*.

The goal is to understand MLOps deeply from a DevOps engineering perspective and gradually build the foundations required for LLMOps.

## Environment

- Fedora Linux
- Python
- Git and GitHub Actions
- Podman and Docker
- Make

## Repository Structure

```text
chapters/
└── 01-introduction-to-mlops/
    ├── README.md
    ├── notes/
    └── labs/
        └── python-ci-scaffold/

shared/
└── scripts/
```

## Study Progress

- [x] Chapter 1 — Introduction to MLOps
- [ ] Chapter 2 — MLOps Foundations
- [ ] Chapter 3 — Containers and Edge Devices

## Run Chapter 1 Lab

```bash
cd chapters/01-introduction-to-mlops/labs/python-ci-scaffold

python3 -m venv .venv
source .venv/bin/activate

make all
```

## Build the Chapter 1 Container

```bash
cd chapters/01-introduction-to-mlops/labs/python-ci-scaffold

podman build \
  --tag localhost/practical-mlops-ch01:dev \
  .

podman run \
  --rm \
  localhost/practical-mlops-ch01:dev
```

## Repository Rules

- Each chapter will have its own notes and hands-on labs.
- Every Python lab should include automated tests.
- Formatting, linting, and tests must pass before committing.
- Secrets and credentials must never be committed.
- Book PDFs and copyrighted figures must not be uploaded.
- Virtual environments and generated artifacts must remain ignored.
