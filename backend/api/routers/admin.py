"""
Admin router for user management and system administration.

Admin-only endpoints for:
- User CRUD operations
- Role assignment
- System configuration
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.schemas.common import SuccessResponse, PaginationParams
from backend.auth.dependencies import get_current_admin_user
from backend.auth.models import User, UserCreate, UserResponse, UserUpdate, RoleEnum
from backend.auth.service import AuthService
from backend.auth.rbac import RBACService
from backend.database.connection import get_db

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Create a new user.
    
    Requires: ADMIN role
    """
    # Check if user already exists
    existing_user = AuthService.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    existing_user = AuthService.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )
    
    # Create user
    user = AuthService.create_user(
        db=db,
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        full_name=user_data.full_name,
        roles=user_data.roles
    )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        roles=[role.name for role in user.roles],
        created_at=user.created_at
    )


@router.get("/users", response_model=List[UserResponse])
async def list_users(
    pagination: PaginationParams = Depends(),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    List all users.
    
    Requires: ADMIN role
    """
    users = db.query(User).offset(pagination.offset).limit(pagination.page_size).all()
    
    return [
        UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            roles=[role.name for role in user.roles],
            created_at=user.created_at
        )
        for user in users
    ]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get user by ID.
    
    Requires: ADMIN role
    """
    user = AuthService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        roles=[role.name for role in user.roles],
        created_at=user.created_at
    )


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update user information.
    
    Requires: ADMIN role
    """
    user = AuthService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    if user_update.roles is not None:
        # Update roles
        user.roles.clear()
        for role_name in user_update.roles:
            from backend.auth.models import Role
            role = db.query(Role).filter(Role.name == role_name.value).first()
            if role:
                user.roles.append(role)
    
    db.commit()
    db.refresh(user)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        roles=[role.name for role in user.roles],
        created_at=user.created_at
    )


@router.delete("/users/{user_id}", response_model=SuccessResponse)
async def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete a user (soft delete by deactivating).
    
    Requires: ADMIN role
    """
    user = AuthService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Soft delete
    user.is_active = False
    db.commit()
    
    return SuccessResponse(
        success=True,
        message=f"User {user.username} deactivated successfully"
    )


@router.post("/init-roles", response_model=SuccessResponse)
async def initialize_roles(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Initialize default roles in the system.
    
    Requires: ADMIN role
    """
    RBACService.initialize_default_roles(db)
    
    return SuccessResponse(
        success=True,
        message="Default roles initialized successfully"
    )
