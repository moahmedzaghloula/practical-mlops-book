"""Tests for dataset validation."""

from pathlib import Path

import pandas as pd
import pytest

from src.validate_data import validate_dataset


def write_dataset(path: Path, rows: list[dict]) -> None:
    """Write test rows to a CSV file."""

    pd.DataFrame(rows).to_csv(path, index=False)


def valid_rows() -> list[dict]:
    """Return a minimal valid dataset."""

    return [
        {
            "Index": 1,
            "Height-Inches": 65.0,
            "Weight-Pounds": 120.0,
        },
        {
            "Index": 2,
            "Height-Inches": 70.0,
            "Weight-Pounds": 160.0,
        },
    ]


def test_valid_dataset_passes(tmp_path: Path) -> None:
    """A valid dataset should pass validation."""

    data_path = tmp_path / "valid.csv"
    write_dataset(data_path, valid_rows())

    dataframe = validate_dataset(data_path)

    assert len(dataframe) == 2


def test_missing_column_fails(tmp_path: Path) -> None:
    """A dataset with a missing column should fail."""

    rows = valid_rows()

    for row in rows:
        del row["Weight-Pounds"]

    data_path = tmp_path / "missing-column.csv"
    write_dataset(data_path, rows)

    with pytest.raises(ValueError, match="missing required columns"):
        validate_dataset(data_path)


def test_duplicate_index_fails(tmp_path: Path) -> None:
    """Duplicate indexes should fail."""

    rows = valid_rows()
    rows[1]["Index"] = 1

    data_path = tmp_path / "duplicate.csv"
    write_dataset(data_path, rows)

    with pytest.raises(ValueError, match="duplicate"):
        validate_dataset(data_path)


def test_invalid_height_fails(tmp_path: Path) -> None:
    """An unrealistic height should fail."""

    rows = valid_rows()
    rows[0]["Height-Inches"] = 400

    data_path = tmp_path / "invalid-height.csv"
    write_dataset(data_path, rows)

    with pytest.raises(ValueError, match="Height-Inches"):
        validate_dataset(data_path)
