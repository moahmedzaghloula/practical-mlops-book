"""Tests for the model training module."""

import json

import joblib

from train import fingerprint_dataset, make_dataset, train_model


def test_dataset_is_deterministic():
    first_features, first_targets = make_dataset()
    second_features, second_targets = make_dataset()

    assert fingerprint_dataset(
        first_features,
        first_targets,
    ) == fingerprint_dataset(
        second_features,
        second_targets,
    )


def test_train_model_writes_artifacts(tmp_path):
    model_path, metadata_path = train_model(tmp_path)

    assert model_path.is_file()
    assert metadata_path.is_file()

    bundle = joblib.load(model_path)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    assert "model" in bundle
    assert metadata["model_name"] == "height-to-weight-regressor"
    assert metadata["training_rows"] == 500
