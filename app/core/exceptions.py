from fastapi import HTTPException, status
from typing import Optional


class DocumentAPIException(HTTPException):
    """Base custom exception for Document API"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code or "UNKNOWN_ERROR"


class DocumentNotFound(DocumentAPIException):
    """Document not found exception"""
    def __init__(self, doc_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {doc_id} not found",
            error_code="DOCUMENT_NOT_FOUND"
        )


class UnauthorizedAccess(DocumentAPIException):
    """Unauthorized access exception"""
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            error_code="UNAUTHORIZED"
        )


class ForbiddenAccess(DocumentAPIException):
    """Forbidden access exception"""
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
            error_code="FORBIDDEN"
        )


class InvalidRequest(DocumentAPIException):
    """Invalid request exception"""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
            error_code="INVALID_REQUEST"
        )


class InvalidFileType(DocumentAPIException):
    """Invalid file type exception"""
    def __init__(self, allowed_types: list):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}",
            error_code="INVALID_FILE_TYPE"
        )


class FileSizeExceeded(DocumentAPIException):
    """File size exceeded exception"""
    def __init__(self, max_size: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {max_size} bytes",
            error_code="FILE_SIZE_EXCEEDED"
        )


class DocumentStatusError(DocumentAPIException):
    """Document status error exception"""
    def __init__(self, current_status: str, action: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot {action} document with status '{current_status}'",
            error_code="INVALID_DOCUMENT_STATUS"
        )


class DuplicateEmailError(DocumentAPIException):
    """Duplicate email exception"""
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{email}' is already registered",
            error_code="DUPLICATE_EMAIL"
        )


class DatabaseError(DocumentAPIException):
    """Database error exception"""
    def __init__(self, message: str = "Database error occurred"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
            error_code="DATABASE_ERROR"
        )
