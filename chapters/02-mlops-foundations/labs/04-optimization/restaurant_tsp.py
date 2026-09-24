#!/usr/bin/env python3

"""Geocode Alexandria locations and solve a small TSP route."""

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from tsp import best_of_random_starts, format_closed_route

CACHE_PATH = Path("restaurant-coordinates.json")

LOCATION_QUERIES: dict[str, list[str]] = {
    "San Stefano": [
        "San Stefano Mall, Alexandria, Egypt",
        "San Stefano, Alexandria, Egypt",
    ],
    "City Centre Alexandria": [
        "City Centre Alexandria, Egypt",
        "City Centre, Alexandria, Egypt",
        "Smouha, Alexandria, Egypt",
    ],
    "Bibliotheca Alexandrina": [
        "Bibliotheca Alexandrina, Alexandria, Egypt",
        "Library of Alexandria, Egypt",
        "Al Shatby, Alexandria, Egypt",
    ],
    "Stanley Bridge": [
        "Stanley Bridge, Alexandria, Egypt",
        "Stanley, Alexandria, Egypt",
    ],
}


def request_coordinates(query: str) -> tuple[float, float] | None:
    """Send one geocoding request to Nominatim."""

    encoded_query = urllib.parse.urlencode(
        {
            "q": query,
            "format": "jsonv2",
            "limit": 1,
            "countrycodes": "eg",
            "addressdetails": 1,
        }
    )

    url = f"https://nominatim.openstreetmap.org/search?{encoded_query}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": ("practical-mlops-book-study/1.0 " "(educational-project)"),
            "Accept": "application/json",
            "Accept-Language": "en",
        },
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=30,
        ) as response:
            results: list[dict[str, Any]] = json.load(response)

    except urllib.error.HTTPError as error:
        raise RuntimeError(
            f"Nominatim returned HTTP {error.code} for query: {query}"
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Network error while geocoding {query}: {error.reason}"
        ) from error

    if not results:
        return None

    first_result = results[0]

    print(f"  Match: {first_result.get('display_name', 'Unknown')}")

    return (
        float(first_result["lat"]),
        float(first_result["lon"]),
    )


def geocode_with_fallbacks(
    location_name: str,
    queries: list[str],
) -> tuple[float, float]:
    """Try multiple queries until Nominatim returns a match."""

    for attempt_number, query in enumerate(
        queries,
        start=1,
    ):
        print(f"  Attempt {attempt_number}/{len(queries)}: {query}")

        coordinates = request_coordinates(query)

        if coordinates is not None:
            return coordinates

        print("  No match; trying the next query.")

        # Keep requests separated when using a public geocoding service.
        time.sleep(1)

    raise ValueError(f"No coordinates found for location: {location_name}")


def load_cached_coordinates() -> dict[str, tuple[float, float]] | None:
    """Load coordinates from the local JSON cache."""

    if not CACHE_PATH.exists():
        return None

    print(f"Loading cached coordinates from: {CACHE_PATH}")

    raw_coordinates = json.loads(CACHE_PATH.read_text(encoding="utf-8"))

    coordinates = {
        name: (float(value[0]), float(value[1]))
        for name, value in raw_coordinates.items()
    }

    expected_locations = set(LOCATION_QUERIES)
    cached_locations = set(coordinates)

    if cached_locations != expected_locations:
        print("Cache does not match the configured locations.")
        print("Ignoring the old cache.")
        return None

    return coordinates


def save_coordinates(
    coordinates: dict[str, tuple[float, float]],
) -> None:
    """Persist coordinates to avoid repeated API calls."""

    CACHE_PATH.write_text(
        json.dumps(
            coordinates,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"Coordinates cached in: {CACHE_PATH}")


def load_or_create_coordinates() -> dict[str, tuple[float, float]]:
    """Load coordinates from cache or obtain them from Nominatim."""

    cached_coordinates = load_cached_coordinates()

    if cached_coordinates is not None:
        return cached_coordinates

    coordinates: dict[str, tuple[float, float]] = {}

    for location_name, queries in LOCATION_QUERIES.items():
        print(f"\nGeocoding location: {location_name}")

        coordinates[location_name] = geocode_with_fallbacks(
            location_name,
            queries,
        )

        # Avoid rapid requests to the public Nominatim instance.
        time.sleep(1)

    save_coordinates(coordinates)

    return coordinates


def main() -> None:
    """Geocode configured locations and calculate a route."""

    coordinates = load_or_create_coordinates()

    print("\nResolved coordinates:")

    for location_name, coordinate in coordinates.items():
        print(
            f"  {location_name}: "
            f"latitude={coordinate[0]:.6f}, "
            f"longitude={coordinate[1]:.6f}"
        )

    route, distance = best_of_random_starts(
        coordinates,
        iterations=1000,
        seed=42,
    )

    print("\nTSP result:")
    print(f"Route: {format_closed_route(route)}")
    print(f"Coordinate-space distance: {distance:.6f}")


if __name__ == "__main__":
    main()
