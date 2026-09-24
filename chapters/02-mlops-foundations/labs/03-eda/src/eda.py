#!/usr/bin/env python3

"""Perform exploratory data analysis on the height and weight dataset."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from validate_data import validate_dataset


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "raw" / "height-weight-25k.csv"
FIGURES_DIR = PROJECT_DIR / "figures"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"


def inches_to_centimeters(value: pd.Series) -> pd.Series:
    """Convert inches to centimeters."""

    return value * 2.54


def pounds_to_kilograms(value: pd.Series) -> pd.Series:
    """Convert pounds to kilograms."""

    return value * 0.45359237


def main() -> None:
    """Run the complete EDA workflow."""

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    dataframe = validate_dataset(DATA_PATH)

    print("\nDataset shape:")
    print(dataframe.shape)

    print("\nFirst five rows:")
    print(dataframe.head())

    print("\nData types:")
    print(dataframe.dtypes)

    print("\nMissing values:")
    print(dataframe.isnull().sum())

    numeric_columns = [
        "Height-Inches",
        "Weight-Pounds",
    ]

    descriptive_statistics = dataframe[numeric_columns].describe()

    print("\nDescriptive statistics:")
    print(descriptive_statistics)

    descriptive_statistics.to_csv(
        PROCESSED_DIR / "descriptive-statistics.csv"
    )

    correlation = dataframe[numeric_columns].corr()

    print("\nCorrelation matrix:")
    print(correlation)

    correlation.to_csv(PROCESSED_DIR / "correlation-matrix.csv")

    dataframe["Height-Centimeters"] = inches_to_centimeters(
        dataframe["Height-Inches"]
    )

    dataframe["Weight-Kilograms"] = pounds_to_kilograms(
        dataframe["Weight-Pounds"]
    )

    dataframe.to_csv(
        PROCESSED_DIR / "height-weight-clean.csv",
        index=False,
    )

    sns.set_theme(style="whitegrid")

    regression_plot = sns.lmplot(
        data=dataframe,
        x="Height-Inches",
        y="Weight-Pounds",
        height=7,
        aspect=1.2,
        scatter_kws={
            "alpha": 0.20,
            "s": 12,
        },
        line_kws={
            "color": "red",
            "linewidth": 2,
        },
    )

    regression_plot.set_axis_labels(
        "Height (inches)",
        "Weight (pounds)",
    )

    regression_plot.figure.suptitle(
        "Height versus Weight with Linear Regression",
        y=1.02,
    )

    regression_plot.figure.savefig(
        FIGURES_DIR / "height-weight-regression.png",
        dpi=160,
        bbox_inches="tight",
    )

    plt.close(regression_plot.figure)

    kde_plot = sns.jointplot(
        data=dataframe,
        x="Height-Inches",
        y="Weight-Pounds",
        kind="kde",
        fill=True,
        cmap="mako",
        height=8,
    )

    kde_plot.set_axis_labels(
        "Height (inches)",
        "Weight (pounds)",
    )

    kde_plot.figure.suptitle(
        "Joint Density of Height and Weight",
        y=1.02,
    )

    kde_plot.figure.savefig(
        FIGURES_DIR / "height-weight-kde.png",
        dpi=160,
        bbox_inches="tight",
    )

    plt.close(kde_plot.figure)

    figure, axes = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(13, 5),
    )

    sns.histplot(
        data=dataframe,
        x="Height-Inches",
        kde=True,
        ax=axes[0],
    )

    axes[0].set_title("Height Distribution")
    axes[0].set_xlabel("Height (inches)")

    sns.histplot(
        data=dataframe,
        x="Weight-Pounds",
        kde=True,
        ax=axes[1],
    )

    axes[1].set_title("Weight Distribution")
    axes[1].set_xlabel("Weight (pounds)")

    figure.tight_layout()

    figure.savefig(
        FIGURES_DIR / "height-weight-distributions.png",
        dpi=160,
        bbox_inches="tight",
    )

    plt.close(figure)

    print("\nGenerated files:")

    for path in sorted(FIGURES_DIR.glob("*.png")):
        print(path)


if __name__ == "__main__":
    main()

