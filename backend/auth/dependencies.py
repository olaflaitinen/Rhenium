"""
FastAPI dependencies for authentication and authorization.

Provides dependency functions for:
- Getting the current user from JWT token
- Requiring specific permissions
- Database session management
"""
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.auth.models import User, PermissionType
from backend.auth.service import AuthService, AuthenticationError
from backend.auth.rbac import RBACService, AccessDeniedError
from backend.database.connection import get_db

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer token
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    
    try:
        token_data = AuthService.decode_access_token(token)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = AuthService.get_user_by_id(db, token_data.user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure user is active.
    
    Args:
        current_user: Current user from get_current_user
        
    Returns:
        User object
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to require admin role.
    
    Args:
        current_user: Current user from get_current_user
        
    Returns:
        User object if admin
        
    Raises:
        HTTPException: If user is not an admin
    """
    try:
        RBACService.require_permission(current_user, PermissionType.ADMIN)
    except AccessDeniedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user


def require_permission(required_permission: PermissionType):
    """
    Dependency factory to require a specific permission.
    
    Usage:
        @router.get("/endpoint")
        async def endpoint(
            user: User = Depends(require_permission(PermissionType.EXECUTE_QUERY))
        ):
            ...
    
    Args:
        required_permission: Permission type required
        
    Returns:
        Dependency function
    """
    async def permission_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        try:
            RBACService.require_permission(current_user, required_permission)
        except AccessDeniedError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        return current_user
    
    return permission_checker


# Optional: Allow unauthenticated access (for development/testing)
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to optionally get the current user.
    Returns None if no token provided.
    
    Args:
        credentials: Optional HTTP Bearer token
        db: Database session
        
    Returns:
        User object or None
    """
    if credentials is None:
        return None
    
    try:
        token_data = AuthService.decode_access_token(credentials.credentials)
        user = AuthService.get_user_by_id(db, token_data.user_id)
        return user if user and user.is_active else None
    except AuthenticationError:
        return None
