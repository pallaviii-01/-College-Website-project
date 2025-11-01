import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.auth import create_access_token, verify_password, get_password_hash

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "SkillPath Navigator" in response.json()["message"]


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token():
    """Test JWT token creation."""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_register_user():
    """Test user registration endpoint."""
    user_data = {
        "email": f"test{pytest.timestamp}@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "preferred_language": "en"
    }
    
    response = client.post("/api/users/register", json=user_data)
    
    if response.status_code == 400:
        assert "already registered" in response.json()["detail"]
    else:
        assert response.status_code == 201
        assert response.json()["email"] == user_data["email"]


def test_register_duplicate_user():
    """Test registration with duplicate email."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "testpass123",
        "full_name": "Duplicate User",
        "preferred_language": "en"
    }
    
    client.post("/api/users/register", json=user_data)
    response = client.post("/api/users/register", json=user_data)
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/users/login", json=login_data)
    assert response.status_code == 401


def test_get_courses():
    """Test courses listing endpoint."""
    response = client.get("/api/courses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_courses_with_filters():
    """Test courses listing with filters."""
    response = client.get("/api/courses/?nsqf_level=5&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_nonexistent_course():
    """Test getting a course that doesn't exist."""
    response = client.get("/api/courses/99999")
    assert response.status_code == 404


def test_unauthorized_access():
    """Test accessing protected endpoint without authentication."""
    response = client.get("/api/users/me")
    assert response.status_code == 401


def test_get_sectors():
    """Test getting list of sectors."""
    response = client.get("/api/courses/sectors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Add timestamp for unique test data
pytest.timestamp = str(int(__import__('time').time()))
