"""
Query endpoints
Handles Q&A queries about code
"""

from fastapi import APIRouter, HTTPException, status
import logging
import time

from app.models import (
    QueryRequest,
    QueryResponse
)
from app.services.ai_client import ai_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/query", tags=["Query"])


@router.post("/", response_model=QueryResponse)
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

# Made with Bob
