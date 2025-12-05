"""
Policy Definitions for SQL Safety Engine.

This module defines the configuration models and default policies for the
SQL validation system. It allows for different "Safety Modes" (Strict, Moderate, Permissive).
"""
from enum import Enum
from typing import List, Set, Optional
from pydantic import BaseModel

class SafetyMode(str, Enum):
    STRICT = "strict"       # Read-only, whitelist tables, no joins, limited rows
    MODERATE = "moderate"   # Read-only, all tables, joins allowed, row limit
    PERMISSIVE = "permissive" # Allow write (if role permits), no limits (dangerous)

class SQLPolicy(BaseModel):
    """Configuration for SQL safety rules."""
    mode: SafetyMode
    allowed_commands: Set[str]
    max_rows: int
    allow_joins: bool
    allow_subqueries: bool
    forbidden_functions: Set[str]
    required_where_clause: bool = False

# Predefined Policies
STRICT_POLICY = SQLPolicy(
    mode=SafetyMode.STRICT,
    allowed_commands={"SELECT"},
    max_rows=100,
    allow_joins=False,
    allow_subqueries=False,
    forbidden_functions={"SLEEP", "BENCHMARK", "pg_sleep", "random"},
    required_where_clause=True
)

MODERATE_POLICY = SQLPolicy(
    mode=SafetyMode.MODERATE,
    allowed_commands={"SELECT", "WITH"},
    max_rows=1000,
    allow_joins=True,
    allow_subqueries=True,
    forbidden_functions={"SLEEP", "BENCHMARK", "pg_sleep"},
    required_where_clause=False
)

PERMISSIVE_POLICY = SQLPolicy(
    mode=SafetyMode.PERMISSIVE,
    allowed_commands={"SELECT", "INSERT", "UPDATE", "DELETE", "WITH", "CREATE", "DROP"},
    max_rows=10000,
    allow_joins=True,
    allow_subqueries=True,
    forbidden_functions=set(),
    required_where_clause=False
)

def get_policy(mode: str) -> SQLPolicy:
    """Factory to get policy by name."""
    if mode.lower() == "strict":
        return STRICT_POLICY
    elif mode.lower() == "permissive":
        return PERMISSIVE_POLICY
    else:
        return MODERATE_POLICY
