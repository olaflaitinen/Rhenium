"""
Admin Schemas

Pydantic models for admin-related operations.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class UserListResponse(BaseModel):
    """Paginated user list response"""
    users: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int
    total_pages: int


class SystemStats(BaseModel):
    """System statistics"""
    total_users: int
    total_queries: int
    total_queries_today: int
    active_sessions: int
    database_size_mb: float
    cache_hit_rate: Optional[float] = None
    uptime_seconds: int


class AuditLogEntry(BaseModel):
    """Audit log entry"""
    id: int
    user_id: int
    username: str
    natural_language_query: str
    generated_sql: str
    execution_status: str
    execution_time_ms: float
    rows_returned: Optional[int] = None
    timestamp: datetime

    class Config:
        from_attributes = True


class AuditLogResponse(BaseModel):
    """Paginated audit log response"""
    logs: List[AuditLogEntry]
    total: int
    page: int
    page_size: int


class ConfigUpdate(BaseModel):
    """Update system configuration"""
    setting_name: str
    setting_value: str


class RolePermissionsUpdate(BaseModel):
    """Update role permissions"""
    role_name: str
    allowed_tables: List[str]
    allowed_operations: List[str]
