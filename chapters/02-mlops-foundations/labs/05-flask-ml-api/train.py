#!/usr/bin/env python3

"""Train and persist a simple height-to-weight regression model."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

PROJECT_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = PROJECT_DIR / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "height-weight-model.joblib"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"


def build_dataset(
    row_count: int = 2000,
    seed: int = 42,
) -> pd.DataFrame:
    """Create deterministic example training data."""

    random_generator = np.random.default_rng(seed)

    heights = random_generator.uniform(
        low=58,
        high=78,
        size=row_count,
    )

    noise = random_generator.normal(
        loc=0,
        scale=8,
        size=row_count,
    )

    weights = (3.2 * heights) - 85 + noise

    return pd.DataFrame(
        {
            "height_inches": heights,
            "weight_pounds": weights,
        }
    )


def dataframe_hash(dataframe: pd.DataFrame) -> str:
    """Calculate a reproducible fingerprint for the training dataset."""

    csv_bytes = dataframe.to_csv(
        index=False,
        float_format="%.10f",
    ).encode("utf-8")

    return hashlib.sha256(csv_bytes).hexdigest()


def main() -> None:
    """Train, evaluate, and save the model."""

    ARTIFACT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataset = build_dataset()

    features = dataset[["height_inches"]]
    target = dataset["weight_pounds"]

    (
        train_features,
        test_features,
        train_target,
        test_target,
    ) = train_test_split(
        features,
        target,
        test_size=0.20,
        random_state=42,
    )

    model = LinearRegression()

    model.fit(
        train_features,
        train_target,
    )

    predictions = model.predict(test_features)

    metrics = {
        "mean_absolute_error": float(
            mean_absolute_error(
                test_target,
                predictions,
            )
        ),
        "r2_score": float(
            r2_score(
                test_target,
                predictions,
            )
        ),
    }

    metadata = {
        "model_name": "height-weight-linear-regression",
        "model_version": "1.0.0",
        "trained_at_utc": datetime.now(UTC).isoformat(),
        "training_rows": len(train_features),
        "test_rows": len(test_features),
        "dataset_sha256": dataframe_hash(dataset),
        "feature_names": ["height_inches"],
        "target_name": "weight_pounds",
        "metrics": metrics,
    }

    artifact = {
        "model": model,
        "metadata": metadata,
    }

    joblib.dump(
        artifact,
        MODEL_PATH,
    )

    METRICS_PATH.write_text(
        json.dumps(
            metadata,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Model saved to: {MODEL_PATH}")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
