# Quick Start Guide

## 1. Installation

```bash
cd c:\Users\dell\Desktop\FastAPI.Task
pip install -r requirements.txt
```

## 2. Database Setup

```bash
# Seed database with demo data
python seed_database.py
```

## 3. Run Server

```bash
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`

## 4. API Documentation

Visit: `http://localhost:8000/api/docs`

## 5. Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=app tests/
```

## 6. Demo Credentials

### Admin Account
```
Email: admin@example.com
Password: admin123
```

### Regular User
```
Email: user1@example.com
Password: password123
```

## 7. Common API Calls

### Get Admin Token
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

### View All Documents (Admin Only)
```bash
curl -X GET "http://localhost:8000/documents/" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### Approve Document
```bash
curl -X PUT "http://localhost:8000/documents/1/approve" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":"Approved"}'
```

### Advanced Search
```bash
curl -X GET "http://localhost:8000/documents/search/advanced?status=pending&search=invoice&skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### Get Approved Documents (No Auth)
```bash
curl -X GET "http://localhost:8000/documents/public/approved"
```

## 8. Project Features

✅ Day 1: Authentication with JWT  
✅ Day 2: Database with SQLAlchemy  
✅ Day 3: File upload & validation  
✅ Day 4: Role-based access control  
✅ Day 5: Background tasks  
✅ Day 6: Search, filtering & pagination  
✅ Day 7: Comprehensive testing & documentation  

## 9. File Structure

```
app/
├── main.py              # FastAPI app
├── database.py          # DB config
├── core/                # Config, security, exceptions
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── routes/              # API endpoints
├── services/            # Business logic
├── dependencies/        # Dependency injection
└── utils/               # Utilities

tests/
├── conftest.py          # Pytest config
├── test_auth.py         # Auth tests
├── test_documents.py    # Document tests
└── test_users.py        # User tests
```

## 10. Troubleshooting

**Issue**: Port 8000 already in use
```bash
uvicorn app.main:app --reload --port 8001
```

**Issue**: Database locked
```bash
# Delete the database and reseed
rm dms.db
python seed_database.py
```

**Issue**: Import errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```
