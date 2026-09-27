"""Serve the trained regression model through a Flask API."""

from __future__ import annotations

import os
from pathlib import Path

import joblib
import numpy as np
from flask import Flask, jsonify, request

DEFAULT_MODEL_PATH = Path(os.getenv("MODEL_PATH", "model/model.joblib"))


def create_app(
    model_path: Path = DEFAULT_MODEL_PATH,
) -> Flask:
    """Create and configure the Flask application."""
    application = Flask(__name__)

    model_bundle = joblib.load(model_path)
    model = model_bundle["model"]
    metadata = model_bundle["metadata"]

    @application.get("/")
    def home():
        return jsonify(
            {
                "service": "Chapter 3 model API",
                "documentation": {
                    "prediction_endpoint": "POST /predict",
                    "example_body": {"height_cm": 175.0},
                    "metadata_endpoint": "GET /metadata",
                    "health_endpoint": "GET /health",
                    "readiness_endpoint": "GET /ready",
                },
            }
        )

    @application.get("/health")
    def health():
        return jsonify({"status": "alive"}), 200

    @application.get("/ready")
    def ready():
        return (
            jsonify(
                {
                    "status": "ready",
                    "model_loaded": True,
                    "model_version": metadata["model_version"],
                }
            ),
            200,
        )

    @application.get("/metadata")
    def model_metadata():
        return jsonify(metadata), 200

    @application.post("/predict")
    def predict():
        if not request.is_json:
            return jsonify({"error": ("Content-Type must be application/json")}), 415

        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400

        if "height_cm" not in payload:
            return jsonify({"error": "Missing required field: height_cm"}), 400

        height_cm = payload["height_cm"]

        if isinstance(height_cm, bool) or not isinstance(
            height_cm,
            (int, float),
        ):
            return jsonify({"error": "height_cm must be a number"}), 400

        if not 100.0 <= float(height_cm) <= 250.0:
            return jsonify({"error": ("height_cm must be between 100 and 250")}), 400

        inference_features = np.array(
            [[float(height_cm)]],
            dtype=np.float64,
        )

        predicted_weight = float(model.predict(inference_features)[0])

        return (
            jsonify(
                {
                    "input": {
                        "height_cm": float(height_cm),
                    },
                    "prediction": {
                        "weight_kg": round(predicted_weight, 2),
                    },
                    "model_version": metadata["model_version"],
                }
            ),
            200,
        )

    return application


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
    )
