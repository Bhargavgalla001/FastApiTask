# Quick Reference - Admin Document Management

## Database Credentials
```
Admin Email: admin@example.com
Admin Pass:  admin123
User Email:  user1@example.com
User Pass:   password123
```

## Admin Endpoints

### 1️⃣ VIEW ALL DOCUMENTS
```bash
GET /documents/
Authorization: Bearer <ADMIN_TOKEN>

Response: List of all documents with full details
Status: 200 ✅ | 403 ❌ (User can't access)
```

### 2️⃣ APPROVE DOCUMENT  
```bash
PUT /documents/1/approve
Authorization: Bearer <ADMIN_TOKEN>

{
  "comment": "Approved - meets requirements"
}

Response: Confirmation with admin name, date
Status: 200 ✅ | 400 ❌ (Not pending)
```

### 3️⃣ REJECT DOCUMENT
```bash
PUT /documents/1/reject
Authorization: Bearer <ADMIN_TOKEN>

{
  "comment": "Invalid format"
}

Response: Confirmation with rejection reason
Status: 200 ✅ | 400 ❌ (Not pending)
```

## User Endpoints

### 1️⃣ UPLOAD DOCUMENT
```bash
POST /documents/upload
Authorization: Bearer <USER_TOKEN>
Content-Type: multipart/form-data

file: document.pdf

Status: 200 ✅ (pending approval)
```

### 2️⃣ VIEW OWN DOCUMENTS
```bash
GET /documents/my
Authorization: Bearer <USER_TOKEN>

Status: 200 ✅ (only own docs)
```

## Testing Commands

### Get Admin Token
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

### View All Documents (Admin)
```bash
curl -X GET http://localhost:8000/documents/ \
  -H "Authorization: Bearer TOKEN"
```

### Approve Document
```bash
curl -X PUT http://localhost:8000/documents/1/approve \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"Approved"}'
```

### Security Test - User Can't Approve
```bash
# Get user token
USER_TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user1@example.com","password":"password123"}' \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# Try to approve (should get 403)
curl -X GET http://localhost:8000/documents/ \
  -H "Authorization: Bearer $USER_TOKEN"

# Result: {"detail":"Admin access required"}
```

## Key Security Features

✅ Role embedded in JWT token  
✅ Admin-only dependency injection  
✅ Approval tracked by admin ID  
✅ Timestamp recorded for each action  
✅ Comment/reason stored for audit  
✅ 403 Forbidden for unauthorized users  
✅ Atomic database transactions  

## Database Sample Data

| User | Role | Email | Can Do |
|------|------|-------|--------|
| admin | admin | admin@example.com | View all docs, Approve, Reject |
| user1 | user | user1@example.com | Upload, View own |
| user2 | user | user2@example.com | Upload, View own |

| Doc | Status | Uploaded By | Approved By |
|-----|--------|-------------|-------------|
| 1 | pending → approved | user1 | admin |
| 2 | approved | user2 | admin |
| 3 | rejected | user1 | admin |

## Run Tests
```bash
# Seed database with test data
python seed_database.py

# Start server
uvicorn app.main:app --reload

# Run tests
python test_admin_documents.py
```
