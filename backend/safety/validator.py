import sqlparse
from sqlparse.sql import Statement, Token
from sqlparse.tokens import Keyword

from backend.config.settings import settings
from backend.auth.models import User
from backend.auth.rbac import RBACService
from backend.safety.policies import get_policy, SQLPolicy
from backend.safety.access_control import AccessControlService
from backend.safety.explainer import SafetyExplainer
from backend.api.schemas.query import SQLValidationResult

class SQLValidator:
    """
    Advanced SQL Validator using sqlparse and policy-based rules.
    Enforces RBAC, safety modes, and prevents dangerous operations.
    """

    def __init__(self, user: User):
        self.user = user
        self.policy: SQLPolicy = get_policy(settings.SAFETY_MODE)
        self.rbac = RBACService()

    def validate_and_explain(self, sql: str) -> SQLValidationResult:
        """
        Validate SQL and return detailed result with explanation.
        """
        is_valid, reason = self.validate(sql)
        
        if not is_valid:
            explanation = SafetyExplainer.explain_rejection(reason, self.policy)
            return SQLValidationResult(
                is_valid=False,
                sql=sql,
                error_message=reason,
                safety_explanation=explanation
            )
        
        # If valid, check if we modified it (e.g. enforced LIMIT)
        # For now, we just return the original valid SQL
        return SQLValidationResult(
            is_valid=True,
            sql=sql,
            safety_explanation="Query passed all safety checks."
        )

    def validate(self, sql: str) -> tuple[bool, str]:
        """
        Validates a SQL query against safety rules and user permissions.
        Returns: (is_valid, error_message)
        """
        if not sql or not sql.strip():
            return False, "Empty SQL query."

        # Parse SQL
        try:
            parsed = sqlparse.parse(sql)
        except Exception as e:
            return False, f"SQL parsing error: {str(e)}"

        # 1. Check for multiple statements
        if len(parsed) > 1:
            # Some parsers might split semicolon ending as a second empty statement
            # Check if the second statement is meaningful
            if any(token.ttype is not sqlparse.tokens.Whitespace for token in parsed[1].flatten()):
                 return False, "Multiple SQL statements are not allowed (semicolon injection prevention)."

        stmt = parsed[0]
        
        # 2. Check Command Type (DML/DDL)
        command_type = stmt.get_type().upper()
        if command_type not in self.policy.allowed_commands:
            return False, f"Forbidden command '{command_type}'. Allowed: {self.policy.allowed_commands}"

        # 3. Extract Tables and Check Permissions
        tables = self._extract_tables(stmt)
        if not tables and command_type == "SELECT":
             # Simple SELECT 1 or SELECT version() might have no tables, which is usually fine
             pass
        
        accessible_tables = self.rbac.get_accessible_tables(self.user)
        # If user is admin, accessible_tables might be {"*"} or handled separately
        
        if "*" not in accessible_tables:
            for table in tables:
                if table.lower() not in accessible_tables:
                    return False, f"Access denied for table '{table}'."

        # 4. Check Column Permissions (Basic Implementation)
        for table in tables:
            allowed_columns = self.rbac.get_accessible_columns(self.user, table)
            if "*" in allowed_columns:
                continue
                
            if self._is_select_star(stmt):
                 return False, f"SELECT * is not allowed for table '{table}' due to column restrictions. Please select specific columns."

        return True, ""

    def _is_select_star(self, stmt: Statement) -> bool:
        for token in stmt.tokens:
            if token.ttype is sqlparse.tokens.Wildcard:
                return True
        return False

    def _extract_tables(self, stmt: Statement) -> set[str]:
        """
        Extract table names from a parsed SQL statement.
        """
        tables = set()
        
        # Robust extraction using sqlparse
        idx = 0
        tokens = stmt.tokens
        while idx < len(tokens):
            token = tokens[idx]
            
            if token.ttype is Keyword and token.value.upper() in ['FROM', 'JOIN']:
                # Next token (skipping whitespace) should be the table
                idx += 1
                while idx < len(tokens) and tokens[idx].is_whitespace:
                    idx += 1
                
                if idx < len(tokens):
                    target = tokens[idx]
                    if isinstance(target, sqlparse.sql.IdentifierList):
                        for id_ in target.get_identifiers():
                            tables.add(id_.get_real_name())
                    elif isinstance(target, sqlparse.sql.Identifier):
                        tables.add(target.get_real_name())
            
            idx += 1
            
        return tables
