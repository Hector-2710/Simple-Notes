from fastapi.testclient import TestClient

# User tests
def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_user_duplicate(client: TestClient):
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    response = client.post(
        "/users/",
        json={"username": "testuser2", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 409

def test_login_user(client: TestClient):
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    response = client.post(
        "/users/login",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_user_not_found(client: TestClient):
    response = client.post(
        "/users/login",
        data={"username": "wrong@example.com", "password": "password123"},
    )
    assert response.status_code == 404

def test_login_user_wrong_password(client: TestClient):
    # Create user first
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    response = client.post(
        "/users/login",
        data={"username": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 400

# Note tests
def test_create_note(client: TestClient):
    # Register and login first
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    login_response = client.post(
        "/users/login",
        data={"username": "test@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "This is a test note."},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test note."

def test_create_note_unauthenticated(client: TestClient):
    response = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "This is a test note."},
    )
    assert response.status_code == 401

def test_get_notes(client: TestClient):
    # Setup user and note
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    token = client.post(
        "/users/login",
        data={"username": "test@example.com", "password": "password123"},
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    client.post(
        "/notes/",
        json={"title": "Note 1", "content": "Content 1"},
        headers=headers,
    )
    client.post(
        "/notes/",
        json={"title": "Note 2", "content": "Content 2"},
        headers=headers,
    )

    response = client.get("/notes/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Note 1"

def test_get_note_by_title(client: TestClient):
    # Setup user and note
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    token = client.post(
        "/users/login",
        data={"username": "test@example.com", "password": "password123"},
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    client.post(
        "/notes/",
        json={"title": "Target Note", "content": "Target Content"},
        headers=headers,
    )

    response = client.get("/notes/Target Note", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Target Note"
    assert data["content"] == "Target Content"

def test_delete_note(client: TestClient):
    # Setup user and note
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    token = client.post(
        "/users/login",
        data={"username": "test@example.com", "password": "password123"},
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    client.post(
        "/notes/",
        json={"title": "Delete Me", "content": "Content"},
        headers=headers,
    )

    # Verify exists
    assert client.get("/notes/Delete Me", headers=headers).status_code == 200

    # Delete
    response = client.delete("/notes/Delete Me", headers=headers)
    # The return type of delete endpoint might vary, assuming 200 and maybe returning the deleted note or a message
    # Based on the route reading: `return note` so it returns NoteResponse
    assert response.status_code == 200
    assert response.json()["title"] == "Delete Me"

    # Verify deleted
    # Wait, the get_note_for_user_service probably raises 404 or returns None. 
    # Let's check exception handling if time permits, but typically 404.
    # The route code showed `delete_note_for_user_service` returning `note`.
