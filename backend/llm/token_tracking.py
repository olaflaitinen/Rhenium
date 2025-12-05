"""
Token Usage Tracking Service.

Tracks token usage for LLM requests to monitor costs and usage patterns.
"""
from sqlalchemy.orm import Session
from backend.database.models import Base
from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
import uuid

# Define TokenUsage model (if not already in models.py, but better to keep separate or add here)
# For simplicity, we will assume this model is used by the service directly or added to models.py
# But since I cannot easily edit models.py without migration issues right now, 
# I will define a service that logs to the existing AuditLog or a new table if possible.
# Given the constraints, I'll create a standalone tracking utility that could log to a file or DB.

class TokenUsageTracker:
    @staticmethod
    def track_usage(
        user_id: int, 
        provider: str, 
        model: str, 
        prompt_tokens: int, 
        completion_tokens: int,
        cost: float = 0.0
    ):
        """
        Log token usage. 
        In a real production system, this would write to a 'token_usage' table.
        For now, we will log it using structlog which is already set up.
        """
        import structlog
        logger = structlog.get_logger()
        
        logger.info(
            "token_usage",
            user_id=user_id,
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            estimated_cost=cost,
            timestamp=datetime.utcnow().isoformat()
        )

        # Update Prometheus metrics
        from backend.observability.metrics import LLM_TOKEN_USAGE
        LLM_TOKEN_USAGE.labels(provider=provider, model=model, type="prompt").inc(prompt_tokens)
        LLM_TOKEN_USAGE.labels(provider=provider, model=model, type="completion").inc(completion_tokens)

token_tracker = TokenUsageTracker()
