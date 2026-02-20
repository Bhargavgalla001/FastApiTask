"""
Test cases for authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestAuthentication:
    """Authentication tests"""
    
    def test_register_user(self, client: TestClient):
        """Test user registration"""
        response = client.post(
            "/auth/register",
            json={"email": "newuser@example.com", "password": "password123"}
        )
        assert response.status_code == 201
        assert response.json()["message"] == "User registered successfully"
        assert response.json()["user"]["email"] == "newuser@example.com"
        assert response.json()["user"]["role"] == "user"
    
    def test_register_duplicate_email(self, client: TestClient, test_user):
        """Test duplicate email registration"""
        response = client.post(
            "/auth/register",
            json={"email": "testuser@example.com", "password": "password123"}
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_login_success(self, client: TestClient, test_user):
        """Test successful login"""
        response = client.post(
            "/auth/login",
            json={"email": "testuser@example.com", "password": "password123"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
    
    def test_login_wrong_password(self, client: TestClient, test_user):
        """Test login with wrong password"""
        response = client.post(
            "/auth/login",
            json={"email": "testuser@example.com", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "Invalid" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with nonexistent user"""
        response = client.post(
            "/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"}
        )
        assert response.status_code == 401
    
    def test_refresh_token(self, client: TestClient, test_user):
        """Test token refresh"""
        # First login
        login_response = client.post(
            "/auth/login",
            json={"email": "testuser@example.com", "password": "password123"}
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh token
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
    
    def test_invalid_refresh_token(self, client: TestClient):
        """Test refresh with invalid token"""
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": "invalid_token"}
        )
        assert response.status_code == 401
