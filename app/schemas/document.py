from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentBase(BaseModel):
    filename: str
    status: str = "pending"


class DocumentCreate(BaseModel):
    pass


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    status: str
    uploaded_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentDetailResponse(DocumentResponse):
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    approval_comment: Optional[str] = None


class DocumentApprovalRequest(BaseModel):
    comment: Optional[str] = None


class DocumentAdminView(BaseModel):
    """Admin view with full document information"""
    id: int
    filename: str
    file_path: str
    status: str
    uploaded_by: int
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    approval_comment: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
