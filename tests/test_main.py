from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app 

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", params={"name": "Test User", "email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"
    assert response.json()["email"] == "test@example.com"

def test_read_user_not_found():
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
