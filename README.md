# Simple-Notes

Simple-Notes is a RESTful API built with **FastAPI** for managing users and notes. It uses **PostgreSQL** as the database and **SQLModel** for ORM. The project follows a Client-Server architecture where the backend serves a GUI client (e.g., Tkinter).

## 🏗️ Architecture

The application follows a standard Client-Server model:
1. The Client (e.g., Tkinter app) captures user input and sends JSON payloads.
2. **FastAPI** receives the requests and interacts with **PostgreSQL** using **SQLModel**.
3. The database returns the record, and the API sends a structured response back to the client.

## 🚀 Features

- **User Management**:
  - Registration (with email uniqueness check)
  - Login (JWT Authentication)
- **Note Management**:
  - Create notes
  - Retrieve all notes for the logged-in user
  - Retrieve specific notes by title
  - Delete notes

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLModel / SQLAlchemy
- **Authentication**: OAuth2 with Password (Bearer Token)
- **Testing**: Pytest

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Simple-Notes
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your database URL:
   ```env
   POSTGRES_URL=postgresql://user:password@localhost:5432/db_name
   SECRET_KEY=your_secret_key
   ```

## ▶️ Running the Application

Start the development server with Uvicorn:

```bash
uvicorn api.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.
Access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## 🧪 Running Tests

This project uses **Pytest** for testing. A `conftest.py` is configured to use an in-memory SQLite database for test isolation.

Run the tests using:

```bash
pytest
# or
venv/bin/pytest
```
