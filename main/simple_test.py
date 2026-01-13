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
    
    # Test creating an order
    order_data = {
        "customer_id": "customer_123",
        "items": [{"product_id": "prod_1", "quantity": 2, "price": 10.99}],
        "total_amount": 21.98
    }
    
    response = client.post("/v1/orders", json=order_data)
    print(f"Create order: {response.status_code} - {response.json()}")
    assert response.status_code == 201
    
    # Store the created order ID for later use
    created_order = response.json()
    order_id = created_order["id"]
    
    # Test getting the order
    response = client.get(f"/v1/orders/{order_id}")
    print(f"Get order: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    
    # Test listing orders
    response = client.get("/v1/orders")
    print(f"List orders: {response.status_code} - {len(response.json())} orders")
    assert response.status_code == 200
    
    print("All tests passed!")

if __name__ == "__main__":
    test_endpoints()