#!/usr/bin/env python3

"""Serve the trained regression model through a Flask API."""

import math
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from flask import Flask, jsonify, request

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "artifacts" / "height-weight-model.joblib"

app = Flask(__name__)


def load_model_artifact() -> dict[str, Any] | None:
    """Load the local model artifact if it exists."""

    if not MODEL_PATH.exists():
        return None

    return joblib.load(MODEL_PATH)


model_artifact = load_model_artifact()


@app.get("/health")
def health() -> tuple[Any, int]:
    """Liveness endpoint."""

    return (
        jsonify(
            {
                "status": "alive",
            }
        ),
        200,
    )


@app.get("/ready")
def ready() -> tuple[Any, int]:
    """Readiness endpoint."""

    if model_artifact is None:
        return (
            jsonify(
                {
                    "status": "not-ready",
                    "reason": "model artifact is unavailable",
                }
            ),
            503,
        )

    return (
        jsonify(
            {
                "status": "ready",
                "model_version": model_artifact["metadata"]["model_version"],
            }
        ),
        200,
    )


@app.post("/predict")
def predict() -> tuple[Any, int]:
    """Generate a weight prediction from a height."""

    if model_artifact is None:
        return (
            jsonify(
                {
                    "error": "model artifact is unavailable",
                }
            ),
            503,
        )

    if not request.is_json:
        return (
            jsonify(
                {
                    "error": "Content-Type must be application/json",
                }
            ),
            415,
        )

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return (
            jsonify(
                {
                    "error": "Request body must be a JSON object",
                }
            ),
            400,
        )

    height_value = payload.get("height_inches")

    if isinstance(height_value, bool):
        return (
            jsonify(
                {
                    "error": "height_inches must be numeric",
                }
            ),
            400,
        )

    try:
        height_inches = float(height_value)
    except (TypeError, ValueError):
        return (
            jsonify(
                {
                    "error": "height_inches must be numeric",
                }
            ),
            400,
        )

    if not math.isfinite(height_inches):
        return (
            jsonify(
                {
                    "error": "height_inches must be finite",
                }
            ),
            400,
        )

    if not 40 <= height_inches <= 100:
        return (
            jsonify(
                {
                    "error": "height_inches must be between 40 and 100",
                }
            ),
            400,
        )

    feature_frame = pd.DataFrame(
        {
            "height_inches": [height_inches],
        }
    )

    prediction = float(model_artifact["model"].predict(feature_frame)[0])

    return (
        jsonify(
            {
                "input": {
                    "height_inches": height_inches,
                },
                "prediction": {
                    "weight_pounds": round(prediction, 2),
                },
                "model": {
                    "name": model_artifact["metadata"]["model_name"],
                    "version": model_artifact["metadata"]["model_version"],
                },
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
