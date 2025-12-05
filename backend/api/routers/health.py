"""
Health check and monitoring router.

Provides endpoints for:
- Health checks (liveness/readiness probes)
- System metrics
- Status information
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.api.schemas.common import HealthResponse
from backend.database.connection import get_db
from backend.config.settings import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint for load balancers and orchestrators.
    
    Returns:
        Health status including version, environment, and service status
    """
    # Check database connectivity
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        version=settings.is_production and "1.0.0" or "1.0.0-dev",
        environment=settings.ENVIRONMENT,
        database=db_status,
        llm_provider=settings.LLM_PROVIDER
    )


@router.get("/liveness")
async def liveness():
    """
    Kubernetes liveness probe.
    
    Returns 200 if the application is running.
    """
    return {"status": "alive"}


@router.get("/readiness")
async def readiness(db: Session = Depends(get_db)):
    """
    Kubernetes readiness probe.
    
    Returns 200 if the application is ready to serve traffic.
    Checks database connectivity.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail=f"Database not ready: {str(e)}")
