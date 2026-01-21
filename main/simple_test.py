from app.main import app
from fastapi.testclient import TestClient

# Create a test client
client = TestClient(app)


def test_endpoints():
    print("Testing API endpoints...")

    # Test root endpoint
    response = client.get("/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")
    assert response.status_code == 200

    # Test health endpoint (it's mounted under the API prefix)
    response = client.get("/v1/health")
    print(f"Health endpoint: {response.status_code} - {response.json()}")
    assert response.status_code == 200

    # Test creating a request
    request_data = {
        "customer_id": "customer_123",
        "items": [{"product_id": "prod_1", "quantity": 2, "price": 10.99}],
        "total_amount": 21.98
    }

    response = client.post("/v1/requests", json=request_data)
    print(f"Create request: {response.status_code} - {response.json()}")
    assert response.status_code == 201

    # Store the created request ID for later use
    created_request = response.json()
    request_id = created_request["id"]

    # Test getting the request
    response = client.get(f"/v1/requests/{request_id}")
    print(f"Get request: {response.status_code} - {response.json()}")
    assert response.status_code == 200

    # Test listing requests
    response = client.get("/v1/requests")
    print(
        f"List requests: {response.status_code} - "
        f"{len(response.json())} requests"
    )
    assert response.status_code == 200

    print("All tests passed!")


if __name__ == "__main__":
    test_endpoints()
