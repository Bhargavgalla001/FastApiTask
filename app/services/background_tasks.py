import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.document_status_history import DocumentStatusHistory
from app.models.document import Document
from app.models.user import User

logger = logging.getLogger(__name__)

def log_document_approval(
    document_id: int,
    admin_id: int,
    status: str,
    comment: str = None
):
    """
    Background task to log document approval/rejection
    Called asynchronously when admin approves/rejects document
    """
    db = SessionLocal()
    try:
        # Log the status change in history table
        history_entry = DocumentStatusHistory(
            document_id=document_id,
            status=status,
            changed_by=admin_id,
            comment=comment,
            created_at=datetime.utcnow()
        )
        db.add(history_entry)
        db.commit()
        
        # Get document and admin info for logging
        document = db.query(Document).filter(Document.id == document_id).first()
        admin = db.query(User).filter(User.id == admin_id).first()
        
        if document and admin:
            log_message = (
                f"DOCUMENT APPROVAL LOG:\n"
                f"  Document ID: {document_id}\n"
                f"  Filename: {document.filename}\n"
                f"  Status: {status.upper()}\n"
                f"  Admin: {admin.email}\n"
                f"  Comment: {comment or 'N/A'}\n"
                f"  Timestamp: {datetime.utcnow().isoformat()}"
            )
            logger.info(log_message)
            print(log_message)  # Also print to console for visibility
        
    except Exception as e:
        logger.error(f"Error logging document approval: {str(e)}")
    finally:
        db.close()


def simulate_email_notification(
    document_id: int,
    status: str,
    uploader_email: str,
    admin_email: str = None,
    comment: str = None
):
    """
    Background task to simulate email notification
    In production, this would call an email service (SendGrid, AWS SES, etc.)
    """
    try:
        message = (
            f"EMAIL NOTIFICATION:\n"
            f"  To: {uploader_email}\n"
            f"  Subject: Document {status.upper()}\n"
            f"  Body:\n"
            f"    Your document (ID: {document_id}) has been {status}.\n"
        )
        
        if comment:
            message += f"    Reason: {comment}\n"
        
        if admin_email:
            message += f"    Processed by: {admin_email}\n"
        
        logger.info(message)
        print(message)  # Console output for visibility in development
        
    except Exception as e:
        logger.error(f"Error sending email notification: {str(e)}")


def generate_audit_log(
    action: str,
    user_id: int,
    document_id: int,
    details: dict = None
):
    """
    Background task to generate audit log
    Useful for compliance and tracking user actions
    """
    try:
        log_entry = (
            f"AUDIT LOG:\n"
            f"  Action: {action}\n"
            f"  User ID: {user_id}\n"
            f"  Document ID: {document_id}\n"
            f"  Timestamp: {datetime.utcnow().isoformat()}\n"
        )
        
        if details:
            log_entry += f"  Details: {details}\n"
        
        logger.info(log_entry)
        
    except Exception as e:
        logger.error(f"Error generating audit log: {str(e)}")
