# 📚 Complete API Endpoints Reference

## Authentication Endpoints

### 1. Register User
```
POST /auth/register
No Auth Required

Request:
{
  "email": "user@example.com",
  "password": "password123"
}

Response (201):
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  }
}
```

### 2. Login
```
POST /auth/login
No Auth Required

Request:
{
  "email": "user@example.com",
  "password": "password123"
}

Response (200):
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc..."
}
```

### 3. Refresh Token
```
POST /auth/refresh
No Auth Required

Request:
{
  "refresh_token": "eyJhbGc..."
}

Response (200):
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc..."
}
```

---

## User Management Endpoints

### 1. Get Current User Profile
```
GET /users/me
Auth Required: YES

Response (200):
{
  "id": 1,
  "email": "user@example.com",
  "role": "user"
}
```

### 2. List All Users
```
GET /users/
Auth Required: YES
Role Required: ADMIN

Response (200):
[
  {
    "id": 1,
    "email": "admin@example.com",
    "role": "admin"
  },
  {
    "id": 2,
    "email": "user@example.com",
    "role": "user"
  }
]
```

### 3. Get User by ID
```
GET /users/{user_id}
Auth Required: YES
Role Required: ADMIN

Response (200):
{
  "id": 1,
  "email": "user@example.com",
  "role": "user"
}
```

### 4. Update User
```
PATCH /users/{user_id}
Auth Required: YES
Role Required: ADMIN

Request:
{
  "role": "admin",
  "password": "newpassword123"
}

Response (200):
{
  "id": 1,
  "email": "user@example.com",
  "role": "admin"
}
```

### 5. Delete User
```
DELETE /users/{user_id}
Auth Required: YES
Role Required: ADMIN

Response: 204 No Content
```

### 6. Update Own Password
```
PUT /users/{user_id}/password
Auth Required: YES

Request:
{
  "password": "newpassword123"
}

Response (200):
{
  "message": "Password updated successfully"
}
```

---

## Document Endpoints

### 1. Upload Document
```
POST /documents/upload
Auth Required: YES
Role Required: ANY

Request: multipart/form-data
- file: <binary file>

Response (200):
{
  "message": "Document uploaded successfully",
  "document_id": 1,
  "status": "pending"
}
```

### 2. Get My Documents
```
GET /documents/my
Auth Required: YES
Role Required: ANY

Response (200):
[
  {
    "id": 1,
    "filename": "document.pdf",
    "file_path": "/uploads/document.pdf",
    "status": "pending",
    "uploaded_by": 1,
    "created_at": "2026-02-19T16:42:17",
    "updated_at": "2026-02-19T16:42:17"
  }
]
```

### 3. Get All Documents (Admin)
```
GET /documents/
Auth Required: YES
Role Required: ADMIN

Response (200):
[
  {
    "id": 1,
    "filename": "document.pdf",
    "file_path": "/uploads/document.pdf",
    "status": "pending",
    "uploaded_by": 1,
    "approved_by": null,
    "approval_date": null,
    "approval_comment": null,
    "created_at": "2026-02-19T16:42:17",
    "updated_at": "2026-02-19T16:42:17"
  }
]
```

### 4. Get Document Details
```
GET /documents/{doc_id}
Auth Required: YES
Role Required: ADMIN

Response (200):
{
  "id": 1,
  "filename": "document.pdf",
  "file_path": "/uploads/document.pdf",
  "status": "approved",
  "uploaded_by": 1,
  "approved_by": 2,
  "approval_date": "2026-02-19T16:45:12",
  "approval_comment": "Approved",
  "created_at": "2026-02-19T16:42:17",
  "updated_at": "2026-02-19T16:45:12"
}
```

### 5. Approve Document
```
PUT /documents/{doc_id}/approve
Auth Required: YES
Role Required: ADMIN

Request:
{
  "comment": "Approved - meets requirements"
}

Response (200):
{
  "message": "Document approved successfully",
  "document_id": 1,
  "status": "approved",
  "approved_by": "admin@example.com",
  "approval_date": "2026-02-19T16:45:12"
}

🔄 Background Tasks:
  ✓ Log to document_status_history
  ✓ Send email notification
  ✓ Generate audit log
```

### 6. Reject Document
```
PUT /documents/{doc_id}/reject
Auth Required: YES
Role Required: ADMIN

Request:
{
  "comment": "Invalid format - please resubmit"
}

Response (200):
{
  "message": "Document rejected successfully",
  "document_id": 1,
  "status": "rejected",
  "rejected_by": "admin@example.com",
  "rejection_date": "2026-02-19T16:45:12",
  "reason": "Invalid format - please resubmit"
}

🔄 Background Tasks:
  ✓ Log to document_status_history
  ✓ Send email notification
  ✓ Generate audit log
```

### 7. Advanced Search
```
GET /documents/search/advanced
Auth Required: YES
Role Required: ADMIN

Query Parameters:
- status: pending | approved | rejected (optional)
- search: filename search (optional, case-insensitive)
- start_date: YYYY-MM-DD (optional)
- end_date: YYYY-MM-DD (optional)
- skip: 0 (default)
- limit: 10 (default, max 100)

Example:
GET /documents/search/advanced?status=pending&search=invoice&skip=0&limit=10

Response (200):
{
  "total": 25,
  "skip": 0,
  "limit": 10,
  "count": 10,
  "documents": [
    {
      "id": 1,
      "filename": "invoice_001.pdf",
      "status": "pending",
      "uploaded_by": 2,
      "approved_by": null,
      "approval_comment": null,
      "created_at": "2026-02-19T16:42:17",
      "updated_at": "2026-02-19T16:42:17"
    }
  ]
}
```

### 8. Get Document History
```
GET /documents/{doc_id}/history
Auth Required: YES
Role Required: ADMIN

Response (200):
{
  "document_id": 1,
  "filename": "document.pdf",
  "current_status": "approved",
  "history_count": 2,
  "history": [
    {
      "id": 2,
      "status": "approved",
      "changed_by": 3,
      "comment": "Approved",
      "created_at": "2026-02-19T16:45:12"
    },
    {
      "id": 1,
      "status": "pending",
      "changed_by": 1,
      "comment": null,
      "created_at": "2026-02-19T16:42:17"
    }
  ]
}
```

### 9. Get Approved Documents (Public)
```
GET /documents/public/approved
Auth Required: NO
Role Required: NONE

Query Parameters:
- search: filename search (optional)
- skip: 0 (default)
- limit: 10 (default)

Response (200):
{
  "total": 15,
  "skip": 0,
  "limit": 10,
  "count": 10,
  "message": "Only approved documents are visible",
  "documents": [
    {
      "id": 2,
      "filename": "approved_doc.pdf",
      "created_at": "2026-02-19T16:42:17",
      "uploaded_by_id": 1,
      "file_path": "/uploads/approved_doc.pdf"
    }
  ]
}
```

---

## Health & Info Endpoints

### Health Check
```
GET /health
No Auth Required

Response (200):
{
  "status": "healthy",
  "timestamp": "2026-02-19T16:45:12"
}
```

### API Root
```
GET /
No Auth Required

Response (200):
{
  "message": "Welcome to Document Management API",
  "docs": "/api/docs",
  "version": "1.0.0"
}
```

---

## Error Response Format

All errors return structured format:

```json
{
  "success": false,
  "error_code": "ERROR_CODE",
  "message": "Human-readable error message",
  "timestamp": "2026-02-19T16:45:12"
}
```

### Common Error Codes
- `UNAUTHORIZED` - Missing/invalid token (401)
- `FORBIDDEN` - Insufficient permissions (403)
- `DOCUMENT_NOT_FOUND` - Document doesn't exist (404)
- `INVALID_FILE_TYPE` - File type not allowed (400)
- `FILE_SIZE_EXCEEDED` - File too large (400)
- `INVALID_DOCUMENT_STATUS` - Cannot perform action in current status (400)
- `DUPLICATE_EMAIL` - Email already registered (409)
- `INTERNAL_SERVER_ERROR` - Server error (500)

---

## Status Codes Reference

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Success, no response body |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing/invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Duplicate email |
| 500 | Internal Server Error |

---

## Authentication Header

All protected endpoints require:

```
Authorization: Bearer <access_token>
```

### Example cURL:
```bash
curl -H "Authorization: Bearer eyJhbGc..." \
     https://api.example.com/documents/
```

---

## Pagination Guidelines

All list endpoints support pagination:

```
GET /documents/search/advanced?skip=0&limit=10
```

- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 10, max: 100)
- `total`: Total number of matching records
- `count`: Number of records returned

### Example:
```json
{
  "total": 100,
  "skip": 10,
  "limit": 10,
  "count": 10,
  "documents": [...]
}
```

---

## Role Permissions Matrix

| Endpoint | Public | User | Admin |
|----------|--------|------|-------|
| Register | ✅ | ✅ | ✅ |
| Login | ✅ | ✅ | ✅ |
| Refresh Token | ✅ | ✅ | ✅ |
| Get Current User | - | ✅ | ✅ |
| Upload Document | - | ✅ | ✅ |
| View Own Documents | - | ✅ | ✅ |
| View All Documents | - | ❌ | ✅ |
| Approve Document | - | ❌ | ✅ |
| Reject Document | - | ❌ | ✅ |
| Search Advanced | - | ❌ | ✅ |
| View History | - | ❌ | ✅ |
| View Approved Docs | ✅ | ✅ | ✅ |

---

## API Documentation

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`
- **OpenAPI Schema**: `http://localhost:8000/api/openapi.json`
