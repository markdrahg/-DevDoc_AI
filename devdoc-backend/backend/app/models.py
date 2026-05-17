"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class IngestionType(str, Enum):
    """Types of ingestion sources"""
    GITHUB = "github"
    ZIP = "zip"
    PDF = "pdf"


class IngestionStatus(str, Enum):
    """Status of ingestion process"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ============= Ingestion Models =============

class GitHubIngestionRequest(BaseModel):
    """Request model for GitHub repository ingestion"""
    repo_url: HttpUrl = Field(..., description="GitHub repository URL")
    branch: Optional[str] = Field(default="main", description="Branch to ingest")
    
    class Config:
        json_schema_extra = {
            "example": {
                "repo_url": "https://github.com/username/repo",
                "branch": "main"
            }
        }


class IngestionResponse(BaseModel):
    """Response model for ingestion requests"""
    job_id: str = Field(..., description="Unique job identifier")
    status: IngestionStatus = Field(..., description="Current status")
    message: str = Field(..., description="Status message")
    ingestion_type: IngestionType = Field(..., description="Type of ingestion")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "processing",
                "message": "Repository ingestion started",
                "ingestion_type": "github",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


class IngestionStatusResponse(BaseModel):
    """Response model for checking ingestion status"""
    job_id: str
    status: IngestionStatus
    progress: int = Field(..., ge=0, le=100, description="Progress percentage")
    message: str
    files_processed: Optional[int] = None
    total_files: Optional[int] = None
    error: Optional[str] = None


# ============= Query Models =============

class QueryRequest(BaseModel):
    """Request model for Q&A queries"""
    question: str = Field(..., min_length=1, max_length=1000, description="User question")
    repo_id: Optional[str] = Field(None, description="Repository ID to query against")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum number of results")
    include_citations: bool = Field(default=True, description="Include source citations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "How does the authentication system work?",
                "repo_id": "550e8400-e29b-41d4-a716-446655440000",
                "max_results": 5,
                "include_citations": True
            }
        }


class Citation(BaseModel):
    """Source citation model"""
    file_path: str = Field(..., description="Path to source file")
    line_start: int = Field(..., description="Starting line number")
    line_end: int = Field(..., description="Ending line number")
    content: str = Field(..., description="Relevant code snippet")
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance score")


class QueryResponse(BaseModel):
    """Response model for Q&A queries"""
    answer: str = Field(..., description="Generated answer")
    citations: List[Citation] = Field(default_factory=list, description="Source citations")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "The authentication system uses JWT tokens...",
                "citations": [
                    {
                        "file_path": "src/auth/jwt.py",
                        "line_start": 15,
                        "line_end": 30,
                        "content": "def generate_token(user_id)...",
                        "relevance_score": 0.95
                    }
                ],
                "confidence": 0.92,
                "processing_time": 1.23
            }
        }


# ============= Documentation Models =============

class DocumentationRequest(BaseModel):
    """Request model for documentation generation"""
    repo_id: str = Field(..., description="Repository ID")
    doc_type: str = Field(default="full", description="Documentation type (full, api, readme)")
    include_diagrams: bool = Field(default=True, description="Include Mermaid diagrams")


class DocumentationResponse(BaseModel):
    """Response model for generated documentation"""
    repo_id: str
    documentation: str = Field(..., description="Generated documentation in Markdown")
    health_score: float = Field(..., ge=0, le=100, description="Documentation health score")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Documentation metrics")
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class HealthScore(BaseModel):
    """Documentation health score model"""
    overall_score: float = Field(..., ge=0, le=100)
    coverage: float = Field(..., ge=0, le=100, description="Documentation coverage")
    quality: float = Field(..., ge=0, le=100, description="Documentation quality")
    completeness: float = Field(..., ge=0, le=100, description="Documentation completeness")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")


# ============= Health Check Models =============

class HealthCheckResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ai_engine_status: str = Field(..., description="AI engine connectivity status")
    uptime: float = Field(..., description="Uptime in seconds")


# ============= Error Models =============

class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid request parameters",
                "detail": "Field 'repo_url' is required",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }

# Made with Bob
