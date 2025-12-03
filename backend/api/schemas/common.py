"""
Common schemas shared across the API.

Includes error responses, pagination, and base models.
"""
from typing import Optional, Any, Dict, List
from datetime import datetime
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Detailed error information."""
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    field: Optional[str] = Field(None, description="Field that caused the error")


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[List[ErrorDetail]] = Field(None, description="Detailed error information")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SuccessResponse(BaseModel):
    """Generic success response."""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    @classmethod
    def create(cls, items: List[Any], total: int, pagination: PaginationParams):
        """Create a paginated response."""
        total_pages = (total + pagination.page_size - 1) // pagination.page_size
        return cls(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages
        )


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str
    environment: str
    database: str = "connected"
    llm_provider: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
