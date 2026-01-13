import pytest
import asyncio
from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app
from app.schemas import RequestCreate


@pytest.fixture
def client():
    return TestClient(app)


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_create_request(client):
    request_data = {
        "customer_id": "customer_123",
        "items": [{"product_id": "prod_1", "quantity": 2, "price": 10.99}],
        "total_amount": 21.98
    }

    response = client.post("/v1/requests", json=request_data)
    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["customer_id"] == request_data["customer_id"]
    assert data["total_amount"] == request_data["total_amount"]
    assert data["status"] == "pending"


def test_get_request(client):
    # First create a request
    request_data = {
        "customer_id": "customer_456",
        "items": [{"product_id": "prod_2", "quantity": 1, "price": 15.50}],
        "total_amount": 15.50
    }

    create_response = client.post("/v1/requests", json=request_data)
    assert create_response.status_code == 201
    created_request = create_response.json()

    # Then get the request
    request_id = created_request["id"]
    response = client.get(f"/v1/requests/{request_id}")
    assert response.status_code == 200
    retrieved_request = response.json()

    assert retrieved_request["id"] == request_id
    assert retrieved_request["customer_id"] == request_data["customer_id"]


if __name__ == "__main__":
    pytest.main([__file__])