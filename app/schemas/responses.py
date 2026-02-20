from pydantic import BaseModel
from typing import Optional, Any


class ErrorResponse(BaseModel):
    """Structured error response format"""
    success: bool = False
    error_code: str
    message: str
    details: Optional[Any] = None
    timestamp: Optional[str] = None


class SuccessResponse(BaseModel):
    """Structured success response format"""
    success: bool = True
    message: str
    data: Optional[Any] = None
    timestamp: Optional[str] = None
