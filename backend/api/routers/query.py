"""
Query router for natural language to SQL functionality.

Handles:
- Natural language query processing
- SQL generation and validation
- Query execution
- Query history
- Caching and Observability
"""
import time
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.schemas.query import (
    QueryRequest,
    QueryResponse,
    SQLValidationResult,
    QueryHistoryResponse,
    QueryHistoryItem
)
from backend.api.schemas.common import PaginationParams, PaginatedResponse
from backend.auth.dependencies import get_current_user, require_permission
from backend.auth.models import User, PermissionType
from backend.auth.rbac import RBACService
from backend.database.connection import get_db
from backend.database.models import AuditLog
from backend.llm.client import get_llm_client
from backend.llm.prompts import get_text_to_sql_prompt
from backend.llm.cache import llm_cache
from backend.safety.validator import SQLValidator
from backend.database.executor import execute_sql_query, QueryExecutionError
from backend.config.settings import settings
from backend.observability.metrics import (
    LLM_REQUEST_COUNT, 
    SQL_QUERY_COUNT, 
    LLM_LATENCY,
    SQL_EXECUTION_TIME
)

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/", response_model=QueryResponse)
async def process_natural_language_query(
    request: QueryRequest,
    current_user: User = Depends(require_permission(PermissionType.EXECUTE_QUERY)),
    db: Session = Depends(get_db)
):
    """
    Process a natural language query and return SQL results.
    
    Workflow:
    1. Check Cache
    2. Generate SQL from natural language using LLM (if not cached)
    3. Validate SQL against safety policies and user permissions
    4. Execute SQL if valid (unless dry_run=True)
    5. Return results with metrics
    6. Log to audit trail
    """
    start_time = time.time()
    generated_sql = ""
    validation_result = None
    results = None
    error_message = None
    from_cache = False
    
    try:
        # Step 1: Check Cache
        cached_sql = llm_cache.get(request.question, settings.LLM_PROVIDER)
        if cached_sql:
            generated_sql = cached_sql
            from_cache = True
        else:
            # Step 2: Generate SQL using LLM
            llm_start = time.time()
            try:
                llm_client = get_llm_client()
                prompt = get_text_to_sql_prompt(request.question)
                generated_sql = llm_client.generate_sql(prompt, history=request.history)
                
                # Clean SQL
                generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
                
                # Cache result
                llm_cache.set(request.question, settings.LLM_PROVIDER, generated_sql)
                
                # Metrics
                LLM_REQUEST_COUNT.labels(provider=settings.LLM_PROVIDER, model="default").inc()
                LLM_LATENCY.labels(provider=settings.LLM_PROVIDER, model="default").observe(time.time() - llm_start)
                
            except Exception as e:
                LLM_REQUEST_COUNT.labels(provider=settings.LLM_PROVIDER, model="default").inc() # Count errors too?
                raise e
        
        # Step 3: Validate SQL (Advanced Validator)
        validator = SQLValidator(current_user)
        validation_result = validator.validate_and_explain(generated_sql)
        
        is_valid = validation_result.is_valid
        error_msg = validation_result.error_message
        
        # Step 4: Execute SQL (if valid and not dry run)
        if is_valid and not request.dry_run:
            sql_start = time.time()
            try:
                results = execute_sql_query(generated_sql)
                SQL_QUERY_COUNT.labels(status="success").inc()
                SQL_EXECUTION_TIME.observe(time.time() - sql_start)
            except QueryExecutionError as e:
                error_message = str(e)
                validation_result.is_valid = False
                validation_result.error_message = error_message
                SQL_QUERY_COUNT.labels(status="failed").inc()
        
        # Step 5: Generate explanation if requested
        explanation = None
        if request.explain and is_valid:
            # We don't cache explanations for now, but we could
            explanation = get_llm_client().explain_sql(generated_sql, request.question)
        
        execution_time_ms = (time.time() - start_time) * 1000
        
        # Step 6: Audit logging
        audit_entry = AuditLog(
            user_id=current_user.id,
            natural_language_query=request.question,
            generated_sql=generated_sql,
            execution_status="success" if is_valid and results is not None else "blocked" if not is_valid else "dry_run",
            execution_time_ms=execution_time_ms,
            rows_returned=len(results) if results else 0,
            error_message=error_message,
            validation_status="allowed" if is_valid else "blocked",
            validation_reason=error_msg if not is_valid else None,
            endpoint="/api/v1/query"
        )
        db.add(audit_entry)
        db.commit()
        
        return QueryResponse(
            question=request.question,
            generated_sql=generated_sql,
            validation=validation_result,
            results=results,
            row_count=len(results) if results else None,
            execution_time_ms=execution_time_ms,
            explanation=explanation,
            error=error_message
        )
        
    except Exception as e:
        # Log error
        audit_entry = AuditLog(
            user_id=current_user.id,
            natural_language_query=request.question,
            generated_sql=generated_sql or "",
            execution_status="error",
            execution_time_ms=(time.time() - start_time) * 1000,
            error_message=str(e),
            validation_status="error",
            endpoint="/api/v1/query"
        )
        db.add(audit_entry)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/history", response_model=QueryHistoryResponse)
async def get_query_history(
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get query history for the current user.
    
    Returns paginated list of past queries with their status and metrics.
    """
    # Query audit logs for this user
    query = db.query(AuditLog).filter(AuditLog.user_id == current_user.id)
    total = query.count()
    
    logs = query.order_by(AuditLog.timestamp.desc()).offset(pagination.offset).limit(pagination.page_size).all()
    
    history_items = [
        QueryHistoryItem(
            id=log.id,
            question=log.natural_language_query,
            generated_sql=log.generated_sql,
            execution_status=log.execution_status,
            execution_time_ms=log.execution_time_ms,
            rows_returned=log.rows_returned,
            timestamp=log.timestamp,
            user_id=log.user_id
        )
        for log in logs
    ]
    
    return QueryHistoryResponse(
        queries=history_items,
        total=total
    )
