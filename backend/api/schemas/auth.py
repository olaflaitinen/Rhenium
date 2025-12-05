"""
Authentication and Authorization Schemas

Pydantic models for auth-related requests and responses.
"""

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Decoded token data"""
    username: Optional[str] = None
    user_id: Optional[int] = None
    roles: List[str] = []


class LoginRequest(BaseModel):
    """Login credentials"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    """User information response"""
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    roles: List[str]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # For SQLAlchemy models


class UserCreate(BaseModel):
    """Create new user request"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, max_length=100)
    roles: List[str] = Field(default_factory=lambda: ["VIEWER"])


class UserUpdate(BaseModel):
    """Update user request"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    roles: Optional[List[str]] = None


class PasswordChange(BaseModel):
    """Change password request"""
    current_password: str
    new_password: str = Field(..., min_length=8)
