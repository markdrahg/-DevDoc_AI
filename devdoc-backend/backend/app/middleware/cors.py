"""
CORS (Cross-Origin Resource Sharing) middleware configuration
Allows frontend to communicate with backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the FastAPI application
    
    Args:
        app: FastAPI application instance
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allow all headers
        expose_headers=["*"],  # Expose all headers to the frontend
        max_age=3600,  # Cache preflight requests for 1 hour
    )
    
    print(f"[OK] CORS configured for origins: {settings.cors_origins_list}")

# Made with Bob
