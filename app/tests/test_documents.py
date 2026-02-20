"""
Test cases for document endpoints
"""
import pytest
from io import BytesIO
from fastapi.testclient import TestClient


class TestDocuments:
    """Document endpoint tests"""
    
    def test_get_my_documents_authenticated(self, client: TestClient, user_token):
        """Test getting own documents as authenticated user"""
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/documents/my", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_my_documents_unauthenticated(self, client: TestClient):
        """Test getting own documents without authentication"""
        response = client.get("/documents/my")
        assert response.status_code == 401
    
    def test_get_all_documents_admin(self, client: TestClient, admin_token):
        """Test getting all documents as admin"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/documents/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_all_documents_user_forbidden(self, client: TestClient, user_token):
        """Test that regular users cannot get all documents"""
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/documents/", headers=headers)
        assert response.status_code == 403
        assert "Admin access required" in response.json()["detail"]
    
    def test_upload_document(self, client: TestClient, user_token):
        """Test document upload"""
        headers = {"Authorization": f"Bearer {user_token}"}
        
        # Create a test file
        file_content = b"Test document content"
        files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}
        
        response = client.post(
            "/documents/upload",
            headers=headers,
            files=files
        )
        assert response.status_code == 200
        assert "document_id" in response.json()
        assert response.json()["status"] == "pending"
    
    def test_upload_document_unauthenticated(self, client: TestClient):
        """Test document upload without authentication"""
        file_content = b"Test document content"
        files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}
        
        response = client.post(
            "/documents/upload",
            files=files
        )
        assert response.status_code == 401
    
    def test_get_approved_documents_public(self, client: TestClient):
        """Test getting approved documents without authentication"""
        response = client.get("/documents/public/approved")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert "documents" in response.json()
    
    def test_search_documents_with_filters(self, client: TestClient, admin_token):
        """Test advanced search with filters"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        response = client.get(
            "/documents/search/advanced?status=pending&limit=5",
            headers=headers
        )
        assert response.status_code == 200
        assert "total" in response.json()
        assert "documents" in response.json()
        assert "skip" in response.json()
        assert "limit" in response.json()
    
    def test_search_invalid_status(self, client: TestClient, admin_token):
        """Test search with invalid status filter"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        response = client.get(
            "/documents/search/advanced?status=invalid_status",
            headers=headers
        )
        assert response.status_code == 400
    
    def test_approve_document(self, client: TestClient, admin_token, db):
        """Test approving a document"""
        # Create a test document
        from app.models.document import Document
        
        doc = Document(
            filename="test.pdf",
            file_path="/uploads/test.pdf",
            uploaded_by=2,
            status="pending"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.put(
            f"/documents/{doc.id}/approve",
            json={"comment": "Approved"},
            headers=headers
        )
        assert response.status_code == 200
        assert response.json()["status"] == "approved"
    
    def test_approve_already_approved_document(self, client: TestClient, admin_token, db):
        """Test approving an already approved document"""
        from app.models.document import Document
        
        doc = Document(
            filename="test.pdf",
            file_path="/uploads/test.pdf",
            uploaded_by=2,
            status="approved"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.put(
            f"/documents/{doc.id}/approve",
            json={"comment": "Approved"},
            headers=headers
        )
        assert response.status_code == 400
        assert "Cannot approve" in response.json()["detail"]
    
    def test_reject_document(self, client: TestClient, admin_token, db):
        """Test rejecting a document"""
        from app.models.document import Document
        
        doc = Document(
            filename="test.pdf",
            file_path="/uploads/test.pdf",
            uploaded_by=2,
            status="pending"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.put(
            f"/documents/{doc.id}/reject",
            json={"comment": "Rejected"},
            headers=headers
        )
        assert response.status_code == 200
        assert response.json()["status"] == "rejected"
    
    def test_user_cannot_approve(self, client: TestClient, user_token, db):
        """Test that regular users cannot approve documents"""
        from app.models.document import Document
        
        doc = Document(
            filename="test.pdf",
            file_path="/uploads/test.pdf",
            uploaded_by=2,
            status="pending"
        )
        db.add(doc)
        db.commit()
        
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.put(
            f"/documents/{doc.id}/approve",
            json={"comment": "Approved"},
            headers=headers
        )
        assert response.status_code == 403
