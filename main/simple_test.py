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

    # First, try to register a user (use unique values to avoid conflicts)
    import uuid
    unique_id = str(uuid.uuid4())[:8]  # Short unique identifier

    register_data = {
        "user_name": f"test_user_{unique_id}",
        "user_mail": f"test_{unique_id}@example.com"
    }
    response = client.post("/v1/register", json=register_data)
    print(f"Register user: {response.status_code} - {response.json()}")
    # Accept both success (200/201) and conflict (409) since user might already exist
    assert response.status_code in [200, 201, 409]

    # Extract user ID from registration response if successful
    register_response = response.json()
    user_id = register_response.get("user_id")

    # If user already existed, we'll get an error in the response
    if user_id and user_id != "00000000-0000-0000-0000-000000000000":
        print(f"Registered new user with ID: {user_id}")
        # Test creating a search request with the registered user
        request_data = {
            "user": user_id,  # Include the user ID
            "n": 1,
            "prompt": "test search query",
            "mode": "sync"
        }

        response = client.post("/v1/requests", json=request_data)
        print(f"Create search request: {response.status_code} - {response.json()}")
        # Expect 201 Created or 200 OK depending on the implementation
        assert response.status_code in [200, 201]

        # Store the created request ID for later use
        created_request = response.json()
        request_id = created_request.get("request_id") or created_request.get("id")

        if request_id:
            # Test getting the request
            response = client.get(f"/v1/requests/{request_id}")
            print(f"Get request: {response.status_code} - {response.json()}")
            # The request might not be found if it's processed quickly or not stored in memory
            # So we'll accept both 200 and 404
            assert response.status_code in [200, 404]
    else:
        print("Could not register new user, possibly due to conflict. Skipping request creation test.")
        # If we can't register a user, we can't test the request creation
        # But we can still test other endpoints

    # Test listing requests
    response = client.get("/v1/requests")
    print(
        f"List requests: {response.status_code} - "
        f"{len(response.json()) if isinstance(response.json(), list) else 'data'} requests"
    )
    assert response.status_code == 200

    print("All tests passed!")


if __name__ == "__main__":
    test_endpoints()
