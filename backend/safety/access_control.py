"""
Access Control Module for Table and Column Level Permissions.

This module implements fine-grained access control logic, allowing the system
to restrict access not just to tables, but to specific columns based on user roles.
"""
from typing import Dict, List, Set, Optional
from backend.auth.models import RoleEnum, PermissionType

# Define sensitive columns that require higher privileges
SENSITIVE_COLUMNS = {
    "users": {"hashed_password", "email", "is_superuser"},
    "salaries": {"amount", "bonus"},  # Hypothetical table
    "customers": {"credit_limit", "phone"}
}

# Define column-level restrictions per role
# If a role is not listed, they have access to all non-sensitive columns
# If a table is not listed, standard table-level RBAC applies
COLUMN_ACCESS_POLICIES = {
    RoleEnum.VIEWER: {
        "customers": {"customername", "city", "country"},  # Whitelist: only these columns
        "sales": {"*"}  # Access to all columns in sales
    },
    RoleEnum.ANALYST: {
        "customers": {"*"}, # Access to all columns
        "sales": {"*"}
    }
}

class AccessControlService:
    """Service to enforce fine-grained access control policies."""

    @staticmethod
    def get_allowed_columns(role: RoleEnum, table: str) -> Set[str]:
        """
        Get the set of allowed columns for a given role and table.
        Returns {'*'} if all columns are allowed.
        """
        # Admin has access to everything
        if role == RoleEnum.ADMIN:
            return {"*"}

        # Check specific policies
        if role in COLUMN_ACCESS_POLICIES:
            role_policy = COLUMN_ACCESS_POLICIES[role]
            if table in role_policy:
                return role_policy[table]
        
        # Default: If no specific column policy, allow all (subject to sensitive filter)
        return {"*"}

    @staticmethod
    def is_column_access_allowed(role: RoleEnum, table: str, column: str) -> bool:
        """Check if a specific column can be accessed by the role."""
        if role == RoleEnum.ADMIN:
            return True

        # Check sensitive columns first
        if table in SENSITIVE_COLUMNS and column in SENSITIVE_COLUMNS[table]:
            # Only ADMIN (already handled) or specific roles might access sensitive data
            # For now, block everyone else
            return False

        allowed = AccessControlService.get_allowed_columns(role, table)
        if "*" in allowed:
            return True
        
        return column.lower() in {c.lower() for c in allowed}

    @staticmethod
    def filter_query_columns(role: RoleEnum, table: str, requested_columns: List[str]) -> List[str]:
        """
        Filter a list of requested columns, returning only those allowed.
        """
        return [
            col for col in requested_columns 
            if AccessControlService.is_column_access_allowed(role, table, col)
        ]
