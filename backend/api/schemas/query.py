"""
Query-related schemas for the API.

Defines request/response models for natural language query endpoints.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for natural language query."""
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Natural language question",
        examples=["What is the total revenue?", "How many orders in 2023?"]
    )
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional context for query generation"
    )
    dry_run: bool = Field(
        False,
        description="If true, generate SQL but don't execute"
    )
    explain: bool = Field(
        False,
        description="If true, include explanation of generated SQL"
    )
    user_id: Optional[str] = Field(
        None,
        description="Optional user identifier for logging"
    )
    history: Optional[List[Dict[str, str]]] = Field(
        None,
        description="Conversation history for multi-turn context (e.g. [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}])"
    )


class SQLValidationResult(BaseModel):
    """SQL validation result."""
    is_valid: bool
    error_message: Optional[str] = None
    blocked_reason: Optional[str] = None
    policy_violated: Optional[str] = None


class QueryResponse(BaseModel):
    """Response model for natural language query."""
    question: str
    generated_sql: str
    validation: SQLValidationResult
    results: Optional[List[Dict[str, Any]]] = None
    row_count: Optional[int] = None
    execution_time_ms: Optional[float] = None
    explanation: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None


class QueryHistoryItem(BaseModel):
    """Query history item."""
    id: int
    question: str
    generated_sql: str
    execution_status: str
    execution_time_ms: Optional[float]
    rows_returned: Optional[int]
    timestamp: datetime
    user_id: Optional[int]


class QueryHistoryResponse(BaseModel):
    """Query history response."""
    queries: List[QueryHistoryItem]
    total: int
