# tests/test_users.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.user import UserCreate, UserUpdate

client = TestClient(app)

@pytest.fixture
def create_user():
    user_data = UserCreate(full_name="Test User", email="test@example.com", password="password")
    response = client.post("/users/", json=user_data.dict())
    return response.json()

def test_create_user(create_user):
    assert create_user["full_name"] == "Test User"
    assert create_user["email"] == "test@example.com"

def test_get_user(create_user):
    user_id = create_user["user_id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "Test User"

def test_update_user(create_user):
    user_id = create_user["user_id"]
    update_data = UserUpdate(full_name="Updated User")
    response = client.put(f"/users/{user_id}", json=update_data.dict(exclude_unset=True))
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated User"

def test_delete_user(create_user):
    user_id = create_user["user_id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404