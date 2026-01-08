import requests

BASE_URL = "http://127.0.0.1:8000"

def register_user_api(username, email, password):
    payload = {"username": username, "email": email, "password": password}
    return requests.post(f"{BASE_URL}/users", json=payload)

def login_user_api(email, password):
    # Usamos data= porque FastAPI OAuth2 espera formulario, no JSON
    form_data = {'username': email, 'password': password}
    return requests.post(f"{BASE_URL}/users/login", data=form_data)

def save_note_api(user_id, title, content):
    payload = {"title": title, "content": content}
    return requests.post(f"{BASE_URL}/notes/{user_id}", json=payload)