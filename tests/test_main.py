import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure the db module is correctly recognized
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.database import Base, engine, SessionLocal
from main import app, get_db, users_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}

def test_create_user():
    response = client.post("/users/", json={"id": 1, "name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "John Doe", "email": "john@example.com"}

def test_read_user():
    users_db[1] = {"id": 1, "name": "John Doe", "email": "john@example.com"}
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "email": "john@example.com"}

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_user():
    users_db[1] = {"id": 1, "name": "John Doe", "email": "john@example.com"}
    response = client.put("/users/1", json={"id": 1, "name": "Jane Doe", "email": "jane@example.com"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Jane Doe", "email": "jane@example.com"}

def test_delete_user():
    users_db[1] = {"id": 1, "name": "John Doe", "email": "john@example.com"}
    response = client.delete("/users/1")
    assert response.status_code == 204
    response = client.get("/users/1")
    assert response.status_code == 404