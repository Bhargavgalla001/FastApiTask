"""
Test cases for user management endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestUsers:
    """User management endpoint tests"""
    
    def test_get_current_user_authenticated(self, client: TestClient, user_token):
        """Test getting current user profile"""
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["email"] == "testuser@example.com"
        assert response.json()["role"] == "user"
    
    def test_get_current_user_unauthenticated(self, client: TestClient):
        """Test getting current user without authentication"""
        response = client.get("/users/me")
        assert response.status_code == 401
    
    def test_list_users_admin(self, client: TestClient, admin_token, test_user):
        """Test listing all users as admin"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/users/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 2  # Admin and test user
    
    def test_list_users_non_admin(self, client: TestClient, user_token):
        """Test that non-admins cannot list all users"""
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/users/", headers=headers)
        assert response.status_code == 403
    
    def test_get_user_by_id_admin(self, client: TestClient, admin_token, test_user):
        """Test getting specific user as admin"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get(f"/users/{test_user.id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["email"] == "testuser@example.com"
    
    def test_get_nonexistent_user(self, client: TestClient, admin_token):
        """Test getting nonexistent user"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/users/9999", headers=headers)
        assert response.status_code == 404
    
    def test_update_user_role_admin(self, client: TestClient, admin_token, test_user):
        """Test updating user role as admin"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.patch(
            f"/users/{test_user.id}",
            json={"role": "admin"},
            headers=headers
        )
        assert response.status_code == 200
        assert response.json()["role"] == "admin"
    
    def test_delete_user_admin(self, client: TestClient, admin_token, test_user):
        """Test deleting user as admin"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.delete(f"/users/{test_user.id}", headers=headers)
        assert response.status_code == 204
    
    def test_user_cannot_delete_another_user(self, client: TestClient, user_token, test_admin):
        """Test that users cannot delete other users"""
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.delete(f"/users/{test_admin.id}", headers=headers)
        assert response.status_code == 403
    
    def test_update_own_password(self, client: TestClient, user_token, test_user):
        """Test updating own password"""
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.put(
            f"/users/{test_user.id}/password",
            json={"password": "newpassword123"},
            headers=headers
        )
        assert response.status_code == 200
        assert "Password updated successfully" in response.json()["message"]
    
    def test_update_other_user_password_non_admin(self, client: TestClient, user_token, test_admin):
        """Test that users cannot update other users' passwords"""
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.put(
            f"/users/{test_admin.id}/password",
            json={"password": "newpassword123"},
            headers=headers
        )
        assert response.status_code == 403
