# Document Management API - Complete Implementation Guide

## 📋 Overview

A production-ready Document Management System built with FastAPI that demonstrates:
- ✅ Full Authentication & Authorization (JWT)
- ✅ Role-Based Access Control (Admin, User)
- ✅ Document Upload & Management
- ✅ Approval Workflow with Background Tasks
- ✅ Advanced Search, Filtering & Pagination
- ✅ Comprehensive Testing
- ✅ Proper Error Handling
- ✅ API Documentation

---

## 🗓️ Implementation Timeline (7 Days)

### ✅ Day 1 – Project Setup + Authentication
- FastAPI project structure (modular)
- JWT Authentication (access + refresh tokens)
- Password hashing with bcrypt
- User registration & login
- Role system (admin, user)

### ✅ Day 2 – Database Design
- SQLAlchemy ORM models:
  - `users` - User accounts with roles
  - `documents` - Document metadata
  - `document_status_history` - Audit trail
- Relational schema with foreign keys
- Database migrations ready structure

### ✅ Day 3 – File Upload & Storage
- Document upload endpoint
- File type validation (PDF, images)
- File size limits (5MB max)
- Metadata storage in database
- File path management

### ✅ Day 4 – RBAC Implementation
- Role checking dependencies
- Admin-only endpoints
- User-specific document access
- Proper permission enforcement
- 403 error handling for unauthorized access

### ✅ Day 5 – Background Tasks
- Document approval logging
- Email notification simulation
- Audit log generation
- Status change tracking
- Async task processing

### ✅ Day 6 – Filtering, Pagination, Search
- Advanced document search
- Filter by status (pending/approved/rejected)
- Filter by date range
- Search by filename
- Result pagination (skip/limit)
- Public approved documents endpoint

### ✅ Day 7 – Testing & Documentation
- Comprehensive pytest test suite
- 30+ test cases covering all scenarios
- Custom exception handling
- Structured error responses
- Swagger documentation
- Health check endpoint

---

## 🏗️ Project Structure

```
app/
├── main.py                          # FastAPI app with exception handlers
├── database.py                      # Database configuration
├── core/
│   ├── config.py                   # Configuration (secrets, paths)
│   ├── security.py                 # Password hashing & JWT tokens
│   ├── exceptions.py               # Custom exceptions
│   └── enums.py                    # Role enumerations
├── models/
│   ├── user.py                     # User model
│   ├── document.py                 # Document model
│   └── document_status_history.py  # Audit trail
├── schemas/
│   ├── auth.py                     # Login/Register schemas
│   ├── user.py                     # User response schemas
│   ├── document.py                 # Document schemas
│   ├── filters.py                  # Filter schemas
│   └── responses.py                # Standard response schemas
├── routes/
│   ├── auth.py                     # Authentication endpoints
│   ├── users.py                    # User management
│   └── documents.py                # Document endpoints
├── services/
│   ├── auth_service.py             # Auth business logic
│   ├── document_service.py         # Document business logic
│   └── background_tasks.py         # Background task handlers
├── dependencies/
│   └── auth.py                     # Dependency injection
└── utils/
    └── file_handler.py             # File upload utilities

tests/
├── conftest.py                     # Pytest configuration & fixtures
├── test_auth.py                    # Authentication tests
├── test_users.py                   # User management tests
└── test_documents.py               # Document endpoint tests
```

---

## 🔐 Authentication Flow

### Request Access Token
```bash
POST /auth/login
Content-Type: application/json

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

### Use Token
```bash
GET /documents/my
Authorization: Bearer eyJhbGc...
```

### Refresh Token
```bash
POST /auth/refresh
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

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---|
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/login` | Login user | No |
| POST | `/auth/refresh` | Refresh token | No |

### User Management

| Method | Endpoint | Description | Auth Required | Role Required |
|--------|----------|-------------|---|---|
| GET | `/users/me` | Get current user | Yes | Any |
| GET | `/users/` | List all users | Yes | Admin |
| GET | `/users/{id}` | Get user details | Yes | Admin |
| PATCH | `/users/{id}` | Update user role | Yes | Admin |
| DELETE | `/users/{id}` | Delete user | Yes | Admin |
| PUT | `/users/{id}/password` | Update password | Yes | Any |

### Documents

| Method | Endpoint | Description | Auth Required | Role Required |
|--------|----------|-------------|---|---|
| POST | `/documents/upload` | Upload document | Yes | Any |
| GET | `/documents/my` | Get own documents | Yes | Any |
| GET | `/documents/` | Get all documents | Yes | Admin |
| GET | `/documents/{id}` | Get document details | Yes | Admin |
| PUT | `/documents/{id}/approve` | Approve document | Yes | Admin |
| PUT | `/documents/{id}/reject` | Reject document | Yes | Admin |
| GET | `/documents/search/advanced` | Search with filters | Yes | Admin |
| GET | `/documents/{id}/history` | Get approval history | Yes | Admin |
| GET | `/documents/public/approved` | Get approved docs | No | Any |

---

## 🔍 Advanced Search Example

```bash
GET /documents/search/advanced?status=pending&search=invoice&skip=0&limit=10
Authorization: Bearer <admin_token>

Response (200):
{
  "total": 25,
  "skip": 0,
  "limit": 10,
  "count": 10,
  "documents": [
    {
      "id": 1,
      "filename": "invoice_2024.pdf",
      "status": "pending",
      "uploaded_by": 2,
      "created_at": "2026-02-19T16:42:17.842182"
    }
  ]
}
```

---

## ✅ Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_auth.py -v
```

### Run with Coverage
```bash
pytest --cov=app tests/
```

### Test Cases Included
- ✅ User registration & duplicate handling
- ✅ Login with correct/incorrect credentials
- ✅ Token refresh
- ✅ Document upload
- ✅ Admin approval/rejection
- ✅ Role-based access control
- ✅ Search & filtering
- ✅ Pagination
- ✅ Error handling

---

## 🔧 Configuration

Edit `app/core/config.py`:

```python
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
UPLOAD_FOLDER = "uploads/"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_TYPES = ["application/pdf", "image/jpeg", "image/png"]
```

---

## 📊 Database Models

### User
```python
users:
  - id: UUID (primary key)
  - email: str (unique)
  - hashed_password: str
  - role: str (admin, user)
  - created_at: datetime
```

### Document
```python
documents:
  - id: UUID (primary key)
  - filename: str
  - file_path: str
  - status: str (pending, approved, rejected)
  - uploaded_by: UUID (FK to users)
  - approved_by: UUID (FK to users, nullable)
  - approval_date: datetime (nullable)
  - approval_comment: str (nullable)
  - created_at: datetime
  - updated_at: datetime
```

### DocumentStatusHistory
```python
document_status_history:
  - id: UUID (primary key)
  - document_id: UUID (FK to documents)
  - status: str (pending, approved, rejected)
  - changed_by: UUID (FK to users)
  - comment: str (nullable)
  - created_at: datetime
```

---

## 🚀 Deployment Checklist

- [ ] Set proper `SECRET_KEY` in production
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure CORS properly
- [ ] Set up HTTPS
- [ ] Configure file upload path
- [ ] Set up logging
- [ ] Configure email service for notifications
- [ ] Run migrations
- [ ] Run test suite
- [ ] Setup CI/CD pipeline

---

## 📖 API Documentation

Interactive documentation available at:
- **Swagger**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`
- **OpenAPI Schema**: `http://localhost:8000/api/openapi.json`

---

## 🔒 Security Features

✅ Password hashing with bcrypt
✅ JWT tokens with expiration
✅ Role-based access control
✅ CORS protection ready
✅ SQL injection prevention (SQLAlchemy)
✅ Input validation (Pydantic)
✅ Audit trail/logging
✅ File type validation
✅ File size limits
✅ Secure token storage

---

## 🐛 Error Handling

All errors return structured response:

```json
{
  "success": false,
  "error_code": "INVALID_FILE_TYPE",
  "message": "Invalid file type. Allowed types: application/pdf, image/jpeg, image/png",
  "timestamp": "2026-02-19T16:45:12.946142"
}
```

---

## 🔄 Background Tasks

When a document is approved/rejected:
1. ✅ Status change logged in history table
2. ✅ Audit log generated
3. ✅ Email notification sent (simulated)
4. ✅ Tasks run asynchronously

---

## 📝 Example Workflows

### Complete Approval Workflow
```
1. User uploads document → status = "pending"
2. Admin views all documents → GET /documents/
3. Admin approves document → PUT /documents/{id}/approve
4. Background tasks:
   - Log approval in history
   - Send notification email
   - Generate audit log
5. Document now visible in public endpoint → GET /documents/public/approved
```

---

## 🤝 Contributing

1. Create feature branch
2. Write tests
3. Ensure all tests pass
4. Submit PR

---

## 📄 License

MIT License

---

## 📞 Support

For issues or questions, please check the test files for usage examples.
