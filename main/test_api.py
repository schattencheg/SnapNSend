import pytest
import asyncio
from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app
from app.schemas import OrderCreate


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


def test_create_order(client):
    order_data = {
        "customer_id": "customer_123",
        "items": [{"product_id": "prod_1", "quantity": 2, "price": 10.99}],
        "total_amount": 21.98
    }
    
    response = client.post("/v1/orders", json=order_data)
    assert response.status_code == 201
    data = response.json()
    
    assert "id" in data
    assert data["customer_id"] == order_data["customer_id"]
    assert data["total_amount"] == order_data["total_amount"]
    assert data["status"] == "pending"


def test_get_order(client):
    # First create an order
    order_data = {
        "customer_id": "customer_456",
        "items": [{"product_id": "prod_2", "quantity": 1, "price": 15.50}],
        "total_amount": 15.50
    }
    
    create_response = client.post("/v1/orders", json=order_data)
    assert create_response.status_code == 201
    created_order = create_response.json()
    
    # Then get the order
    order_id = created_order["id"]
    response = client.get(f"/v1/orders/{order_id}")
    assert response.status_code == 200
    retrieved_order = response.json()
    
    assert retrieved_order["id"] == order_id
    assert retrieved_order["customer_id"] == order_data["customer_id"]


if __name__ == "__main__":
    pytest.main([__file__])