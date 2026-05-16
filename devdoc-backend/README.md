# DevDocs AI Backend

FastAPI backend for the DevDocs AI application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

### Repository Ingestion
- `POST /api/ingest/github` - Ingest GitHub repository
- `POST /api/ingest/zip` - Upload and ingest ZIP file

### Query
- `POST /api/query` - Ask questions about repository

### Documentation
- `GET /api/docs/{repo_id}` - Get generated documentation

### Health Score
- `GET /api/health/score/{repo_id}` - Get documentation health metrics

### Repository Management
- `GET /api/repositories` - List all repositories
- `GET /api/repositories/{repo_id}` - Get repository details

## Development

The backend currently uses mock data for demonstration purposes. To integrate with real AI services (IBM Watsonx), you'll need to:

1. Add IBM Watsonx API credentials to environment variables
2. Implement the AI integration in a separate module
3. Replace mock responses with real AI-generated content