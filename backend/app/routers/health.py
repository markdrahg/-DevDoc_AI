"""
Health check endpoints
System status and monitoring
"""

from fastapi import APIRouter
import logging
import time
from datetime import datetime

from app.models import HealthCheckResponse
from app.config import settings
from app.services.ai_client import ai_client

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])

# Track server start time
START_TIME = time.time()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Check the health status of the backend API and AI engine
    
    Returns system status, version, and connectivity information
    """
    logger.info("Health check requested")
    
    # Check AI engine connectivity
    ai_engine_status = "unknown"
    try:
        await ai_client.health_check()
        ai_engine_status = "healthy"
    except Exception as e:
        logger.warning(f"AI engine health check failed: {str(e)}")
        ai_engine_status = "unavailable"
    
    uptime = time.time() - START_TIME
    
    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow(),
        ai_engine_status=ai_engine_status,
        uptime=uptime
    )


@router.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

# Made with Bob
