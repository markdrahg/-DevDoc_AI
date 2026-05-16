"""
API route handlers
"""

from .ingestion import router as ingestion_router
from .query import router as query_router
from .health import router as health_router

__all__ = ["ingestion_router", "query_router", "health_router"]

# Made with Bob
