"""
Enhanced SQL validator using sqlparse for AST-based analysis.

Provides:
- SQL parsing and validation
- Dangerous operation detection
- Table/column access control
- Policy-based validation
"""
import re
from typing import List, Tuple, Set, Optional
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where, Comparison, Token
from sqlparse.tokens import Keyword, DML

from backend.auth.models import User
from backend.auth.rbac import RBACService
from backend.config.settings import settings


class SecurityError(Exception):
    """Exception raised when a query violates safety rules."""
    pass


class SQLValidationResult:
    """Result of SQL validation."""
    def __init__(
        self,
        is_valid: bool,
        error_message: Optional[str] = None,
        blocked_reason: Optional[str] = None,
        policy_violated: Optional[str] = None,
        tables_accessed: Optional[Set[str]] = None
    ):
        self.is_valid = is_valid
        self.error_message = error_message
        self.blocked_reason = blocked_reason
        self.policy_violated = policy_violated
        self.tables_accessed = tables_accessed or set()


class SQLValidator:
    """
    Enhanced SQL validator with parser-based analysis.
    """
    
    # Block list of dangerous SQL keywords
    FORBIDDEN_KEYWORDS = {
        "DROP", "DELETE", "TRUNCATE", "ALTER", "UPDATE", "INSERT",
        "GRANT", "REVOKE", "COMMIT", "ROLLBACK", "REPLACE", "MERGE"
    }
    
    # Allowed tables (can be configured via settings or database)
    ALLOWED_TABLES = {"sales", "customers", "products", "orders"}
    
    @classmethod
    def validate(
        cls,
        query: str,
        user: Optional[User] = None,
        strict_mode: bool = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate a SQL query against safety rules.
        
        Args:
            query: SQL query to validate
            user: Optional user for RBAC checks
            strict_mode: Override safety mode from settings
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if strict_mode is None:
            strict_mode = settings.SAFETY_MODE == "strict"
        
        query_upper = query.upper()
        query = query.strip()
        
        # 1. Check for forbidden keywords (quick check)
        for keyword in cls.FORBIDDEN_KEYWORDS:
            if re.search(r'\b' + keyword + r'\b', query_upper):
                # Allow if permissive mode and user has permission
                if not strict_mode and user and RBACService.can_execute_dangerous_query(user):
                    continue
                return False, f"Query contains forbidden keyword: {keyword}"
        
        # 2. Check for multiple statements (SQL injection prevention)
        stripped_query = query.rstrip(';')
        if ';' in stripped_query:
            return False, "Multiple statements are not allowed"
        
        # 3. Parse SQL using sqlparse
        try:
            parsed = sqlparse.parse(query)
            if not parsed:
                return False, "Could not parse SQL query"
            
            statement = parsed[0]
            
            # 4. Check statement type
            stmt_type = statement.get_type()
            if stmt_type not in ('SELECT', 'UNKNOWN'):  # UNKNOWN for WITH clauses
                # Check if it's a CTE (WITH ... SELECT)
                if not query_upper.strip().startswith("WITH"):
                    return False, f"Only SELECT queries are allowed (got {stmt_type})"
            
            # 5. Extract tables and check access
            tables = cls._extract_tables(statement)
            
            if user:
                # Check RBAC table access
                accessible_tables = RBACService.get_accessible_tables(user)
                if "*" not in accessible_tables:  # Not admin
                    for table in tables:
                        if table.lower() not in [t.lower() for t in accessible_tables]:
                            return False, f"User does not have access to table: {table}"
            
        except Exception as e:
            return False, f"SQL parsing error: {str(e)}"
        
        return True, None
    
    @classmethod
    def validate_with_details(
        cls,
        query: str,
        user: Optional[User] = None
    ) -> SQLValidationResult:
        """
        Validate with detailed result including tables accessed.
        
        Args:
            query: SQL query to validate
            user: Optional user for RBAC checks
            
        Returns:
            SQLValidationResult with detailed information
        """
        is_valid, error_msg = cls.validate(query, user)
        
        tables_accessed = set()
        if is_valid:
            try:
                parsed = sqlparse.parse(query)
                if parsed:
                    tables_accessed = cls._extract_tables(parsed[0])
            except:
                pass
        
        return SQLValidationResult(
            is_valid=is_valid,
            error_message=error_msg,
            blocked_reason=error_msg if not is_valid else None,
            tables_accessed=tables_accessed
        )
    
    @classmethod
    def validate_or_raise(cls, query: str, user: Optional[User] = None):
        """
        Validate a query and raise SecurityError if invalid.
        
        Args:
            query: SQL query to validate
            user: Optional user for RBAC checks
            
        Raises:
            SecurityError: If query is invalid
        """
        is_valid, error = cls.validate(query, user)
        if not is_valid:
            raise SecurityError(f"Security violation: {error}")
    
    @classmethod
    def _extract_tables(cls, statement) -> Set[str]:
        """
        Extract table names from a parsed SQL statement.
        
        Args:
            statement: sqlparse Statement object
            
        Returns:
            Set of table names
        """
        tables = set()
        
        from_seen = False
        for token in statement.tokens:
            if from_seen:
                if isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        tables.add(cls._get_table_name(identifier))
                elif isinstance(token, Identifier):
                    tables.add(cls._get_table_name(token))
                from_seen = False
            elif token.ttype is Keyword and token.value.upper() == 'FROM':
                from_seen = True
            elif isinstance(token, Identifier) and 'JOIN' in str(token).upper():
                # Handle JOIN clauses
                table_name = cls._get_table_name(token)
                if table_name:
                    tables.add(table_name)
        
        return tables
    
    @classmethod
    def _get_table_name(cls, token) -> str:
        """
        Extract table name from a token.
        
        Args:
            token: sqlparse token
            
        Returns:
            Table name
        """
        if isinstance(token, Identifier):
            return token.get_real_name()
        return str(token).strip()
