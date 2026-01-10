from fastapi.testclient import TestClient
from api.main import app


client = TestClient(app)

def test_register():
    response = client.post("/users/", json={
        "username": "testusedr",
        "email": "testuserdlk@example.com",    
        "password": "testpy"
    })
    assert response.status_code == 201

def test_register_duplicate():
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "testuserdlk@example.com",    
        "password": "testpy"
    })
    assert response.status_code == 409

def test_login():
    response = client.post("/users/login", data={
        "username": "testuserd@example.com", "password": "testpy"
    })
    assert response.status_code == 200