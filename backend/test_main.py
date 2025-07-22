from fastapi.testclient import TestClient
from backend.main import app
from backend.dependencies import get_db
import pytest
import mysql.connector
from backend.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

client = TestClient(app)

@pytest.fixture(scope="module")
def db_connection():
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=f"{DB_NAME}_test"
    )
    yield connection
    connection.close()

@pytest.fixture(scope="module", autouse=True)
def setup_teardown_database(db_connection):
    cursor = db_connection.cursor()
    # Create tables
    with open('../database/schema.sql', 'r') as f:
        cursor.execute(f.read(), multi=True)
    db_connection.commit()
    yield
    # Teardown
    cursor.execute("DROP TABLE borrowed_books, books, users;")
    db_connection.commit()
    cursor.close()

def override_get_db(db_connection):
    def _override_get_db():
        try:
            yield db_connection
        finally:
            pass
    return _override_get_db

def test_create_user(db_connection):
    app.dependency_overrides[get_db] = override_get_db(db_connection)
    response = client.post(
        "/users/",
        json={"name": "Test User", "email": "test@example.com", "password": "testpassword", "role": "user"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "id" in response.json()


def test_create_existing_user(db_connection):
    app.dependency_overrides[get_db] = override_get_db(db_connection)
    response = client.post(
        "/users/",
        json={"name": "Test User", "email": "test@example.com", "password": "testpassword", "role": "user"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login(db_connection):
    app.dependency_overrides[get_db] = override_get_db(db_connection)
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_read_users_me(db_connection):
    app.dependency_overrides[get_db] = override_get_db(db_connection)
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "testpassword"},
    )
    token = response.json()["access_token"]
    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
