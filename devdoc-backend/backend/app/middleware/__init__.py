"""
Middleware components for FastAPI application
"""

from .cors import setup_cors
from .error_handler import setup_error_handlers

__all__ = ["setup_cors", "setup_error_handlers"]

# Made with Bob
