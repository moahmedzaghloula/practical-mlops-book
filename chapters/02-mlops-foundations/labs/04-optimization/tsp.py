#!/usr/bin/env python3

"""Nearest-neighbor heuristic for the Traveling Salesperson Problem."""

import argparse
import math
import random
from collections.abc import Mapping, Sequence
from itertools import pairwise

Coordinate = tuple[float, float]

DEFAULT_CITIES: dict[str, Coordinate] = {
    "Alexandria": (31.2001, 29.9187),
    "Cairo": (30.0444, 31.2357),
    "Damanhour": (31.0341, 30.4682),
    "Tanta": (30.7865, 31.0004),
    "Mansoura": (31.0409, 31.3785),
    "Zagazig": (30.5877, 31.5020),
}


def euclidean_distance(
    first: Coordinate,
    second: Coordinate,
) -> float:
    """Calculate Euclidean distance between two points."""

    return math.dist(first, second)


def route_distance(
    route: Sequence[str],
    coordinates: Mapping[str, Coordinate],
) -> float:
    """Calculate the closed-tour distance."""

    if len(route) < 2:
        return 0.0

    total = 0.0

    for current, following in pairwise(route):
        total += euclidean_distance(
            coordinates[current],
            coordinates[following],
        )

    total += euclidean_distance(
        coordinates[route[-1]],
        coordinates[route[0]],
    )

    return total


def nearest_neighbor_route(
    coordinates: Mapping[str, Coordinate],
    start: str,
) -> list[str]:
    """Build a route by repeatedly selecting the nearest unvisited city."""

    if not coordinates:
        raise ValueError("coordinates cannot be empty")

    if start not in coordinates:
        raise ValueError(f"Unknown starting city: {start}")

    route = [start]
    unvisited = set(coordinates) - {start}

    while unvisited:
        current = route[-1]

        nearest = min(
            unvisited,
            key=lambda city: (
                euclidean_distance(
                    coordinates[current],
                    coordinates[city],
                ),
                city,
            ),
        )

        route.append(nearest)
        unvisited.remove(nearest)

    return route


def best_of_random_starts(
    coordinates: Mapping[str, Coordinate],
    iterations: int = 100,
    seed: int = 42,
) -> tuple[list[str], float]:
    """Run nearest-neighbor search from randomly selected starting cities."""

    if iterations <= 0:
        raise ValueError("iterations must be positive")

    if not coordinates:
        raise ValueError("coordinates cannot be empty")

    random_generator = random.Random(seed)
    city_names = list(coordinates)

    best_route: list[str] | None = None
    best_distance = math.inf

    for _ in range(iterations):
        start = random_generator.choice(city_names)

        route = nearest_neighbor_route(
            coordinates,
            start,
        )

        distance = route_distance(
            route,
            coordinates,
        )

        if distance < best_distance:
            best_route = route
            best_distance = distance

    if best_route is None:
        raise RuntimeError("No route was generated")

    return best_route, best_distance


def format_closed_route(route: Sequence[str]) -> str:
    """Format a route showing the return to its starting point."""

    if not route:
        return ""

    return " -> ".join([*route, route[0]])


def main() -> None:
    """CLI entry point."""

    parser = argparse.ArgumentParser(
        description="Solve a small TSP using nearest-neighbor random restarts."
    )

    parser.add_argument(
        "--iterations",
        type=int,
        default=100,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    args = parser.parse_args()

    route, distance = best_of_random_starts(
        DEFAULT_CITIES,
        iterations=args.iterations,
        seed=args.seed,
    )

    print(f"Route: {format_closed_route(route)}")
    print(f"Euclidean distance: {distance:.4f}")


if __name__ == "__main__":
    main()
