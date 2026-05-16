"""
Query endpoints
Handles Q&A queries and documentation generation
"""

from fastapi import APIRouter, HTTPException, status
import logging
import time

from app.models import (
    QueryRequest,
    QueryResponse,
    DocumentationRequest,
    DocumentationResponse,
    HealthScore
)
from app.services.ai_client import ai_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Query"])


@router.post("/query", response_model=QueryResponse)
async def query_codebase(request: QueryRequest):
    """
    Ask questions about the codebase
    
    - **question**: Your question about the code
    - **repo_id**: Repository ID to query (optional)
    - **max_results**: Maximum number of results to return
    - **include_citations**: Include source code citations
    """
    logger.info(f"Processing query: {request.question[:100]}...")
    
    start_time = time.time()
    
    try:
        # Forward query to AI engine
        response = await ai_client.query(
            question=request.question,
            repo_id=request.repo_id,
            max_results=request.max_results,
            include_citations=request.include_citations
        )
        
        processing_time = time.time() - start_time
        
        return QueryResponse(
            answer=response.get("answer", ""),
            citations=response.get("citations", []),
            confidence=response.get("confidence", 0.0),
            processing_time=processing_time
        )
    
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise


@router.post("/documentation/generate", response_model=DocumentationResponse)
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


@router.get("/documentation/health/{repo_id}", response_model=HealthScore)
async def get_documentation_health(repo_id: str):
    """
    Get documentation health score for a repository
    
    - **repo_id**: Repository ID
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

# Made with Bob
