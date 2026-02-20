"""
Database seeding script
Creates admin user and test data
Run this once to populate the database
"""

from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.document import Document
from app.core.security import hash_password
from datetime import datetime, timedelta

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Clear existing data (optional - comment out if you want to keep existing data)
    # db.query(Document).delete()
    # db.query(User).delete()
    # db.commit()

    # Check if admin already exists
    admin_exists = db.query(User).filter(User.email == "admin@example.com").first()
    
    if not admin_exists:
        # Create Admin User
        admin = User(
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            role="admin"
        )
        db.add(admin)
        print("✅ Admin user created: admin@example.com")
    else:
        admin = admin_exists
        print("✅ Admin user already exists: admin@example.com")

    # Create test users if they don't exist
    user1_exists = db.query(User).filter(User.email == "user1@example.com").first()
    if not user1_exists:
        user1 = User(
            email="user1@example.com",
            hashed_password=hash_password("password123"),
            role="user"
        )
        db.add(user1)
        print("✅ Test user created: user1@example.com")
    else:
        user1 = user1_exists

    user2_exists = db.query(User).filter(User.email == "user2@example.com").first()
    if not user2_exists:
        user2 = User(
            email="user2@example.com",
            hashed_password=hash_password("password123"),
            role="user"
        )
        db.add(user2)
        print("✅ Test user created: user2@example.com")
    else:
        user2 = user2_exists

    db.commit()

    # Create sample documents
    doc1_exists = db.query(Document).filter(
        Document.filename == "sample_document_1.pdf"
    ).first()
    
    if not doc1_exists:
        doc1 = Document(
            filename="sample_document_1.pdf",
            file_path="/uploads/sample_document_1.pdf",
            status="pending",
            uploaded_by=user1.id
        )
        db.add(doc1)
        print("✅ Sample document 1 created (pending)")

    doc2_exists = db.query(Document).filter(
        Document.filename == "sample_document_2.pdf"
    ).first()
    
    if not doc2_exists:
        doc2 = Document(
            filename="sample_document_2.pdf",
            file_path="/uploads/sample_document_2.pdf",
            status="approved",
            uploaded_by=user2.id,
            approved_by=admin.id,
            approval_date=datetime.utcnow(),
            approval_comment="Document meets requirements"
        )
        db.add(doc2)
        print("✅ Sample document 2 created (approved by admin)")

    doc3_exists = db.query(Document).filter(
        Document.filename == "sample_document_3.pdf"
    ).first()
    
    if not doc3_exists:
        doc3 = Document(
            filename="sample_document_3.pdf",
            file_path="/uploads/sample_document_3.pdf",
            status="rejected",
            uploaded_by=user1.id,
            approved_by=admin.id,
            approval_date=datetime.utcnow(),
            approval_comment="Document format is incorrect"
        )
        db.add(doc3)
        print("✅ Sample document 3 created (rejected by admin)")

    db.commit()

    print("\n" + "="*50)
    print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
    print("="*50)
    print("\n📊 Summary:")
    print(f"  Admin: admin@example.com / admin123")
    print(f"  User 1: user1@example.com / password123")
    print(f"  User 2: user2@example.com / password123")
    print("\n🔐 Admin Can:")
    print("  • View all documents")
    print("  • Approve/Reject documents")
    print("  • Manage users")
    print("\n👤 Users Can:")
    print("  • Upload documents")
    print("  • View only their documents")

finally:
    db.close()
