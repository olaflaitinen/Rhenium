"""
Role-Based Access Control (RBAC) implementation.

Provides permission checking and policy enforcement based on user roles.
"""
from typing import List, Optional, Set
from sqlalchemy.orm import Session

from backend.auth.models import User, Role, Permission, RoleEnum, PermissionType


class AccessDeniedError(Exception):
    """Raised when a user doesn't have required permissions."""
    pass


class RBACService:
    """Service for role-based access control operations."""

    # Role hierarchy: higher level roles inherit permissions from lower levels
    ROLE_HIERARCHY = {
        RoleEnum.ADMIN: {RoleEnum.DATA_SCIENTIST, RoleEnum.ANALYST, RoleEnum.VIEWER},
        RoleEnum.DATA_SCIENTIST: {RoleEnum.ANALYST, RoleEnum.VIEWER},
        RoleEnum.ANALYST: {RoleEnum.VIEWER},
        RoleEnum.VIEWER: set()
    }

    # Default permissions for each role
    DEFAULT_ROLE_PERMISSIONS = {
        RoleEnum.VIEWER: {
            PermissionType.READ,
            PermissionType.EXECUTE_QUERY
        },
        RoleEnum.ANALYST: {
            PermissionType.READ,
            PermissionType.EXECUTE_QUERY
        },
        RoleEnum.DATA_SCIENTIST: {
            PermissionType.READ,
            PermissionType.WRITE,
            PermissionType.EXECUTE_QUERY,
            PermissionType.APPROVE_QUERY
        },
        RoleEnum.ADMIN: {
            PermissionType.READ,
            PermissionType.WRITE,
            PermissionType.DELETE,
            PermissionType.ADMIN,
            PermissionType.EXECUTE_QUERY,
            PermissionType.APPROVE_QUERY,
            PermissionType.MANAGE_USERS
        }
    }

    @staticmethod
    def get_user_permissions(user: User) -> Set[PermissionType]:
        """
        Get all permissions for a user based on their roles.
        
        Args:
            user: User object
            
        Returns:
            Set of permission types
        """
        permissions = set()
        
        for role in user.roles:
            try:
                role_enum = RoleEnum(role.name)
                # Add direct permissions for this role
                permissions.update(RBACService.DEFAULT_ROLE_PERMISSIONS.get(role_enum, set()))
                
                # Add inherited permissions from role hierarchy
                inherited_roles = RBACService.ROLE_HIERARCHY.get(role_enum, set())
                for inherited_role in inherited_roles:
                    permissions.update(RBACService.DEFAULT_ROLE_PERMISSIONS.get(inherited_role, set()))
            except ValueError:
                # Skip unknown roles
                continue
        
        return permissions

    @staticmethod
    def check_permission(
        user: User,
        required_permission: PermissionType,
        resource_type: Optional[str] = None,
        resource_name: Optional[str] = None
    ) -> bool:
        """
        Check if a user has a specific permission.
        
        Args:
            user: User object
            required_permission: Permission to check
            resource_type: Optional resource type (e.g., 'table')
            resource_name: Optional resource name (e.g., 'sales')
            
        Returns:
            True if user has permission, False otherwise
        """
        if not user.is_active:
            return False
        
        # Superusers have all permissions
        if user.is_superuser:
            return True
        
        user_permissions = RBACService.get_user_permissions(user)
        
        # Check if user has the required permission
        if required_permission not in user_permissions:
            return False
        
        # If resource-specific check is needed, verify access to that resource
        if resource_type and resource_name:
            return RBACService.check_resource_access(
                user, resource_type, resource_name
            )
        
        return True

    @staticmethod
    def require_permission(
        user: User,
        required_permission: PermissionType,
        resource_type: Optional[str] = None,
        resource_name: Optional[str] = None
    ) -> None:
        """
        Require that a user has a specific permission, raise exception if not.
        
        Args:
            user: User object
            required_permission: Permission to check
            resource_type: Optional resource type
            resource_name: Optional resource name
            
        Raises:
            AccessDeniedError: If user lacks the required permission
        """
        if not RBACService.check_permission(
            user, required_permission, resource_type, resource_name
        ):
            raise AccessDeniedError(
                f"User {user.username} lacks permission: {required_permission}"
            )

    @staticmethod
    def check_resource_access(
        user: User,
        resource_type: str,
        resource_name: str
    ) -> bool:
        """
        Check if a user has access to a specific resource.
        
        This method can be extended to implement fine-grained access control
        based on table/column level permissions.
        
        Args:
            user: User object
            resource_type: Type of resource (e.g., 'table', 'schema')
            resource_name: Name of the resource
            
        Returns:
            True if user has access, False otherwise
        """
        # For now, implement basic logic
        # In production, this would check against a permission table
        
        # Admins and data scientists have access to all resources
        if user.has_role(RoleEnum.ADMIN.value) or user.has_role(RoleEnum.DATA_SCIENTIST.value):
            return True
        
        # Analysts and viewers have read access to common tables
        if resource_type == "table":
            # Define accessible tables for each role
            analyst_tables = {"sales", "customers", "products", "orders"}
            viewer_tables = {"sales"}
            
            if user.has_role(RoleEnum.ANALYST.value):
                return resource_name.lower() in analyst_tables
            elif user.has_role(RoleEnum.VIEWER.value):
                return resource_name.lower() in viewer_tables
        
        return False

    @staticmethod
    def get_accessible_tables(user: User) -> List[str]:
        """
        Get list of tables a user can access.
        
        Args:
            user: User object
            
        Returns:
            List of table names
        """
        if user.has_role(RoleEnum.ADMIN.value) or user.has_role(RoleEnum.DATA_SCIENTIST.value):
            return ["*"]  # All tables
        elif user.has_role(RoleEnum.ANALYST.value):
            return ["sales", "customers", "products", "orders"]
        elif user.has_role(RoleEnum.VIEWER.value):
            return ["sales"]
        
        return []

    @staticmethod
    def get_accessible_columns(user: User, table_name: str) -> List[str]:
        """
        Get list of columns a user can access in a specific table.
        
        Args:
            user: User object
            table_name: Name of the table
            
        Returns:
            List of column names or ["*"] for all
        """
        if user.has_role(RoleEnum.ADMIN.value) or user.has_role(RoleEnum.DATA_SCIENTIST.value):
            return ["*"]
            
        table_name = table_name.lower()
        
        if user.has_role(RoleEnum.ANALYST.value):
            # Analysts can see almost everything except PII
            if table_name == "customers":
                return ["id", "name", "email", "phone", "address", "created_at"] # Exclude SSN, Credit Card
            return ["*"]
            
        elif user.has_role(RoleEnum.VIEWER.value):
            # Viewers have limited view
            if table_name == "customers":
                return ["id", "name", "email"]
            if table_name == "sales":
                return ["id", "amount", "date", "product_id"] # Exclude profit margin etc.
                
        return ["*"] # Default to all if table access is granted (table check happens first)

    @staticmethod
    def can_execute_dangerous_query(user: User) -> bool:
        """
        Check if user can execute potentially dangerous queries (UPDATE, DELETE, etc.).
        
        Args:
            user: User object
            
        Returns:
            True if allowed, False otherwise
        """
        return (
            user.is_superuser or
            user.has_role(RoleEnum.ADMIN.value) or
            user.has_role(RoleEnum.DATA_SCIENTIST.value)
        )

    @staticmethod
    def initialize_default_roles(db: Session) -> None:
        """
        Initialize default roles in the database.
        
        Args:
            db: Database session
        """
        default_roles = [
            {
                "name": RoleEnum.ADMIN.value,
                "description": "Full system access with user management"
            },
            {
                "name": RoleEnum.DATA_SCIENTIST.value,
                "description": "Advanced query capabilities including write operations"
            },
            {
                "name": RoleEnum.ANALYST.value,
                "description": "Read and query access to analytical tables"
            },
            {
                "name": RoleEnum.VIEWER.value,
                "description": "Read-only access to basic tables"
            }
        ]
        
        for role_data in default_roles:
            existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
            if not existing_role:
                role = Role(**role_data)
                db.add(role)
        
        db.commit()
