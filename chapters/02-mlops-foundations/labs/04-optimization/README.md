# Lab 04 — Optimization and Traveling Salesperson Heuristics

This lab compares fast local decisions with global optimization. It implements
greedy coin change, a nearest-neighbor Traveling Salesperson heuristic, random
restarts, and API-backed coordinate lookup.

## Setup

```bash
cd chapters/02-mlops-foundations/labs/04-optimization
python3 -m venv .venv
source .venv/bin/activate
make install
```

## Run All Offline Quality Gates

```bash
make all
```

The target runs Black, Ruff, Pytest with coverage, the coin-change example, and
the deterministic TSP example.

## Greedy Coin Change

```bash
python coin_change.py 99
```

```bash
python coin_change.py 6 --coins 4 3 1
```

The second command demonstrates a greedy limitation: `4 + 1 + 1` uses three
coins, while the global optimum `3 + 3` uses two.

## Traveling Salesperson Heuristic

```bash
python tsp.py --iterations 1000 --seed 42
```

The implementation chooses a start, repeatedly selects the nearest unvisited
city, closes the tour, repeats from random starts, and keeps the best route. The
seed makes the restart sequence reproducible.

## API-Backed Coordinate Exercise

```bash
make restaurant-tsp
```

`restaurant_tsp.py` queries OpenStreetMap Nominatim, tries fallback search
strings, applies timeouts and HTTP error handling, and caches resolved
coordinates in `restaurant-coordinates.json`.

The live API exercise is excluded from `make all`; offline CI should not fail
because a public third-party service is unavailable or rate-limited.

## Important Limitation

The example calculates Euclidean distance between coordinates. A production
routing system should use road-network distance, travel time, and possibly live
traffic from an appropriate routing engine.
