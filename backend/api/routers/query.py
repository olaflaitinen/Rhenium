"""
Query router for natural language to SQL functionality.

Handles:
- Natural language query processing
- SQL generation and validation
- Query execution
- Query history
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
from backend.safety.validator import SQLValidator
from backend.database.executor import execute_sql_query, QueryExecutionError
from backend.config.settings import settings

router = APIRouter(prefix="/api/v1/query", tags=["Query"])


@router.post("/", response_model=QueryResponse)
async def process_natural_language_query(
    request: QueryRequest,
    current_user: User = Depends(require_permission(PermissionType.EXECUTE_QUERY)),
    db: Session = Depends(get_db)
):
    """
    Process a natural language query and return SQL results.
    
    Workflow:
    1. Generate SQL from natural language using LLM
    2. Validate SQL against safety policies and user permissions
    3. Execute SQL if valid (unless dry_run=True)
    4. Return results with metrics
    5. Log to audit trail
    
    Requires: EXECUTE_QUERY permission
    """
    start_time = time.time()
    generated_sql = ""
    validation_result = None
    results = None
    error_message = None
    
    try:
        # Step 1: Generate SQL using LLM
        llm_client = get_llm_client()
        prompt = get_text_to_sql_prompt(request.question)
        generated_sql = llm_client.generate_sql(prompt)
        
        # Clean SQL (remove markdown if present)
        generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
        
        # Step 2: Validate SQL
        is_valid, error_msg = SQLValidator.validate(generated_sql)
        
        # Additional RBAC validation
        if is_valid:
            # Check if user can execute this type of query
            # For now, simple check based on role
            if not RBACService.can_execute_dangerous_query(current_user):
                # Ensure it's a SELECT query
                if not generated_sql.upper().strip().startswith("SELECT"):
                    is_valid = False
                    error_msg = "User role does not permit non-SELECT queries"
        
        validation_result = SQLValidationResult(
            is_valid=is_valid,
            error_message=error_msg if not is_valid else None,
            blocked_reason=error_msg if not is_valid else None
        )
        
        # Step 3: Execute SQL (if valid and not dry run)
        if is_valid and not request.dry_run:
            try:
                results = execute_sql_query(generated_sql)
            except QueryExecutionError as e:
                error_message = str(e)
                validation_result.is_valid = False
                validation_result.error_message = error_message
        
        # Step 4: Generate explanation if requested
        explanation = None
        if request.explain and is_valid:
            explanation = llm_client.explain_sql(generated_sql, request.question)
        
        execution_time_ms = (time.time() - start_time) * 1000
        
        # Step 5: Audit logging
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
