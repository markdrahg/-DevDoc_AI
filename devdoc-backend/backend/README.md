# DevDoc AI Backend

FastAPI REST API for AI-powered code documentation system.

## Overview

This backend service provides a RESTful API interface for the DevDoc AI system. It handles file uploads, repository ingestion, and proxies requests to the AI processing engine. Built with FastAPI for high performance and automatic API documentation.

## Architecture

The backend follows a layered architecture:

- **Routers**: API endpoint definitions and request handling
- **Services**: Business logic and external service communication
- **Middleware**: Cross-cutting concerns (CORS, error handling)
- **Models**: Pydantic models for request/response validation

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic request/response models
│   ├── routers/
│   │   ├── ingestion.py     # File and repository ingestion endpoints
│   │   ├── query.py         # Q&A and documentation endpoints
│   │   └── health.py        # Health check endpoints
│   ├── services/
│   │   ├── file_handler.py  # File upload handling and validation
│   │   └── ai_client.py     # AI engine HTTP client
│   └── middleware/
│       ├── cors.py          # CORS configuration
│       └── error_handler.py # Global error handling
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

Edit the `.env` file to configure the application:

```env
# FastAPI Configuration
APP_NAME=DevDoc AI Backend
APP_VERSION=1.0.0
DEBUG=True
HOST=0.0.0.0
PORT=8000

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# AI Engine Configuration
AI_ENGINE_URL=http://localhost:8001
AI_ENGINE_TIMEOUT=300

# File Upload Configuration
MAX_UPLOAD_SIZE=104857600  # 100MB in bytes
UPLOAD_DIR=./uploads
ALLOWED_EXTENSIONS=.py,.js,.jsx,.ts,.tsx,.java,.cpp,.c,.h,.cs,.go,.rs,.rb,.php,.swift,.kt,.scala,.md,.txt,.json,.yaml,.yml,.xml,.html,.css,.sql

# Logging
LOG_LEVEL=INFO
```

## Running the Server

### Development Mode (with auto-reload)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Python directly

```bash
python -m app.main
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Ingestion Endpoints

#### Ingest GitHub Repository

```
POST /api/ingest/github
Content-Type: application/json

{
  "repo_url": "https://github.com/username/repo",
  "branch": "main"
}
```

#### Upload ZIP File

```
POST /api/ingest/zip
Content-Type: multipart/form-data

file: <zip file>
```

#### Upload PDF File

```
POST /api/ingest/pdf
Content-Type: multipart/form-data

file: <pdf file>
```

#### Check Ingestion Status

```
GET /api/ingest/status/{job_id}
```

### Query Endpoints

#### Ask Question

```
POST /api/query
Content-Type: application/json

{
  "question": "How does the authentication work?",
  "repo_id": "optional-repo-id",
  "max_results": 5,
  "include_citations": true
}
```

#### Generate Documentation

```
POST /api/documentation/generate
Content-Type: application/json

{
  "repo_id": "repo-id",
  "doc_type": "full",
  "include_diagrams": true
}
```

#### Get Documentation Health Score

```
GET /api/documentation/health/{repo_id}
```

### Health Endpoints

#### System Health Check

```
GET /health
```

#### API Information

```
GET /
```

## Response Format

### Success Response

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "Request processed successfully",
  "data": {}
}
```

### Error Response

```json
{
  "error": "ValidationError",
  "message": "Invalid request parameters",
  "detail": "Field 'repo_url' is required",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Development

### Code Style

The project follows PEP 8 style guidelines. Use the following tools for code quality:

```bash
# Format code
black app/

# Type checking
mypy app/

# Linting
flake8 app/
```

### Testing

Run tests using pytest:

```bash
pytest
```

## Integration

### Frontend Integration

The backend is configured with CORS to allow requests from the frontend application. Update `CORS_ORIGINS` in `.env` to include your frontend URL.

### AI Engine Integration

The backend communicates with the AI processing engine via HTTP. Configure `AI_ENGINE_URL` in `.env` to point to your AI engine service.

## Error Handling

The application includes global error handling for:

- Validation errors (422)
- File not found errors (404)
- Value errors (400)
- Internal server errors (500)

All errors return a standardized JSON response with error details.

## Security Considerations

- File upload size is limited to prevent DoS attacks
- File type validation ensures only allowed extensions are processed
- CORS is configured to restrict cross-origin requests
- Environment variables are used for sensitive configuration

## Performance

- Async/await pattern for non-blocking I/O operations
- Connection pooling for HTTP requests to AI engine
- GZip compression for response payloads
- Configurable timeout for AI engine requests

## Troubleshooting

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Import Errors

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### CORS Issues

Verify that your frontend URL is included in `CORS_ORIGINS` in the `.env` file.

### AI Engine Connection Failed

Check that:

1. AI engine is running
2. `AI_ENGINE_URL` is correctly configured
3. Network connectivity between services

## License

MIT License - Hackathon Project

## Contributing

This is a hackathon project. For contributions, please follow the standard pull request process.

## Support

For issues or questions, please contact the development team or create an issue in the project repository.
