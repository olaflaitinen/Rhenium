"""
Global error handling middleware.

Provides consistent error responses and logging for all exceptions.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import structlog

from backend.api.schemas.common import ErrorResponse, ErrorDetail

logger = structlog.get_logger()


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions with standardized response.
    """
    request_id = getattr(request.state, "request_id", None)
    
    logger.warning(
        "http_exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
        request_id=request_id
    )
    
    error_response = ErrorResponse(
        error="HTTPException",
        message=str(exc.detail),
        request_id=request_id
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(mode='json')
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle request validation errors with detailed feedback.
    """
    request_id = getattr(request.state, "request_id", None)
    
    logger.warning(
        "validation_error",
        errors=exc.errors(),
        path=request.url.path,
        request_id=request_id
    )
    
    # Format validation errors
    details = [
        ErrorDetail(
            code="validation_error",
            message=error["msg"],
            field=".".join(str(loc) for loc in error["loc"])
        )
        for error in exc.errors()
    ]
    
    error_response = ErrorResponse(
        error="ValidationError",
        message="Request validation failed",
        details=details,
        request_id=request_id
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump(mode='json')
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions.
    """
    request_id = getattr(request.state, "request_id", None)
    
    logger.error(
        "unhandled_exception",
        exception=str(exc),
        exception_type=type(exc).__name__,
        path=request.url.path,
        request_id=request_id,
        exc_info=True
    )
    
    error_response = ErrorResponse(
        error="InternalServerError",
        message="An unexpected error occurred",
        request_id=request_id
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(mode='json')
    )
