import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from botocore.exceptions import ClientError

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

# --- Input Validation ---

def test_signup_invalid_email(mock_signup_user):
    response = client.post("/api/auth/signup", json={"email": "not-an-email", "password": "Password123!"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"].startswith("value is not a valid email address")

def test_signup_short_password(mock_signup_user):
    response = client.post("/api/auth/signup", json={"email": "test@example.com", "password": "abc"})
    assert response.status_code == 422   

def test_confirm_signup_missing_code(mock_confirm_signup):
    response = client.post("/api/auth/confirm-signup", json={"email": "test@example.com"})
    assert response.status_code == 422

def test_login_missing_password(mock_login_user):
    response = client.post("/api/auth/login", json={"email": "test@example.com"})
    assert response.status_code == 422

# --- Authentication & Authorization ---

def test_change_password_no_token(mock_change_password):
    response = client.post("/api/auth/change-password", json={
        "old_password": "OldPassword123!",
        "new_password": "NewPassword123!"
    })
    assert response.status_code == 403 or response.status_code == 401

def test_logout_no_token(mock_logout):
    response = client.post("/api/auth/logout")
    assert response.status_code == 403 or response.status_code == 401

# --- Error Handling ---

def test_login_not_authorized(mock_login_user):
    mock_login_user.side_effect = ClientError(
        {"Error": {"Code": "NotAuthorizedException", "Message": "Incorrect username or password"}}, "login_user"
    )
    response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "Wrong@1234#"})
    assert response.status_code == 401
    assert response.json()["error"] == "NotAuthorizedException"

def test_signup_username_exists(mock_signup_user):
    mock_signup_user.side_effect = ClientError(
        {"Error": {"Code": "UsernameExistsException", "Message": "User already exists"}}, "signup_user"
    )
    response = client.post("/api/auth/signup", json={"email": "test@example.com", "password": "Password123!"})
    assert response.status_code == 400 or response.status_code == 409
    assert response.json()["error"] == "UsernameExistsException"

# --- Edge Cases ---

def test_signup_empty_payload(mock_signup_user):
    response = client.post("/api/auth/signup", json={})
    assert response.status_code == 422

def test_reset_password_invalid_code(mock_confirm_forgot_password):
    mock_confirm_forgot_password.side_effect = ClientError(
        {"Error": {"Code": "ExpiredCodeException", "Message": "Code expired"}}, "confirm_forgot_password"
    )
    response = client.post("/api/auth/reset-password", json={
        "email": "test@example.com",
        "code": "123456",
        "new_password": "NewPassword123!"
    })
    assert response.status_code == 400
    assert response.json()["error"] == "ExpiredCodeException"

# --- Rate Limiting (simulate TooManyRequestsException) ---

def test_signup_rate_limited(mock_signup_user):
    mock_signup_user.side_effect = ClientError(
        {"Error": {"Code": "TooManyRequestsException", "Message": "Rate limit exceeded"}}, "signup_user"
    )
    response = client.post("/api/auth/signup", json={"email": "test@example.com", "password": "Password123!"})
    assert response.status_code == 429
    assert response.json()["error"] == "TooManyRequestsException"

# --- Concurrency/State Tests (simulate multiple logins) ---

def test_multiple_logins(mock_login_user):
    mock_login_user.return_value = {"access_token": "token", "refresh_token": "refresh"}
    for _ in range(5):
        response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "Password123!"})
        assert response.status_code == 200
        assert response.json()["status"] == "success"

# --- Schema & Response Format ---

def test_signup_response_schema(mock_signup_user):
    mock_signup_user.return_value = None
    response = client.post("/api/auth/signup", json={"email": "test@example.com", "password": "Password123!"})
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "data" in data

def test_error_response_schema(mock_signup_user):
    mock_signup_user.side_effect = ClientError(
        {"Error": {"Code": "UsernameExistsException", "Message": "User already exists"}}, "signup_user"
    )
    response = client.post("/api/auth/signup", json={"email": "test@example.com", "password": "Password123!"})
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "error" in data

# --- Successful Operations ---
def test_signup_success(mock_signup_user):
    mock_signup_user.return_value = None
    response = client.post("/api/auth/signup", json={"email": "test@example.com", "password": "Password123!"})
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["message"].startswith("Signup successful")

def test_confirm_signup_success(mock_confirm_signup):
    mock_confirm_signup.return_value = None
    response = client.post("/api/auth/confirm-signup", json={"email": "test@example.com", "code": "123456"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"].startswith("Signup confirmed")

def test_login_success(mock_login_user):
    mock_login_user.return_value = {"access_token": "token", "refresh_token": "refresh"}
    response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "Password123!"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "access_token" in data["data"]

def test_forgot_password_success(mock_forgot_password):
    mock_forgot_password.return_value = None
    response = client.post("/api/auth/forgot-password", json={"email": "test@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Confirmation code sent" in data["message"]

def test_reset_password_success(mock_confirm_forgot_password):
    mock_confirm_forgot_password.return_value = None
    response = client.post("/api/auth/reset-password", json={
        "email": "test@example.com",
        "code": "123456",
        "new_password": "NewPassword123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Password reset" in data["message"]

def test_change_password_success(mock_change_password):
    mock_change_password.return_value = None
    headers = {"Authorization": "Bearer testtoken"}
    response = client.post("/api/auth/change-password", json={
        "old_password": "OldPassword123!",
        "new_password": "NewPassword123!"
    }, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Password changed" in data["message"]

def test_logout_success(mock_logout):
    mock_logout.return_value = None
    headers = {"Authorization": "Bearer testtoken"}
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Logged out" in data["message"]
