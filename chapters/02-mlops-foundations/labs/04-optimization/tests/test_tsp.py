"""Tests for the Traveling Salesperson heuristic."""

import pytest

from tsp import (
    DEFAULT_CITIES,
    best_of_random_starts,
    nearest_neighbor_route,
    route_distance,
)


def test_route_visits_every_city_once() -> None:
    """The route should contain every city exactly once."""

    route = nearest_neighbor_route(
        DEFAULT_CITIES,
        "Alexandria",
    )

    assert len(route) == len(DEFAULT_CITIES)
    assert len(set(route)) == len(DEFAULT_CITIES)
    assert set(route) == set(DEFAULT_CITIES)


def test_route_starts_at_requested_city() -> None:
    """The requested starting city should be first."""

    route = nearest_neighbor_route(
        DEFAULT_CITIES,
        "Cairo",
    )

    assert route[0] == "Cairo"


def test_unknown_start_fails() -> None:
    """An unknown city should be rejected."""

    with pytest.raises(ValueError, match="Unknown"):
        nearest_neighbor_route(
            DEFAULT_CITIES,
            "London",
        )


def test_random_restarts_are_reproducible() -> None:
    """The same seed should produce the same result."""

    first_route, first_distance = best_of_random_starts(
        DEFAULT_CITIES,
        iterations=100,
        seed=42,
    )

    second_route, second_distance = best_of_random_starts(
        DEFAULT_CITIES,
        iterations=100,
        seed=42,
    )

    assert first_route == second_route
    assert first_distance == second_distance


def test_route_distance_is_positive() -> None:
    """A multi-city closed route should have a positive distance."""

    route = nearest_neighbor_route(
        DEFAULT_CITIES,
        "Alexandria",
    )

    assert route_distance(route, DEFAULT_CITIES) > 0
