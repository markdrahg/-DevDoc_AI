"""
Configuration management using pydantic-settings
Loads environment variables from .env file
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # FastAPI Configuration
    app_name: str = "DevDoc AI Backend"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # AI Engine Configuration
    ai_engine_url: str = "http://localhost:8001"
    ai_engine_timeout: int = 300
    
    # File Upload Configuration
    max_upload_size: int = 104857600  # 100MB
    upload_dir: str = "./uploads"
    allowed_extensions: str = ".py,.js,.jsx,.ts,.tsx,.java,.cpp,.c,.h,.cs,.go,.rs,.rb,.php,.swift,.kt,.scala,.md,.txt,.json,.yaml,.yml,.xml,.html,.css,.sql"
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse allowed extensions string into list"""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    def ensure_upload_dir(self):
        """Create upload directory if it doesn't exist"""
        os.makedirs(self.upload_dir, exist_ok=True)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Ensure upload directory exists
settings.ensure_upload_dir()

# Made with Bob
