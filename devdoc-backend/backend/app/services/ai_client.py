"""
AI Engine HTTP client
Handles communication with the AI processing engine
"""

import httpx
import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException, status

from app.config import settings

logger = logging.getLogger(__name__)


class AIClient:
    """HTTP client for communicating with AI engine"""
    
    def __init__(self):
        self.base_url = settings.ai_engine_url
        self.timeout = settings.ai_engine_timeout
        self.client = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            follow_redirects=True
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.aclose()
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to AI engine
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: JSON data to send
            files: Files to upload
            params: Query parameters
            
        Returns:
            Response JSON data
            
        Raises:
            HTTPException: If request fails
        """
        try:
            if not self.client:
                self.client = httpx.AsyncClient(
                    base_url=self.base_url,
                    timeout=self.timeout,
                    follow_redirects=True
                )
            
            response = await self.client.request(
                method=method,
                url=endpoint,
                json=data,
                files=files,
                params=params
            )
            
            response.raise_for_status()
            return response.json()
        
        except httpx.TimeoutException:
            logger.error(f"Timeout connecting to AI engine at {self.base_url}")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="AI engine request timed out"
            )
        
        except httpx.ConnectError:
            logger.error(f"Failed to connect to AI engine at {self.base_url}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI engine is unavailable"
            )
        
        except httpx.HTTPStatusError as e:
            logger.error(f"AI engine returned error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"AI engine error: {e.response.text}"
            )
        
        except Exception as e:
            logger.error(f"Unexpected error communicating with AI engine: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to communicate with AI engine: {str(e)}"
            )
    
    async def ingest_github_repo(self, repo_url: str, branch: str = "main") -> Dict[str, Any]:
        """
        Request GitHub repository ingestion
        
        Args:
            repo_url: GitHub repository URL
            branch: Branch to ingest
            
        Returns:
            Ingestion job details
        """
        return await self._make_request(
            method="POST",
            endpoint="/api/ingest/github",
            data={"repo_url": repo_url, "branch": branch}
        )
    
    async def ingest_zip_file(self, file_path: str) -> Dict[str, Any]:
        """
        Request ZIP file ingestion
        
        Args:
            file_path: Path to ZIP file
            
        Returns:
            Ingestion job details
        """
        with open(file_path, 'rb') as f:
            files = {'file': f}
            return await self._make_request(
                method="POST",
                endpoint="/api/ingest/zip",
                files=files
            )
    
    async def ingest_pdf_file(self, file_path: str) -> Dict[str, Any]:
        """
        Request PDF file ingestion
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Ingestion job details
        """
        with open(file_path, 'rb') as f:
            files = {'file': f}
            return await self._make_request(
                method="POST",
                endpoint="/api/ingest/pdf",
                files=files
            )
    
    async def get_ingestion_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get ingestion job status
        
        Args:
            job_id: Job identifier
            
        Returns:
            Job status details
        """
        return await self._make_request(
            method="GET",
            endpoint=f"/api/ingest/status/{job_id}"
        )
    
    async def query(
        self,
        question: str,
        repo_id: Optional[str] = None,
        max_results: int = 5,
        include_citations: bool = True
    ) -> Dict[str, Any]:
        """
        Send query to AI engine
        
        Args:
            question: User question
            repo_id: Repository ID to query against
            max_results: Maximum number of results
            include_citations: Include source citations
            
        Returns:
            Query response with answer and citations
        """
        return await self._make_request(
            method="POST",
            endpoint="/api/query",
            data={
                "question": question,
                "repo_id": repo_id,
                "max_results": max_results,
                "include_citations": include_citations
            }
        )
    
    async def generate_documentation(
        self,
        repo_id: str,
        doc_type: str = "full",
        include_diagrams: bool = True
    ) -> Dict[str, Any]:
        """
        Request documentation generation
        
        Args:
            repo_id: Repository ID
            doc_type: Documentation type
            include_diagrams: Include Mermaid diagrams
            
        Returns:
            Generated documentation
        """
        return await self._make_request(
            method="POST",
            endpoint="/api/documentation/generate",
            data={
                "repo_id": repo_id,
                "doc_type": doc_type,
                "include_diagrams": include_diagrams
            }
        )
    
    async def get_health_score(self, repo_id: str) -> Dict[str, Any]:
        """
        Get documentation health score
        
        Args:
            repo_id: Repository ID
            
        Returns:
            Health score metrics
        """
        return await self._make_request(
            method="GET",
            endpoint=f"/api/documentation/health/{repo_id}"
        )
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check AI engine health
        
        Returns:
            Health status
        """
        return await self._make_request(
            method="GET",
            endpoint="/health"
        )


# Global AI client instance
ai_client = AIClient()

# Made with Bob
