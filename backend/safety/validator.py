import re
from typing import List

from backend.config.settings import settings


class SQLValidator:
    def __init__(self):
        self.allowed_tables = ["sales"]  # Whitelist of tables
        self.forbidden_keywords = [
            "DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE",
            "GRANT", "REVOKE", "COMMIT", "ROLLBACK", "SAVEPOINT"
        ]

    def validate(self, query: str) -> tuple[bool, str | None]:
        """
        Validates the SQL query.
        Returns (is_valid, error_message).
        """
        query_upper = query.upper()

        # 1. Check for forbidden keywords (Basic SQL Injection/Destructive command prevention)
        if not settings.ALLOW_DANGEROUS_QUERIES:
            for keyword in self.forbidden_keywords:
                # Use word boundary to avoid matching substrings (e.g., "UPDATE" in "UPDATED_AT")
                if re.search(r'\b' + keyword + r'\b', query_upper):
                    return False, f"Forbidden keyword detected: {keyword}"

        # 2. Check for multiple statements (semicolon separation)
        # Simple check: if there's a semicolon followed by non-whitespace, it might be multiple queries.
        # This is a basic heuristic.
        if ";" in query:
             parts = [p.strip() for p in query.split(";") if p.strip()]
             if len(parts) > 1:
                 return False, "Multiple SQL statements are not allowed."

        # 3. Table Whitelist (Optional but recommended)
        # This is harder to do perfectly with regex, but we can check if the query mentions known tables.
        # For now, we will just ensure it doesn't try to access system tables like sqlite_master if we wanted to be strict.
        # A simple check: ensure at least one allowed table is present if it's a SELECT.
        # (Skipping strict table check for this prototype to allow flexibility, but good to have in mind)

        return True, None

validator = SQLValidator()
