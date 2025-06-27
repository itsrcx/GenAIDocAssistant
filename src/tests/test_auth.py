import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from src.main import app

client = TestClient(app)

@pytest.fixture
def mock_signup_user():
    with patch("src.services.cognito.signup_user") as mock:
        yield mock

@pytest.fixture
def mock_confirm_signup():
    with patch("src.services.cognito.confirm_signup") as mock:
        yield mock

@pytest.fixture
def mock_login_user():
    with patch("src.services.cognito.login_user") as mock:
        yield mock

@pytest.fixture
def mock_forgot_password():
    with patch("src.services.cognito.forgot_password") as mock:
        yield mock

@pytest.fixture
def mock_confirm_forgot_password():
    with patch("src.services.cognito.confirm_forgot_password") as mock:
        yield mock

@pytest.fixture
def mock_change_password():
    with patch("src.services.cognito.change_password") as mock:
        yield mock

@pytest.fixture
def mock_logout():
    with patch("src.services.cognito.logout") as mock:
        yield mock

def test_signup_success(mock_signup_user):
    mock_signup_user.return_value = None
    response = client.post("/api/auth/signup", json={"email": "test@example.com", "password": "Password123!"})
    assert response.status_code == 201
    assert response.json()["status"] == "success"

def test_confirm_signup_success(mock_confirm_signup):
    mock_confirm_signup.return_value = None
    response = client.post("/api/auth/confirm-signup", json={"email": "test@example.com", "code": "123456"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_login_success(mock_login_user):
    mock_login_user.return_value = {"access_token": "token", "refresh_token": "refresh"}
    response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "Password123!"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "access_token" in response.json()["data"]

def test_forgot_password_success(mock_forgot_password):
    mock_forgot_password.return_value = None
    response = client.post("/api/auth/forgot-password", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_reset_password_success(mock_confirm_forgot_password):
    mock_confirm_forgot_password.return_value = None
    response = client.post("/api/auth/reset-password", json={
        "email": "test@example.com",
        "code": "123456",
        "new_password": "NewPassword123!"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_change_password_success(mock_change_password):
    mock_change_password.return_value = None
    headers = {"Authorization": "Bearer testtoken"}
    response = client.post("/api/auth/change-password", json={
        "old_password": "OldPassword123!",
        "new_password": "NewPassword123!"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_logout_success(mock_logout):
    mock_logout.return_value = None
    headers = {"Authorization": "Bearer testtoken"}
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
