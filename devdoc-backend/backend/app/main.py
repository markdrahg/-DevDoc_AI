"""
FastAPI Application Entry Point
DevDoc AI Backend - REST API for AI-powered code documentation
"""

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.middleware import setup_cors, setup_error_handlers
from app.routers import ingestion_router, query_router, documentation_router, health_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("=" * 60)
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"AI Engine URL: {settings.ai_engine_url}")
    logger.info(f"Upload directory: {settings.upload_dir}")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="REST API for AI-powered code documentation system",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    debug=settings.debug
)

# Setup middleware
setup_cors(app)
setup_error_handlers(app)

# Add GZip compression for responses
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Register routers
app.include_router(health_router)
app.include_router(ingestion_router)
app.include_router(query_router)
app.include_router(documentation_router)

logger.info("[OK] All routers registered")
logger.info("[OK] Application initialized successfully")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

# Made with Bob
