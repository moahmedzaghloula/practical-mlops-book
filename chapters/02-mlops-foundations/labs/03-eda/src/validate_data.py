#!/usr/bin/env python3

"""Validate the raw height and weight dataset."""

from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "raw" / "height-weight-25k.csv"

REQUIRED_COLUMNS = {
    "Index",
    "Height-Inches",
    "Weight-Pounds",
}


def validate_dataset(data_path: Path) -> pd.DataFrame:
    """Load and validate the dataset."""

    if not data_path.exists():
        raise FileNotFoundError(f"Dataset does not exist: {data_path}")

    dataframe = pd.read_csv(data_path)

    if dataframe.empty:
        raise ValueError("Dataset is empty")

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )

    if dataframe[list(REQUIRED_COLUMNS)].isnull().any().any():
        raise ValueError("Dataset contains missing values")

    if not dataframe["Height-Inches"].between(40, 100).all():
        raise ValueError("Height-Inches contains values outside the accepted range")

    if not dataframe["Weight-Pounds"].between(40, 500).all():
        raise ValueError("Weight-Pounds contains values outside the accepted range")

    if dataframe["Index"].duplicated().any():
        raise ValueError("Index contains duplicate values")

    return dataframe


def main() -> None:
    """Run validation and print a short report."""

    dataframe = validate_dataset(DATA_PATH)

    print("Dataset validation passed")
    print(f"Path: {DATA_PATH}")
    print(f"Rows: {len(dataframe)}")
    print(f"Columns: {len(dataframe.columns)}")
    print(f"Column names: {list(dataframe.columns)}")


if __name__ == "__main__":
    main()
