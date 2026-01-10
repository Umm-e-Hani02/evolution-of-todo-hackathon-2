"""Authentication endpoint tests."""
import pytest
from fastapi import status


class TestAuthRegistration:
    """Tests for user registration endpoint."""

    def test_register_new_user(self, client):
        """Test registering a new user returns 201 and token."""
        response = client.post(
            "/auth/register",
            json={"email": "newuser@example.com", "password": "password123"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["email"] == "newuser@example.com"

    def test_register_duplicate_email(self, client, test_user):
        """Test registering with existing email returns 409."""
        response = client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "password123"},
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already registered" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        """Test registering with invalid email returns 422."""
        response = client.post(
            "/auth/register",
            json={"email": "not-an-email", "password": "password123"},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_short_password(self, client):
        """Test registering with short password returns 422."""
        response = client.post(
            "/auth/register",
            json={"email": "user@example.com", "password": "short"},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestAuthLogin:
    """Tests for user login endpoint."""

    def test_login_valid_credentials(self, client, test_user):
        """Test login with valid credentials returns 200 and token."""
        response = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["email"] == "test@example.com"

    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password returns 401."""
        response = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid email or password" in response.json()["detail"]

    def test_login_nonexistent_email(self, client):
        """Test login with non-existent email returns generic 401."""
        response = client.post(
            "/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        # Should not reveal whether email exists
        assert "Invalid email or password" in response.json()["detail"]


class TestAuthMe:
    """Tests for get current user endpoint."""

    def test_get_me_authenticated(self, client, auth_headers, test_user):
        """Test getting current user with valid token."""
        response = client.get("/auth/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["id"] == test_user.id

    def test_get_me_unauthenticated(self, client):
        """Test getting current user without token returns 401."""
        response = client.get("/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_me_invalid_token(self, client):
        """Test getting current user with invalid token returns 401."""
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalidtoken"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
