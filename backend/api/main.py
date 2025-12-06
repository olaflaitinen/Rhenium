"""
Main FastAPI application with production-grade configuration.

Includes:
- All routers (auth, query, admin, schema, health)
- Middleware (logging, error handling, CORS)
- Database initialization
- Structured logging
- API versioning
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.config.settings import settings
from backend.observability.logging_config import configure_logging
from backend.database.connection import init_db
from backend.api.middleware.logging import LoggingMiddleware
from backend.api.middleware.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from backend.api.routers import health, auth, query, admin, schema

# Configure logging
configure_logging()


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="LLM-based DBMS",
        description="Production-grade Natural Language Interface for Database Management",
        version="1.0.0",
        docs_url="/docs" if not settings.is_production else None,  # Disable in production
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url=f"/api/{settings.API_VERSION}/openapi.json"
    )
    
    # CORS Middleware (configure appropriately for production)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.is_development else [],  # Restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Custom middleware
    app.add_middleware(LoggingMiddleware)
    
    # Exception handlers
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    
    # Include routers
    api_router = FastAPI()
    app.include_router(health.router, prefix=f"/api/{settings.API_VERSION}")
    app.include_router(auth.router, prefix=f"/api/{settings.API_VERSION}")
    app.include_router(query.router, prefix=f"/api/{settings.API_VERSION}")
    app.include_router(admin.router, prefix=f"/api/{settings.API_VERSION}")
    app.include_router(schema.router, prefix=f"/api/{settings.API_VERSION}")
    
    # Metrics Endpoint
    from prometheus_client import make_asgi_app
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    # Metrics Middleware
    @app.middleware("http")
    async def metrics_middleware(request, call_next):
        import time
        from backend.observability.metrics import REQUEST_LATENCY, REQUEST_COUNT
        
        start_time = time.time()
        method = request.method
        path = request.url.path
        
        try:
            response = await call_next(request)
            status_code = response.status_code
            REQUEST_COUNT.labels(method=method, endpoint=path, status=status_code).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=path).observe(time.time() - start_time)
            return response
        except Exception as e:
            REQUEST_COUNT.labels(method=method, endpoint=path, status=500).inc()
            raise e

    return app


# Create application instance
app = create_app()


@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    
    Initializes database and performs other startup tasks.
    """
    import structlog
    logger = structlog.get_logger()
    
    logger.info(
        "application_starting",
        version="1.0.0",
        environment=settings.ENVIRONMENT,
        database_type=settings.DATABASE_TYPE,
        llm_provider=settings.LLM_PROVIDER
    )
    
    # Initialize database
    try:
        init_db()
        logger.info("database_initialized")
    except Exception as  e:
        logger.error("database_initialization_failed", error=str(e))
        raise
    
    # Initialize default roles
    try:
        from backend.auth.rbac import RBACService
        from backend.database.connection import SessionLocal
        
        db = SessionLocal()
        RBACService.initialize_default_roles(db)
        db.close()
        
        logger.info("default_roles_initialized")
    except Exception as e:
        logger.warning("default_roles_initialization_failed", error=str(e))


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler.
    """
    import structlog
    logger = structlog.get_logger()
    
    logger.info("application_shutting_down")


# For direct execution
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
