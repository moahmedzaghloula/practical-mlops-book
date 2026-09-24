#!/usr/bin/env python3

"""Greedy coin-change implementation."""

import argparse
from collections.abc import Sequence

DEFAULT_COINS = (25, 10, 5, 1)


def greedy_change(
    amount_cents: int,
    coins: Sequence[int] = DEFAULT_COINS,
) -> dict[int, int]:
    """Return the greedy coin selection for an integer amount."""

    if isinstance(amount_cents, bool) or not isinstance(amount_cents, int):
        raise TypeError("amount_cents must be an integer")

    if amount_cents < 0:
        raise ValueError("amount_cents cannot be negative")

    if not coins:
        raise ValueError("coins cannot be empty")

    if any(
        isinstance(coin, bool) or not isinstance(coin, int) or coin <= 0
        for coin in coins
    ):
        raise ValueError("every coin must be a positive integer")

    ordered_coins = sorted(set(coins), reverse=True)

    remainder = amount_cents
    result: dict[int, int] = {}

    for coin in ordered_coins:
        count, remainder = divmod(remainder, coin)
        result[coin] = count

    if remainder != 0:
        raise ValueError(f"Cannot represent {amount_cents} using coins {ordered_coins}")

    return result


def total_coins(change: dict[int, int]) -> int:
    """Return the total number of selected coins."""

    return sum(change.values())


def calculate_value(change: dict[int, int]) -> int:
    """Calculate the total monetary value of the selected coins."""

    return sum(coin * count for coin, count in change.items())


def main() -> None:
    """CLI entry point."""

    parser = argparse.ArgumentParser(
        description="Calculate change using a greedy algorithm."
    )

    parser.add_argument(
        "amount",
        type=int,
        help="Amount expressed as integer cents",
    )

    parser.add_argument(
        "--coins",
        type=int,
        nargs="+",
        default=list(DEFAULT_COINS),
        help="Available coin denominations",
    )

    args = parser.parse_args()

    change = greedy_change(args.amount, args.coins)

    print(f"Amount: {args.amount} cents")

    for coin, count in change.items():
        print(f"{coin:>3}-cent coin: {count}")

    print(f"Total coins: {total_coins(change)}")
    print(f"Calculated value: {calculate_value(change)} cents")


if __name__ == "__main__":
    main()
