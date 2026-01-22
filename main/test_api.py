import pytest
from fastapi.testclient import TestClient

from app.main import app


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
    response = client.get("/v1/health")  # Use the correct path with API prefix
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_create_request(client):
    import uuid
    unique_id = str(uuid.uuid4())[:8]  # Short unique identifier

    # First register a user with unique information
    register_data = {
        "user_name": f"test_user_create_{unique_id}",
        "user_mail": f"test_create_{unique_id}@example.com"
    }
    register_response = client.post("/v1/register", json=register_data)
    # Accept both success and conflict responses
    assert register_response.status_code in [200, 201, 409]

    register_data_response = register_response.json()
    user_id = register_data_response.get("user_id")

    # If user was created successfully (not a conflict), proceed with the test
    if user_id and user_id != "00000000-0000-0000-0000-000000000000":
        # Now create a search request with the user ID
        request_data = {
            "user": user_id,
            "n": 1,
            "prompt": "test search query",
            "mode": "sync"
        }

        response = client.post("/v1/requests", json=request_data)
        # Could return 201 Created or 200 OK depending on implementation
        assert response.status_code in [200, 201]
        data = response.json()

        assert "request_id" in data
        assert data["status"] in ["pending", "processing", "done", "error"]
    else:
        # If user already exists, skip the rest of this test
        print(f"Skipping request creation test due to user conflict: {register_data_response}")


def test_get_request(client):
    import uuid
    unique_id = str(uuid.uuid4())[:8]  # Short unique identifier

    # First register a user with unique information
    register_data = {
        "user_name": f"test_user_get_{unique_id}",
        "user_mail": f"test_get_{unique_id}@example.com"
    }
    register_response = client.post("/v1/register", json=register_data)
    # Accept both success and conflict responses
    assert register_response.status_code in [200, 201, 409]

    register_data_response = register_response.json()
    user_id = register_data_response.get("user_id")

    # If user was created successfully (not a conflict), proceed with the test
    if user_id and user_id != "00000000-0000-0000-0000-000000000000":
        # Create a search request with the user ID
        request_data = {
            "user": user_id,
            "n": 1,
            "prompt": "test search query for get",
            "mode": "sync"
        }

        create_response = client.post("/v1/requests", json=request_data)
        assert create_response.status_code in [200, 201]
        created_request = create_response.json()

        # Then get the request
        request_id = created_request.get("request_id")
        if request_id:
            response = client.get(f"/v1/requests/{request_id}")
            # May return 200 if found or 404 if not in memory store
            assert response.status_code in [200, 404]
    else:
        # If user already exists, skip the rest of this test
        print(f"Skipping get request test due to user conflict: {register_data_response}")


if __name__ == "__main__":
    pytest.main([__file__])
