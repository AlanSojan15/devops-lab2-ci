import pytest

from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Calculator" in response.data


def test_api_info(client):
    response = client.get("/api")
    assert response.status_code == 200
    assert "message" in response.get_json()


def test_health(client):
    response = client.get("/health")
    assert response.get_json() == {"status": "ok"}


def test_add_endpoint(client):
    response = client.get("/add?a=2&b=3")
    assert response.status_code == 200
    assert response.get_json()["result"] == 5


def test_divide_by_zero_endpoint(client):
    response = client.get("/divide?a=1&b=0")
    assert response.status_code == 400


def test_bad_input(client):
    response = client.get("/add?a=x&b=3")
    assert response.status_code == 400


def test_unknown_operation(client):
    response = client.get("/power?a=2&b=3")
    assert response.status_code == 404
