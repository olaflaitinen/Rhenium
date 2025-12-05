"""
Data models for authentication and authorization.

Defines User, Role, and Permission models with SQLAlchemy ORM.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field

Base = declarative_base()

# Association tables for many-to-many relationships
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)


class RoleEnum(str, Enum):
    """Predefined user roles in the system."""
    ADMIN = "ADMIN"
    DATA_SCIENTIST = "DATA_SCIENTIST"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"


class PermissionType(str, Enum):
    """Types of permissions that can be granted."""
    READ = "READ"
    WRITE = "WRITE"
    DELETE = "DELETE"
    ADMIN = "ADMIN"
    EXECUTE_QUERY = "EXECUTE_QUERY"
    APPROVE_QUERY = "APPROVE_QUERY"
    MANAGE_USERS = "MANAGE_USERS"


# SQLAlchemy ORM Models

class User(Base):
    """User account model."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    
    def has_role(self, role_name: str) -> bool:
        """Check if user has a specific role."""
        return any(role.name == role_name for role in self.roles)
    
    def has_permission(self, permission_type: PermissionType) -> bool:
        """Check if user has a specific permission through their roles."""
        for role in self.roles:
            if any(perm.permission_type == permission_type for perm in role.permissions):
                return True
        return False


class Role(Base):
    """Role model for RBAC."""
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")


class Permission(Base):
    """Permission model for fine-grained access control."""
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    permission_type = Column(String, nullable=False)  # e.g., READ, WRITE, EXECUTE_QUERY
    resource_type = Column(String)  # e.g., 'table', 'schema', 'system'
    resource_name = Column(String)  # e.g., 'sales', 'customers', '*'
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")


# Pydantic models for API requests/responses

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8)
    roles: List[RoleEnum] = Field(default=[RoleEnum.VIEWER])


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    roles: Optional[List[RoleEnum]] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    is_superuser: bool
    roles: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenData(BaseModel):
    """Data encoded in JWT token."""
    user_id: Optional[int] = None
    username: Optional[str] = None
    roles: List[str] = []
