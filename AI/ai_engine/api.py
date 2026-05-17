"""
FastAPI REST API wrapper for the AI Engine
Exposes AI engine functionality as HTTP endpoints for backend integration
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
import os
import time
from datetime import datetime

from ai_engine.rag_cli import (
    run_pipeline,
    ask_question,
    generate_docs,
    get_health,
    load_from_db
)
from shared.utils import log

# Initialize FastAPI app
app = FastAPI(
    title="DevDoc AI Engine",
    description="AI-powered code documentation and analysis engine",
    version="1.0.0"
)

# CORS configuration for backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store job status in memory (in production, use Redis or database)
job_status = {}

# Pydantic models for request/response validation
class GitHubIngestRequest(BaseModel):
    repo_url: str
    branch: Optional[str] = "main"

class QueryRequest(BaseModel):
    question: str
    repo_id: Optional[str] = None
    max_results: Optional[int] = 5
    include_citations: Optional[bool] = True

class DocumentationRequest(BaseModel):
    repo_id: str
    doc_type: Optional[str] = "full"
    include_diagrams: Optional[bool] = True

class IngestionResponse(BaseModel):
    job_id: str
    status: str
    message: str
    ingestion_type: str
    created_at: str

class Citation(BaseModel):
    file_path: str
    line_start: int
    line_end: int
    content: str
    relevance_score: float

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    confidence: float
    processing_time: float

class HealthScoreResponse(BaseModel):
    score: float
    coverage: float
    comments: float
    issues: List[str]
    recommendations: List[str]

# Helper function to update job status
def update_job_status(job_id: str, status: str, progress: int = 0, result: Optional[dict] = None, error: Optional[str] = None):
    job_status[job_id] = {
        "job_id": job_id,
        "status": status,
        "progress": progress,
        "message": f"Job {status}",
        "result": result,
        "error": error,
        "updated_at": datetime.utcnow().isoformat()
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "DevDoc AI Engine",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "ingest_github": "/api/ingest/github",
            "ingest_zip": "/api/ingest/zip",
            "ingest_pdf": "/api/ingest/pdf",
            "query": "/api/query/",
            "documentation": "/api/documentation/generate",
            "health_score": "/api/documentation/health/{repo_id}"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ai-engine"
    }

# GitHub repository ingestion
@app.post("/api/ingest/github", response_model=IngestionResponse)
async def ingest_github(request: GitHubIngestRequest):
    try:
        job_id = str(uuid.uuid4())
        log(f"Starting GitHub ingestion: {request.repo_url}")
        
        # Update job status to processing
        update_job_status(job_id, "processing", 10)
        
        # Run the ingestion pipeline
        chunks, repo_id = run_pipeline(request.repo_url)
        
        if not chunks:
            update_job_status(job_id, "failed", 0, error="No files processed")
            raise HTTPException(status_code=400, detail="Failed to process repository")
        
        # Update job status to completed
        result = {
            "files_processed": len(chunks),
            "total_files": len(chunks),
            "repo_id": repo_id
        }
        update_job_status(job_id, "completed", 100, result=result)
        
        log(f"GitHub ingestion completed: {len(chunks)} chunks")
        
        return IngestionResponse(
            job_id=job_id,
            status="completed",
            message=f"Successfully processed {len(chunks)} code chunks",
            ingestion_type="github",
            created_at=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        log(f"GitHub ingestion failed: {e}")
        if 'job_id' in locals():
            update_job_status(job_id, "failed", 0, error=str(e))
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

# ZIP file ingestion
@app.post("/api/ingest/zip", response_model=IngestionResponse)
async def ingest_zip(file: UploadFile = File(...)):
    try:
        job_id = str(uuid.uuid4())
        log(f"Starting ZIP ingestion: {file.filename}")
        
        # Save uploaded file temporarily
        upload_dir = "workspace/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{job_id}_{file.filename}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        update_job_status(job_id, "processing", 10)
        
        # Run the ingestion pipeline
        chunks, repo_id = run_pipeline(file_path)
        
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        if not chunks:
            update_job_status(job_id, "failed", 0, error="No files processed")
            raise HTTPException(status_code=400, detail="Failed to process ZIP file")
        
        result = {
            "files_processed": len(chunks),
            "total_files": len(chunks),
            "repo_id": repo_id
        }
        update_job_status(job_id, "completed", 100, result=result)
        
        log(f"ZIP ingestion completed: {len(chunks)} chunks")
        
        return IngestionResponse(
            job_id=job_id,
            status="completed",
            message=f"Successfully processed {len(chunks)} code chunks",
            ingestion_type="zip",
            created_at=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        log(f"ZIP ingestion failed: {e}")
        if 'job_id' in locals():
            update_job_status(job_id, "failed", 0, error=str(e))
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

# PDF file ingestion
@app.post("/api/ingest/pdf", response_model=IngestionResponse)
async def ingest_pdf(file: UploadFile = File(...)):
    try:
        job_id = str(uuid.uuid4())
        log(f"Starting PDF ingestion: {file.filename}")
        
        # Save uploaded file temporarily
        upload_dir = "workspace/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{job_id}_{file.filename}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        update_job_status(job_id, "processing", 10)
        
        # Run the ingestion pipeline
        chunks, repo_id = run_pipeline(file_path)
        
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        if not chunks:
            update_job_status(job_id, "failed", 0, error="No content extracted")
            raise HTTPException(status_code=400, detail="Failed to process PDF file")
        
        result = {
            "files_processed": 1,
            "total_files": 1,
            "repo_id": repo_id
        }
        update_job_status(job_id, "completed", 100, result=result)
        
        log(f"PDF ingestion completed: {len(chunks)} chunks")
        
        return IngestionResponse(
            job_id=job_id,
            status="completed",
            message=f"Successfully processed PDF with {len(chunks)} chunks",
            ingestion_type="pdf",
            created_at=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        log(f"PDF ingestion failed: {e}")
        if 'job_id' in locals():
            update_job_status(job_id, "failed", 0, error=str(e))
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

# Check ingestion status
@app.get("/api/ingest/status/{job_id}")
async def get_ingestion_status(job_id: str):
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job_status[job_id]

# Query endpoint (RAG-based Q&A)
@app.post("/api/query/", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        start_time = time.time()
        log(f"Processing query: {request.question}")
        
        # Load chunks from database if repo_id provided
        if request.repo_id:
            chunks = load_from_db(request.repo_id)
            if not chunks:
                raise HTTPException(status_code=404, detail="Repository not found")
        else:
            raise HTTPException(status_code=400, detail="repo_id is required")
        
        # Ask question using RAG pipeline
        result = ask_question(request.question, chunks)
        
        if not result or "answer" not in result:
            raise HTTPException(status_code=500, detail="Failed to generate answer")
        
        processing_time = time.time() - start_time
        
        # Format citations
        citations = []
        for source in result.get("sources", [])[:request.max_results]:
            citations.append(Citation(
                file_path=source.get("file_path", "unknown"),
                line_start=1,
                line_end=10,
                content=source.get("content", "")[:200],
                relevance_score=source.get("score", 0.0)
            ))
        
        log(f"Query completed in {processing_time:.2f}s")
        
        return QueryResponse(
            answer=result["answer"],
            citations=citations,
            confidence=0.85,  # Could be calculated based on retrieval scores
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

# Generate documentation
@app.post("/api/documentation/generate")
async def generate_documentation(request: DocumentationRequest):
    try:
        log(f"Generating documentation for repo: {request.repo_id}")
        
        # Load chunks from database
        chunks = load_from_db(request.repo_id)
        
        if not chunks:
            raise HTTPException(status_code=404, detail="Repository not found")
        
        # Generate documentation
        docs = generate_docs(chunks)
        
        if not docs:
            raise HTTPException(status_code=500, detail="Failed to generate documentation")
        
        log("Documentation generated successfully")
        
        return {
            "repo_id": request.repo_id,
            "documentation": docs,
            "doc_type": request.doc_type,
            "generated_at": datetime.utcnow().isoformat(),
            "sections": ["overview", "architecture", "api", "usage"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log(f"Documentation generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Documentation generation failed: {str(e)}")

# Get health score
@app.get("/api/documentation/health/{repo_id}", response_model=HealthScoreResponse)
async def get_health_score(repo_id: str):
    try:
        log(f"Calculating health score for repo: {repo_id}")
        
        # Load chunks from database
        chunks = load_from_db(repo_id)
        
        if not chunks:
            raise HTTPException(status_code=404, detail="Repository not found")
        
        # Calculate health score
        health = get_health(chunks)
        
        if not health:
            raise HTTPException(status_code=500, detail="Failed to calculate health score")
        
        log(f"Health score calculated: {health.get('score', 0)}")
        
        issues_list = health.get("issues", [])
        recommendations_list = health.get("recommendations", [])
        
        return HealthScoreResponse(
            score=health.get("score", 0.0),
            coverage=health.get("coverage", 0.0),
            comments=health.get("comments", 0.0),
            issues=issues_list if isinstance(issues_list, list) else [],
            recommendations=recommendations_list if isinstance(recommendations_list, list) else []
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log(f"Health score calculation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health score calculation failed: {str(e)}")

# Get documentation by repo_id
@app.get("/api/documentation/{repo_id}")
async def get_documentation(repo_id: str):
    try:
        log(f"Retrieving documentation for repo: {repo_id}")
        
        # Load chunks from database
        chunks = load_from_db(repo_id)
        
        if not chunks:
            raise HTTPException(status_code=404, detail="Repository not found")
        
        # Generate documentation (in production, this would be cached)
        docs = generate_docs(chunks)
        
        return {
            "repo_id": repo_id,
            "documentation": docs,
            "retrieved_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log(f"Documentation retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Documentation retrieval failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

# Made with Bob
