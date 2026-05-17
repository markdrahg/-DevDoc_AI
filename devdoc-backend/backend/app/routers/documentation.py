"""
Documentation endpoints
Handles documentation generation and health scoring
"""

from fastapi import APIRouter, HTTPException, status
import logging

from app.models import (
    DocumentationRequest,
    DocumentationResponse,
    HealthScore
)
from app.services.ai_client import ai_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documentation", tags=["Documentation"])


@router.post("/generate", response_model=DocumentationResponse)
async def generate_documentation(request: DocumentationRequest):
    """
    Generate documentation for a repository
    
    - **repo_id**: Repository ID
    - **doc_type**: Type of documentation (full, api, readme)
    - **include_diagrams**: Include Mermaid diagrams
    """
    logger.info(f"Generating documentation for repo: {request.repo_id}")
    
    try:
        response = await ai_client.generate_documentation(
            repo_id=request.repo_id,
            doc_type=request.doc_type,
            include_diagrams=request.include_diagrams
        )
        
        return DocumentationResponse(
            repo_id=request.repo_id,
            documentation=response.get("documentation", ""),
            health_score=response.get("health_score", 0.0),
            metrics=response.get("metrics", {}),
        )
    
    except Exception as e:
        logger.error(f"Documentation generation failed: {str(e)}")
        raise


@router.get("/health/{repo_id}", response_model=HealthScore)
async def get_documentation_health(repo_id: str):
    """
    Get documentation health score for a repository
    
    - **repo_id**: Repository ID
    
    Returns metrics including:
    - Overall score (0-100)
    - Coverage percentage
    - Quality score
    - Completeness score
    - Improvement suggestions
    """
    logger.info(f"Getting health score for repo: {repo_id}")
    
    try:
        response = await ai_client.get_health_score(repo_id)
        
        return HealthScore(
            overall_score=response.get("overall_score", 0.0),
            coverage=response.get("coverage", 0.0),
            quality=response.get("quality", 0.0),
            completeness=response.get("completeness", 0.0),
            suggestions=response.get("suggestions", [])
        )
    
    except Exception as e:
        logger.error(f"Failed to get health score: {str(e)}")
        raise


@router.get("/{repo_id}", response_model=DocumentationResponse)
async def get_documentation(repo_id: str):
    """
    Get existing documentation for a repository
    
    - **repo_id**: Repository ID
    """
    logger.info(f"Retrieving documentation for repo: {repo_id}")
    
    try:
        # This would typically fetch from a database or cache
        # For now, we'll call the AI engine
        response = await ai_client.generate_documentation(
            repo_id=repo_id,
            doc_type="full",
            include_diagrams=True
        )
        
        return DocumentationResponse(
            repo_id=repo_id,
            documentation=response.get("documentation", ""),
            health_score=response.get("health_score", 0.0),
            metrics=response.get("metrics", {}),
        )
    
    except Exception as e:
        logger.error(f"Failed to retrieve documentation: {str(e)}")
        raise

# Made with Bob
