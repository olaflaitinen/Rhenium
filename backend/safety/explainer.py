"""
Explainability Engine for Safety Decisions.

This module generates human-readable explanations for why a query was allowed
or blocked by the safety engine. It helps build trust and understanding.
"""
from typing import List, Optional
from backend.safety.policies import SQLPolicy

class SafetyExplainer:
    """Generates explanations for safety validation results."""

    @staticmethod
    def explain_rejection(reason: str, policy: SQLPolicy) -> str:
        """
        Generate a user-friendly explanation for a rejection.
        """
        if "forbidden command" in reason.lower():
            return (
                f"The query attempted to use a command that is not allowed in "
                f"'{policy.mode.value}' mode. Only {', '.join(policy.allowed_commands)} "
                f"operations are permitted to ensure data safety."
            )
        
        if "table access denied" in reason.lower():
            return (
                "You do not have permission to access one or more tables referenced "
                "in this query. Please check your user role and permissions."
            )

        if "multiple statements" in reason.lower():
            return (
                "For security reasons, executing multiple SQL statements in a single "
                "request is blocked to prevent SQL injection attacks."
            )
            
        if "row limit" in reason.lower():
            return (
                f"The query would return too many rows. The current safety policy "
                f"limits results to {policy.max_rows} rows to prevent system overload."
            )

        return f"The query was blocked by the safety engine: {reason}"

    @staticmethod
    def explain_modifications(original_sql: str, modified_sql: str) -> str:
        """
        Explain how and why the SQL was modified (e.g., adding LIMIT).
        """
        explanations = []
        
        if "LIMIT" not in original_sql.upper() and "LIMIT" in modified_sql.upper():
            explanations.append(
                "Added a LIMIT clause to prevent fetching excessive data."
            )
            
        if not explanations:
            return "The query was optimized for execution."
            
        return " ".join(explanations)
