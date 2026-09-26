import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"


def test_search_requires_query(client):
    response = client.get(
        "/api/products/search"
    )

    assert response.status_code == 400


def test_invalid_scrape_limit(client):
    response = client.post(
        "/api/scrape?limit=0"
    )

    assert response.status_code == 400
