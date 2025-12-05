"""
Request/Response logging middleware.

Logs all HTTP requests and responses with:
- Request ID
- User information
- Endpoint
- Status code
- Response time
"""
import time
import uuid
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import structlog

logger = structlog.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for structured logging of requests and responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log details.
        """
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Start timer
        start_time = time.time()
        
        # Extract user info if available (from auth header)
        user_info = "anonymous"
        try:
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                # Could decode JWT here for user info, but keep it simple
                user_info = "authenticated"
        except:
            pass
        
        # Log request
        logger.info(
            "http_request_start",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            query_params=str(request.query_params),
            client_host=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            user=user_info
        )
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log exception
            processing_time = time.time() - start_time
            logger.error(
                "http_request_error",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                error=str(e),
                processing_time_ms=processing_time * 1000
            )
            raise
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Log response
        logger.info(
            "http_request_complete",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            processing_time_ms=processing_time * 1000,
            user=user_info
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
