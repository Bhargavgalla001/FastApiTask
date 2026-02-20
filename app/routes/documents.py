from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.models.document import Document
from app.models.user import User
from app.models.document_status_history import DocumentStatusHistory
from app.dependencies.auth import get_db, get_current_user, admin_only
from app.schemas.document import DocumentResponse, DocumentDetailResponse, DocumentAdminView, DocumentApprovalRequest
from app.utils.file_handler import save_file
from app.services.background_tasks import (
    log_document_approval,
    simulate_email_notification,
    generate_audit_log
)

router = APIRouter(prefix="/documents", tags=["Documents"])


# ==================================================
# 👤 USER → Upload Document
# ==================================================
@router.post("/upload", response_model=dict)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """User uploads a document (requires authentication)"""
    file_path = save_file(file)

    new_doc = Document(
        filename=file.filename,
        file_path=file_path,
        uploaded_by=current_user.id,
        status="pending"
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {
        "message": "Document uploaded successfully",
        "document_id": new_doc.id,
        "status": "pending"
    }


# ==================================================
# 👤 USER → View Only Their Documents
# ==================================================
@router.get("/my", response_model=list[DocumentResponse])
def get_my_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View only your own uploaded documents"""
    documents = db.query(Document).filter(
        Document.uploaded_by == current_user.id
    ).all()

    return documents


# ==================================================
# � USER → Delete Their Own Document
# ==================================================
@router.delete("/{doc_id}", response_model=dict)
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete your own document (users can only delete their own documents, admins can delete any)"""
    document = db.query(Document).filter(Document.id == doc_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Check if user is the owner or an admin
    if document.uploaded_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own documents"
        )

    # Delete the document
    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully",
        "document_id": doc_id,
        "filename": document.filename
    }


# ==================================================
# �👑 ADMIN → View All Documents
# ==================================================
@router.get("/", response_model=list[DocumentAdminView])
def get_all_documents(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_only)
):
    """View all documents in the system (Admin only)"""
    documents = db.query(Document).all()
    return documents


# ==================================================
# 👑 ADMIN → Get Single Document Details
# ==================================================
@router.get("/{doc_id}", response_model=DocumentDetailResponse)
def get_document_details(
    doc_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_only)
):
    """Get detailed view of a specific document (Admin only)"""
    document = db.query(Document).filter(Document.id == doc_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document


# ==================================================
# 👑 ADMIN → Approve Document
# ==================================================
@router.put("/{doc_id}/approve", response_model=dict)
def approve_document(
    doc_id: int,
    data: DocumentApprovalRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_only)
):
    """Approve a document (Admin only) - Triggers background tasks"""
    document = db.query(Document).filter(Document.id == doc_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.status != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot approve document with status: {document.status}"
        )

    # Update document status
    document.status = "approved"
    document.approved_by = admin.id
    document.approval_date = datetime.utcnow()
    document.approval_comment = data.comment
    document.updated_at = datetime.utcnow()

    # Add status change to history
    history_entry = DocumentStatusHistory(
        document_id=doc_id,
        status="approved",
        changed_by=admin.id,
        comment=data.comment
    )
    db.add(history_entry)
    db.commit()
    db.refresh(document)

    # Add background tasks
    background_tasks.add_task(
        log_document_approval,
        document_id=doc_id,
        admin_id=admin.id,
        status="approved",
        comment=data.comment
    )
    
    background_tasks.add_task(
        simulate_email_notification,
        document_id=doc_id,
        status="approved",
        uploader_email=document.owner.email,
        admin_email=admin.email,
        comment=data.comment
    )
    
    background_tasks.add_task(
        generate_audit_log,
        action="DOCUMENT_APPROVED",
        user_id=admin.id,
        document_id=doc_id,
        details={"comment": data.comment}
    )

    return {
        "message": "Document approved successfully",
        "document_id": doc_id,
        "status": "approved",
        "approved_by": admin.email,
        "approval_date": document.approval_date
    }


# ==================================================
# 👑 ADMIN → Reject Document
# ==================================================
@router.put("/{doc_id}/reject", response_model=dict)
def reject_document(
    doc_id: int,
    data: DocumentApprovalRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_only)
):
    """Reject a document (Admin only) - Triggers background tasks"""
    document = db.query(Document).filter(Document.id == doc_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.status != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot reject document with status: {document.status}"
        )

    # Update document status
    document.status = "rejected"
    document.approved_by = admin.id
    document.approval_date = datetime.utcnow()
    document.approval_comment = data.comment
    document.updated_at = datetime.utcnow()

    # Add status change to history
    history_entry = DocumentStatusHistory(
        document_id=doc_id,
        status="rejected",
        changed_by=admin.id,
        comment=data.comment
    )
    db.add(history_entry)
    db.commit()
    db.refresh(document)

    # Add background tasks
    background_tasks.add_task(
        log_document_approval,
        document_id=doc_id,
        admin_id=admin.id,
        status="rejected",
        comment=data.comment
    )
    
    background_tasks.add_task(
        simulate_email_notification,
        document_id=doc_id,
        status="rejected",
        uploader_email=document.owner.email,
        admin_email=admin.email,
        comment=data.comment
    )
    
    background_tasks.add_task(
        generate_audit_log,
        action="DOCUMENT_REJECTED",
        user_id=admin.id,
        document_id=doc_id,
        details={"reason": data.comment}
    )

    return {
        "message": "Document rejected successfully",
        "document_id": doc_id,
        "status": "rejected",
        "rejected_by": admin.email,
        "rejection_date": document.approval_date,
        "reason": data.comment
    }


# ==================================================
# 👑 ADMIN → Advanced Search with Filters & Pagination
# ==================================================
@router.get("/search/advanced", response_model=dict)
def search_documents_advanced(
    status: Optional[str] = Query(None, description="Filter by status: pending/approved/rejected"),
    search: Optional[str] = Query(None, description="Search by filename"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Pagination skip"),
    limit: int = Query(10, ge=1, le=100, description="Pagination limit"),
    db: Session = Depends(get_db),
    admin: User = Depends(admin_only)
):
    """
    Advanced document search with filtering and pagination (Admin only)
    
    Query Parameters:
    - status: pending, approved, or rejected
    - search: search by filename (partial match)
    - start_date: filters documents created after this date
    - end_date: filters documents created before this date
    - skip: pagination skip (default 0)
    - limit: pagination limit (default 10, max 100)
    """
    query = db.query(Document)
    
    # Filter by status
    if status:
        valid_statuses = ["pending", "approved", "rejected"]
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        query = query.filter(Document.status == status)
    
    # Search by filename
    if search:
        query = query.filter(Document.filename.ilike(f"%{search}%"))
    
    # Filter by date range
    if start_date:
        try:
            from datetime import datetime as dt
            start = dt.fromisoformat(start_date)
            query = query.filter(Document.created_at >= start)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid start_date format. Use YYYY-MM-DD"
            )
    
    if end_date:
        try:
            from datetime import datetime as dt
            end = dt.fromisoformat(end_date)
            query = query.filter(Document.created_at <= end)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid end_date format. Use YYYY-MM-DD"
            )
    
    # Get total count before pagination
    total_count = query.count()
    
    # Apply pagination
    documents = query.offset(skip).limit(limit).all()
    
    return {
        "total": total_count,
        "skip": skip,
        "limit": limit,
        "count": len(documents),
        "documents": [
            {
                "id": doc.id,
                "filename": doc.filename,
                "status": doc.status,
                "uploaded_by": doc.uploaded_by,
                "approved_by": doc.approved_by,
                "approval_comment": doc.approval_comment,
                "created_at": doc.created_at.isoformat(),
                "updated_at": doc.updated_at.isoformat()
            }
            for doc in documents
        ]
    }


# ==================================================
# 👑 ADMIN → Get Document Status History
# ==================================================
@router.get("/{doc_id}/history", response_model=dict)
def get_document_history(
    doc_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_only)
):
    """Get complete status change history for a document (Admin only)"""
    document = db.query(Document).filter(Document.id == doc_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    history_records = db.query(DocumentStatusHistory).filter(
        DocumentStatusHistory.document_id == doc_id
    ).order_by(DocumentStatusHistory.created_at.desc()).all()
    
    return {
        "document_id": doc_id,
        "filename": document.filename,
        "current_status": document.status,
        "history_count": len(history_records),
        "history": [
            {
                "id": record.id,
                "status": record.status,
                "changed_by": record.changed_by,
                "comment": record.comment,
                "created_at": record.created_at.isoformat()
            }
            for record in history_records
        ]
    }


# ==================================================
# 👁️ PUBLIC → Get Approved Documents (Read-Only)
# ==================================================
@router.get("/public/approved", response_model=dict)
def get_approved_documents(
    search: Optional[str] = Query(None, description="Search by filename"),
    skip: int = Query(0, ge=0, description="Pagination skip"),
    limit: int = Query(10, ge=1, le=100, description="Pagination limit"),
    db: Session = Depends(get_db)
):
    """
    Get approved documents (Public access - no authentication required)
    Only approved documents are publicly accessible
    """
    query = db.query(Document).filter(Document.status == "approved")
    
    # Search by filename if provided
    if search:
        query = query.filter(Document.filename.ilike(f"%{search}%"))
    
    # Get total count
    total_count = query.count()
    
    # Apply pagination and order by latest first
    documents = query.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total_count,
        "skip": skip,
        "limit": limit,
        "count": len(documents),
        "message": "Only approved documents are visible",
        "documents": [
            {
                "id": doc.id,
                "filename": doc.filename,
                "created_at": doc.created_at.isoformat(),
                "uploaded_by_id": doc.uploaded_by,
                "file_path": doc.file_path
            }
            for doc in documents
        ]
    }

