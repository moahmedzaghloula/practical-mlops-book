# Lab 01 — Bash Foundations

This lab practices shell behaviors used to connect data and ML tools inside
local automation and CI/CD pipelines.

## Objectives

- create deterministic input files
- redirect standard output and standard error independently
- connect commands with pipelines
- sample records with `shuf`
- count and inspect generated data

## Files

| File | Purpose |
|---|---|
| `input.txt` | Small deterministic input fixture |
| `numbers.txt` | Sequence used for sampling |
| `sample.txt` | Random sample generated with `shuf` |
| `stdout.log` | Captured standard output |
| `stderr.log` | Captured standard error |

## Reproduce the Exercises

```bash
printf '%s\n' alpha beta gamma > input.txt
wc -l input.txt
cat input.txt | wc -l
```

```bash
seq 1 1000 > numbers.txt
shuf -n 10 numbers.txt > sample.txt
wc -l sample.txt
```

```bash
ls input.txt missing.txt > stdout.log 2> stderr.log || true
```

```bash
cat stdout.log
cat stderr.log
```

## Why It Matters

ML workflows often connect command-line programs: download data, validate it,
train a model, evaluate it, and publish an artifact. Stream handling and exit
behavior determine whether automation reports failure or silently continues.
