"""Tests for the Flask inference API."""

import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_home_documents_the_api(client):
    response = client.get("/")

    assert response.status_code == 200
    assert (
        response.get_json()["documentation"]["prediction_endpoint"] == "POST /predict"
    )


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "alive"}


def test_readiness_endpoint(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.get_json()["model_loaded"] is True


def test_metadata_endpoint(client):
    response = client.get("/metadata")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["feature_names"] == ["height_cm"]


def test_valid_prediction(client):
    response = client.post(
        "/predict",
        json={"height_cm": 175.0},
    )
    payload = response.get_json()

    assert response.status_code == 200
    assert isinstance(
        payload["prediction"]["weight_kg"],
        float,
    )


def test_missing_height_fails(client):
    response = client.post(
        "/predict",
        json={},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == ("Missing required field: height_cm")


def test_invalid_height_type_fails(client):
    response = client.post(
        "/predict",
        json={"height_cm": "tall"},
    )

    assert response.status_code == 400


def test_boolean_height_fails(client):
    response = client.post(
        "/predict",
        json={"height_cm": True},
    )

    assert response.status_code == 400


def test_out_of_range_height_fails(client):
    response = client.post(
        "/predict",
        json={"height_cm": 500},
    )

    assert response.status_code == 400


def test_non_json_request_fails(client):
    response = client.post(
        "/predict",
        data="height_cm=175",
        content_type="text/plain",
    )

    assert response.status_code == 415
