"""Tests for the Flask prediction API."""

from app import app


def test_health_endpoint() -> None:
    """The liveness endpoint should return HTTP 200."""

    with app.test_client() as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "alive",
    }


def test_readiness_endpoint() -> None:
    """The application should load the model artifact."""

    with app.test_client() as client:
        response = client.get("/ready")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ready"


def test_valid_prediction() -> None:
    """A valid input should produce a prediction."""

    with app.test_client() as client:
        response = client.post(
            "/predict",
            json={
                "height_inches": 70,
            },
        )

    body = response.get_json()

    assert response.status_code == 200
    assert body["input"]["height_inches"] == 70
    assert isinstance(
        body["prediction"]["weight_pounds"],
        float,
    )
    assert body["model"]["version"] == "1.0.0"


def test_missing_height_fails() -> None:
    """A missing feature should return HTTP 400."""

    with app.test_client() as client:
        response = client.post(
            "/predict",
            json={},
        )

    assert response.status_code == 400


def test_invalid_height_type_fails() -> None:
    """A nonnumeric feature should return HTTP 400."""

    with app.test_client() as client:
        response = client.post(
            "/predict",
            json={
                "height_inches": "unknown",
            },
        )

    assert response.status_code == 400


def test_out_of_range_height_fails() -> None:
    """An unrealistic value should return HTTP 400."""

    with app.test_client() as client:
        response = client.post(
            "/predict",
            json={
                "height_inches": 500,
            },
        )

    assert response.status_code == 400


def test_non_json_request_fails() -> None:
    """A non-JSON request should return HTTP 415."""

    with app.test_client() as client:
        response = client.post(
            "/predict",
            data="height_inches=70",
        )

    assert response.status_code == 415
