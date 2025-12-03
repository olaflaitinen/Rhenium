"""
Request Tracing Module.

Provides utilities for tracing requests across the system.
"""
import uuid
from contextvars import ContextVar
from typing import Optional

# Context variable to store request ID
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="unknown")

def get_request_id() -> str:
    """Get the current request ID."""
    return request_id_ctx.get()

def set_request_id(request_id: Optional[str] = None) -> str:
    """Set a new request ID."""
    if not request_id:
        request_id = str(uuid.uuid4())
    request_id_ctx.set(request_id)
    return request_id
