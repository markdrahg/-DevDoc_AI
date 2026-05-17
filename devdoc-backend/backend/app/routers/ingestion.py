"""
Ingestion endpoints
Handles GitHub, ZIP, and PDF file ingestion
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Optional
import logging

from app.models import (
    GitHubIngestionRequest,
    IngestionResponse,
    IngestionStatusResponse,
    IngestionType,
    IngestionStatus
)
from app.services.file_handler import file_handler
from app.services.ai_client import ai_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ingest", tags=["Ingestion"])


@router.post("/github", response_model=IngestionResponse, status_code=status.HTTP_202_ACCEPTED)
async def ingest_github_repository(request: GitHubIngestionRequest):
    """
    Ingest a GitHub repository
    
    - **repo_url**: GitHub repository URL (e.g., https://github.com/user/repo)
    - **branch**: Branch to ingest (default: main)
    """
    logger.info(f"Ingesting GitHub repository: {request.repo_url}")
    
    try:
        # Forward request to AI engine
        response = await ai_client.ingest_github_repo(
            repo_url=str(request.repo_url),
            branch=request.branch or "main"
        )
        
        job_id = response.get("job_id")
        if not job_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI engine did not return a job ID"
            )
        
        return IngestionResponse(
            job_id=job_id,
            status=IngestionStatus.PROCESSING,
            message="GitHub repository ingestion started",
            ingestion_type=IngestionType.GITHUB
        )
    
    except Exception as e:
        logger.error(f"GitHub ingestion failed: {str(e)}")
        raise


@router.post("/zip", response_model=IngestionResponse, status_code=status.HTTP_202_ACCEPTED)
async def ingest_zip_file(file: UploadFile = File(...)):
    """
    Ingest a ZIP file containing code
    
    - **file**: ZIP file to upload
    """
    logger.info(f"Ingesting ZIP file: {file.filename}")
    
    # Validate file type
    if not file.filename or not file.filename.endswith('.zip'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only ZIP files are allowed"
        )
    
    try:
        # Save uploaded file
        file_path = await file_handler.save_upload_file(file, subfolder="zip")
        
        # Forward to AI engine
        response = await ai_client.ingest_zip_file(file_path)
        
        # Clean up uploaded file (optional - can keep for debugging)
        # file_handler.delete_file(file_path)
        
        job_id = response.get("job_id")
        if not job_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI engine did not return a job ID"
            )
        
        return IngestionResponse(
            job_id=job_id,
            status=IngestionStatus.PROCESSING,
            message="ZIP file ingestion started",
            ingestion_type=IngestionType.ZIP
        )
    
    except Exception as e:
        logger.error(f"ZIP ingestion failed: {str(e)}")
        raise


@router.post("/pdf", response_model=IngestionResponse, status_code=status.HTTP_202_ACCEPTED)
async def ingest_pdf_file(file: UploadFile = File(...)):
    """
    Ingest a PDF documentation file
    
    - **file**: PDF file to upload
    """
    logger.info(f"Ingesting PDF file: {file.filename}")
    
    # Validate file type
    if not file.filename or not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    try:
        # Save uploaded file
        file_path = await file_handler.save_upload_file(file, subfolder="pdf")
        
        # Forward to AI engine
        response = await ai_client.ingest_pdf_file(file_path)
        
        # Clean up uploaded file (optional)
        # file_handler.delete_file(file_path)
        
        job_id = response.get("job_id")
        if not job_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI engine did not return a job ID"
            )
        
        return IngestionResponse(
            job_id=job_id,
            status=IngestionStatus.PROCESSING,
            message="PDF file ingestion started",
            ingestion_type=IngestionType.PDF
        )
    
    except Exception as e:
        logger.error(f"PDF ingestion failed: {str(e)}")
        raise


@router.get("/status/{job_id}", response_model=IngestionStatusResponse)
async def get_ingestion_status(job_id: str):
    """
    Get the status of an ingestion job
    
    - **job_id**: Unique job identifier returned from ingestion endpoint
    """
    logger.info(f"Checking status for job: {job_id}")
    
    try:
        response = await ai_client.get_ingestion_status(job_id)
        
        status_value = response.get("status")
        if not status_value:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI engine did not return status"
            )
        
        return IngestionStatusResponse(
            job_id=job_id,
            status=status_value,
            progress=response.get("progress", 0),
            message=response.get("message", ""),
            files_processed=response.get("files_processed"),
            total_files=response.get("total_files"),
            error=response.get("error")
        )
    
    except Exception as e:
        logger.error(f"Failed to get ingestion status: {str(e)}")
        raise

# Made with Bob
