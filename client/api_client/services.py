import requests

BASE_URL = "http://127.0.0.1:8000"

def register_user_api(username, email, password):
    payload = {"username": username, "email": email, "password": password}
    return requests.post(f"{BASE_URL}/users", json=payload)

def login_user_api(email, password):
    form_data = {'username': email, 'password': password}
    return requests.post(f"{BASE_URL}/users/login", data=form_data)

def save_note_api(token, title, content):
    payload = {"title": title, "content": content}
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(f"{BASE_URL}/notes/", json=payload, headers=headers)

def get_notes_api(token):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE_URL}/notes/", headers=headers)

def delete_note_api(token, title):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.delete(f"{BASE_URL}/notes/{title}", headers=headers)
