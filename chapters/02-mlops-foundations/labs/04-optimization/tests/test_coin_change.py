"""Tests for the greedy coin-change algorithm."""

import pytest

from coin_change import calculate_value, greedy_change, total_coins


def test_change_for_99_cents() -> None:
    """The US coin system should represent 99 cents correctly."""

    change = greedy_change(99)

    assert change == {
        25: 3,
        10: 2,
        5: 0,
        1: 4,
    }

    assert total_coins(change) == 9
    assert calculate_value(change) == 99


def test_zero_amount() -> None:
    """Zero should require zero coins."""

    change = greedy_change(0)

    assert total_coins(change) == 0
    assert calculate_value(change) == 0


def test_negative_amount_fails() -> None:
    """Negative amounts should be rejected."""

    with pytest.raises(ValueError, match="cannot be negative"):
        greedy_change(-1)


def test_float_amount_fails() -> None:
    """Money should be passed as integer cents."""

    with pytest.raises(TypeError, match="integer"):
        greedy_change(1.5)


def test_empty_coin_list_fails() -> None:
    """At least one coin denomination is required."""

    with pytest.raises(ValueError, match="cannot be empty"):
        greedy_change(10, [])


def test_unrepresentable_amount_fails() -> None:
    """The algorithm should reject an impossible amount."""

    with pytest.raises(ValueError, match="Cannot represent"):
        greedy_change(3, [2])
