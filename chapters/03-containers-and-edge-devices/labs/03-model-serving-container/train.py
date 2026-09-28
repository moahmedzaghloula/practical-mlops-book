"""Train and persist a deterministic regression model."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression

DEFAULT_MODEL_DIR = Path("model")


def make_dataset(
    sample_count: int = 500,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Create deterministic synthetic height and weight observations."""
    random_generator = np.random.default_rng(seed)

    heights_cm = random_generator.uniform(
        low=145.0,
        high=195.0,
        size=sample_count,
    )

    noise = random_generator.normal(
        loc=0.0,
        scale=4.0,
        size=sample_count,
    )

    weights_kg = (0.75 * heights_cm) - 55.0 + noise

    features = heights_cm.reshape(-1, 1)

    return features, weights_kg


def fingerprint_dataset(
    features: np.ndarray,
    targets: np.ndarray,
) -> str:
    """Return a SHA-256 fingerprint for the exact training arrays."""
    digest = hashlib.sha256()
    digest.update(features.tobytes())
    digest.update(targets.tobytes())
    return digest.hexdigest()


def train_model(
    model_dir: Path = DEFAULT_MODEL_DIR,
) -> tuple[Path, Path]:
    """Train the model and write its artifact and metadata."""
    features, targets = make_dataset()

    model = LinearRegression()
    model.fit(features, targets)

    model_version = os.getenv("MODEL_VERSION", "1.0.0")

    metadata = {
        "model_name": "height-to-weight-regressor",
        "model_version": model_version,
        "algorithm": "LinearRegression",
        "feature_names": ["height_cm"],
        "target_name": "weight_kg",
        "training_rows": int(features.shape[0]),
        "training_r2": round(float(model.score(features, targets)), 6),
        "dataset_sha256": fingerprint_dataset(features, targets),
        "random_seed": 42,
    }

    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / "model.joblib"
    metadata_path = model_dir / "metadata.json"

    model_bundle = {
        "model": model,
        "metadata": metadata,
    }

    joblib.dump(model_bundle, model_path)

    metadata_path.write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )

    return model_path, metadata_path


if __name__ == "__main__":
    saved_model, saved_metadata = train_model()
    print(f"Saved model: {saved_model}")
    print(f"Saved metadata: {saved_metadata}")
