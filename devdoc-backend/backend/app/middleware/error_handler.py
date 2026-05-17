"""
Global error handling middleware
Catches exceptions and returns standardized error responses
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import traceback
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def setup_error_handlers(app: FastAPI) -> None:
    """
    Configure global error handlers for the FastAPI application
    
    Args:
        app: FastAPI application instance
    """
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors"""
        logger.error(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "ValidationError",
                "message": "Invalid request parameters",
                "detail": exc.errors(),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle ValueError exceptions"""
        logger.error(f"Value error: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "ValueError",
                "message": str(exc),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    @app.exception_handler(FileNotFoundError)
    async def file_not_found_handler(request: Request, exc: FileNotFoundError):
        """Handle file not found errors"""
        logger.error(f"File not found: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "FileNotFoundError",
                "message": "Requested file not found",
                "detail": str(exc),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other unhandled exceptions"""
        logger.error(f"Unhandled exception: {str(exc)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "detail": str(exc) if app.debug else "Please contact support",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    print("[OK] Error handlers configured")

# Made with Bob
