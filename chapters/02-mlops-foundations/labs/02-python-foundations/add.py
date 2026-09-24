#!/usr/bin/env python3

from random import Random


def add(x: int, y: int) -> int:
    """Return the sum of two integers."""
    return x + y


def main() -> None:
    random_generator = Random(42)
    numbers = range(1, 10)

    for _ in range(10):
        x = random_generator.choice(numbers)
        y = random_generator.choice(numbers)
        print(f"{x} + {y} = {add(x, y)}")


if __name__ == "__main__":
    main()
