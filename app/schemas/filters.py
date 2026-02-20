from pydantic import BaseModel
from typing import Optional, List

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 10

class DocumentListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    documents: List[dict]

class DocumentFilterRequest(BaseModel):
    status: Optional[str] = None
    search: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    skip: int = 0
    limit: int = 10
