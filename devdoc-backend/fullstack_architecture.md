# Full-Stack Repository Intelligence System
## Modular Architecture for 24-Hour Hackathon

**Stack**: React + FastAPI + Python AI Engine  
**AI**: IBM Granite + IBM BOB Reasoning  
**Database**: PostgreSQL with pgvector

---

## Project Structure

```
repo-intelligence/
├── frontend/                    # React + Tailwind UI
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── RepositoryInput.jsx      # GitHub URL / ZIP / PDF upload
│   │   │   ├── QuestionInterface.jsx    # Q&A interface
│   │   │   ├── DocumentationViewer.jsx  # Generated docs viewer
│   │   │   ├── HealthDashboard.jsx      # Health score metrics
│   │   │   └── SourceCitations.jsx      # Citation display
│   │   ├── services/
│   │   │   └── api.js                   # Backend API client
│   │   ├── hooks/
│   │   │   ├── useRepository.js         # Repository state management
│   │   │   └── useQuery.js              # Query state management
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── backend/                     # FastAPI REST API
│   ├── app/
│   │   ├── main.py                      # FastAPI app entry point
│   │   ├── config.py                    # Configuration
│   │   ├── models.py                    # Pydantic models
│   │   ├── database.py                  # Database connection
│   │   ├── routers/
│   │   │   ├── ingestion.py             # Ingestion endpoints
│   │   │   ├── query.py                 # Query endpoints
│   │   │   ├── documentation.py         # Documentation endpoints
│   │   │   └── health.py                # Health check endpoints
│   │   ├── services/
│   │   │   ├── file_handler.py          # File upload handling
│   │   │   └── ai_client.py             # AI engine communication
│   │   └── middleware/
│   │       ├── cors.py                  # CORS configuration
│   │       └── error_handler.py         # Error handling
│   ├── requirements.txt
│   └── .env.example
│
├── ai_engine/                   # AI Processing Engine
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── github_ingestion.py          # GitHub repo cloning & parsing
│   │   ├── zip_handler.py               # ZIP extraction & processing
│   │   ├── pdf_processor.py             # PDF text extraction
│   │   └── file_parser.py               # Multi-format file parsing
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── chunker.py                   # Semantic code chunking
│   │   ├── embeddings.py                # IBM Granite embeddings
│   │   ├── code_analyzer.py             # AST parsing & analysis
│   │   └── metadata_extractor.py        # Extract repo metadata
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── vector_search.py             # pgvector similarity search
│   │   ├── hybrid_search.py             # Vector + keyword search
│   │   └── context_builder.py           # Build hierarchical context
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── granite_client.py            # IBM Granite LLM client
│   │   ├── bob_reasoning.py             # IBM BOB reasoning layer
│   │   ├── prompt_templates.py          # Prompt engineering
│   │   └── response_generator.py        # Generate responses with citations
│   ├── documentation/
│   │   ├── __init__.py
│   │   ├── doc_generator.py             # Auto-generate documentation
│   │   ├── health_scorer.py             # Documentation health scoring
│   │   └── templates/                   # Documentation templates
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py                    # SQLAlchemy models
│   │   ├── repositories.py              # Repository CRUD
│   │   ├── documents.py                 # Document CRUD
│   │   └── chunks.py                    # Chunk CRUD
│   ├── config.py                        # AI engine configuration
│   ├── main.py                          # AI engine entry point
│   └── requirements.txt
│
├── shared/                      # Shared utilities
│   ├── schemas.py                       # Shared data models
│   └── utils.py                         # Common utilities
│
├── docker-compose.yml           # Local development setup
├── .env.example                 # Environment variables template
└── README.md                    # Project documentation
```

---

## Component Responsibilities

### 1. Frontend (`frontend/`)

**Purpose**: User interface for repository intelligence system

**Responsibilities**:
- Provide intuitive UI for repository ingestion
- Handle file uploads (ZIP, PDF)
- Display Q&A interface with real-time responses
- Show generated documentation
- Display health score dashboard
- Render source citations with syntax highlighting

**Technology Stack**:
```json
{
  "framework": "React 18",
  "styling": "Tailwind CSS",
  "build": "Vite",
  "state": "React Context API / Zustand",
  "http": "Axios",
  "routing": "React Router",
  "ui": "Headless UI / Radix UI",
  "syntax": "Prism.js / Highlight.js"
}
```

**Key Features**:
- Repository input (GitHub URL, ZIP, PDF)
- Real-time ingestion progress
- Question answering with streaming responses
- Documentation viewer with navigation
- Health metrics dashboard
- Citation viewer with file preview

---

### 2. Backend (`backend/`)

**Purpose**: Lightweight REST API orchestrating frontend and AI engine

**Responsibilities**:
- Expose REST endpoints for frontend
- Handle file uploads and validation
- Manage request/response flow
- Communicate with AI engine
- Handle errors gracefully
- Provide health checks and status updates

**Technology Stack**:
```python
# Core
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0

# File handling
python-multipart==0.0.6
aiofiles==23.2.1

# HTTP client for AI engine
httpx==0.25.2

# Database (lightweight connection)
sqlalchemy==2.0.23
psycopg2-binary==2.9.9

# Utilities
python-dotenv==1.0.0
```

**Key Features**:
- RESTful API design
- Async request handling
- File upload management
- AI engine proxy
- Error handling middleware
- CORS configuration

---

### 3. AI Engine (`ai_engine/`)

**Purpose**: Core intelligence - ingestion, processing, RAG, and documentation generation

**Responsibilities**:
- Ingest repositories from multiple sources
- Parse and chunk code semantically
- Generate embeddings using IBM Granite
- Perform vector and hybrid search
- Build repository-aware context
- Generate responses using IBM BOB reasoning
- Auto-generate documentation
- Calculate documentation health scores

**Technology Stack**:
```python
# AI/ML
ibm-watsonx-ai==0.1.0  # IBM Granite & BOB
sentence-transformers==2.2.2  # Fallback embeddings

# Code parsing
tree-sitter==0.20.4
pygments==2.17.2

# Ingestion
GitPython==3.1.40
PyGithub==2.1.1
PyMuPDF==1.23.8  # PDF processing

# Vector database
pgvector==0.2.3
sqlalchemy==2.0.23

# Processing
numpy==1.26.2
tiktoken==0.5.2  # Token counting

# Utilities
python-dotenv==1.0.0
```

**Key Features**:
- Multi-source ingestion pipeline
- Semantic code chunking
- IBM Granite embeddings
- pgvector similarity search
- IBM BOB reasoning layer
- Citation-based responses
- Documentation generation
- Health scoring algorithm

---

## Communication Flow

### Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend - React"
        A[User Interface]
        B[API Client]
    end
    
    subgraph "Backend - FastAPI"
        C[REST API]
        D[File Handler]
        E[AI Client]
    end
    
    subgraph "AI Engine - Python"
        F[Ingestion Pipeline]
        G[Processing Layer]
        H[RAG Engine]
        I[Doc Generator]
    end
    
    subgraph "Storage"
        J[(PostgreSQL + pgvector)]
        K[File Storage]
    end
    
    A -->|HTTP/REST| B
    B -->|API Calls| C
    C --> D
    C --> E
    D --> K
    E -->|Internal API| F
    E -->|Internal API| H
    E -->|Internal API| I
    F --> G
    G --> J
    H --> J
    I --> J
```

---

## API Contracts

### Frontend ↔ Backend

**Base URL**: `http://localhost:8000/api/v1`

#### 1. Repository Ingestion

**POST /repositories/ingest/github**
```json
Request:
{
  "url": "https://github.com/user/repo",
  "branch": "main"  // optional
}

Response:
{
  "task_id": "uuid",
  "status": "queued",
  "repository_id": "uuid"
}
```

**POST /repositories/ingest/upload**
```json
Request: multipart/form-data
- file: ZIP or PDF file
- type: "zip" | "pdf"

Response:
{
  "task_id": "uuid",
  "status": "processing",
  "repository_id": "uuid"
}
```

**GET /repositories/{repo_id}/status**
```json
Response:
{
  "repository_id": "uuid",
  "status": "processing" | "completed" | "failed",
  "progress": 75,
  "files_processed": 120,
  "total_files": 150,
  "error": null
}
```

#### 2. Query Interface

**POST /query**
```json
Request:
{
  "repository_id": "uuid",
  "question": "How does authentication work?",
  "stream": false  // optional, for streaming responses
}

Response:
{
  "answer": "Authentication is handled by...",
  "confidence": 0.92,
  "sources": [
    {
      "file": "auth/service.py",
      "lines": "15-25",
      "content": "def authenticate(...)...",
      "relevance": 0.95
    }
  ],
  "reasoning": "Based on the AuthService class..."
}
```

**POST /query/stream** (Server-Sent Events)
```json
Request: Same as /query

Response: SSE stream
data: {"type": "thinking", "content": "Analyzing repository..."}
data: {"type": "sources", "content": [...]}
data: {"type": "answer", "content": "Authentication is..."}
data: {"type": "done"}
```

#### 3. Documentation

**GET /repositories/{repo_id}/documentation**
```json
Response:
{
  "repository_id": "uuid",
  "documentation": {
    "overview": "This repository...",
    "architecture": "The system consists of...",
    "api_reference": [...],
    "setup_guide": "To get started..."
  },
  "generated_at": "2024-01-15T10:30:00Z"
}
```

**POST /repositories/{repo_id}/documentation/generate**
```json
Request:
{
  "sections": ["overview", "api", "setup"]  // optional
}

Response:
{
  "task_id": "uuid",
  "status": "generating"
}
```

#### 4. Health Dashboard

**GET /repositories/{repo_id}/health**
```json
Response:
{
  "repository_id": "uuid",
  "overall_score": 85,
  "metrics": {
    "documentation_coverage": 78,
    "code_quality": 92,
    "test_coverage": 65,
    "dependency_health": 88
  },
  "issues": [
    {
      "severity": "medium",
      "type": "missing_docstrings",
      "count": 15,
      "files": ["src/utils.py", "src/helpers.py"]
    }
  ],
  "recommendations": [
    "Add docstrings to 15 functions",
    "Update outdated dependencies"
  ]
}
```

#### 5. Repository Management

**GET /repositories**
```json
Response:
{
  "repositories": [
    {
      "id": "uuid",
      "name": "my-repo",
      "source": "github",
      "url": "https://github.com/user/repo",
      "status": "completed",
      "ingested_at": "2024-01-15T10:00:00Z",
      "file_count": 150,
      "health_score": 85
    }
  ],
  "total": 1
}
```

**DELETE /repositories/{repo_id}**
```json
Response:
{
  "message": "Repository deleted successfully"
}
```

---

### Backend ↔ AI Engine

**Communication Method**: Internal Python function calls (same process) or HTTP API (separate service)

**Option 1: Direct Import (Recommended for Hackathon)**
```python
# backend/app/services/ai_client.py
from ai_engine.ingestion import github_ingestion
from ai_engine.rag import response_generator
from ai_engine.documentation import doc_generator

class AIEngineClient:
    def ingest_github(self, url: str, branch: str):
        return github_ingestion.ingest_repository(url, branch)
    
    def query_repository(self, repo_id: str, question: str):
        return response_generator.generate_response(repo_id, question)
    
    def generate_documentation(self, repo_id: str):
        return doc_generator.generate_docs(repo_id)
```

**Option 2: Internal HTTP API (For Scalability)**
```python
# AI Engine exposes internal API on port 8001
# Backend calls AI Engine via HTTP

# backend/app/services/ai_client.py
import httpx

class AIEngineClient:
    def __init__(self):
        self.base_url = "http://localhost:8001"
        self.client = httpx.AsyncClient()
    
    async def ingest_github(self, url: str, branch: str):
        response = await self.client.post(
            f"{self.base_url}/ingest/github",
            json={"url": url, "branch": branch}
        )
        return response.json()
```

**Recommended for Hackathon**: Option 1 (Direct Import) - Simpler, faster to implement

---

## Technology Stack Summary

### Frontend
```javascript
// package.json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "zustand": "^4.4.7",
    "@headlessui/react": "^1.7.17",
    "@heroicons/react": "^2.1.1",
    "prismjs": "^1.29.0",
    "react-markdown": "^9.0.1"
  },
  "devDependencies": {
    "vite": "^5.0.8",
    "tailwindcss": "^3.3.6",
    "@vitejs/plugin-react": "^4.2.1"
  }
}
```

### Backend
```python
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
aiofiles==23.2.1
httpx==0.25.2
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0  # For JWT if needed
```

### AI Engine
```python
# requirements.txt
# IBM AI
ibm-watsonx-ai==0.1.0
ibm-generative-ai==2.3.0

# Vector DB
pgvector==0.2.3
sqlalchemy==2.0.23
psycopg2-binary==2.9.9

# Code Processing
tree-sitter==0.20.4
tree-sitter-python==0.20.4
tree-sitter-javascript==0.20.3
pygments==2.17.2

# Ingestion
GitPython==3.1.40
PyGithub==2.1.1
PyMuPDF==1.23.8
python-docx==1.1.0

# ML/Processing
numpy==1.26.2
tiktoken==0.5.2
sentence-transformers==2.2.2

# Utilities
python-dotenv==1.0.0
pydantic==2.5.0
```

---

## 24-Hour Implementation Order

### Phase 1: Foundation (Hours 0-4)

**Hour 0-1: Project Setup**
```bash
# Create project structure
mkdir -p frontend/src/{components,services,hooks}
mkdir -p backend/app/{routers,services,middleware}
mkdir -p ai_engine/{ingestion,processing,retrieval,rag,documentation,database}

# Initialize frontend
cd frontend
npm create vite@latest . -- --template react
npm install axios zustand @headlessui/react @heroicons/react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Initialize backend
cd ../backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn python-multipart

# Initialize AI engine
cd ../ai_engine
python -m venv venv
source venv/bin/activate
pip install sqlalchemy psycopg2-binary pgvector
```

**Hour 1-2: Database Setup**
```sql
-- Create database
CREATE DATABASE repo_intelligence;

-- Enable pgvector
CREATE EXTENSION vector;

-- Create tables (in ai_engine/database/models.py)
```

**Hour 2-3: Backend API Skeleton**
- Set up FastAPI app structure
- Create basic routers
- Add CORS middleware
- Test with simple endpoints

**Hour 3-4: Frontend Skeleton**
- Set up React app structure
- Create basic components
- Set up routing
- Configure Tailwind

**Deliverable**: Project structure ready, basic apps running

---

### Phase 2: Core AI Engine (Hours 4-10)

**Hour 4-5: GitHub Ingestion**
```python
# ai_engine/ingestion/github_ingestion.py
- Clone repository
- Extract files
- Store in database
```

**Hour 5-6: Chunking & Embeddings**
```python
# ai_engine/processing/chunker.py
- Implement semantic chunking
- Token counting

# ai_engine/processing/embeddings.py
- IBM Granite integration
- Batch embedding generation
```

**Hour 6-7: Vector Search**
```python
# ai_engine/retrieval/vector_search.py
- pgvector similarity search
- Context retrieval
```

**Hour 7-9: RAG Pipeline**
```python
# ai_engine/rag/granite_client.py
- IBM Granite LLM client

# ai_engine/rag/bob_reasoning.py
- IBM BOB reasoning layer

# ai_engine/rag/response_generator.py
- Generate responses with citations
```

**Hour 9-10: Testing AI Engine**
- Test ingestion with sample repo
- Test query with sample questions
- Verify citations

**Deliverable**: Working AI engine with RAG

---

### Phase 3: Backend Integration (Hours 10-13)

**Hour 10-11: Ingestion Endpoints**
```python
# backend/app/routers/ingestion.py
- POST /repositories/ingest/github
- POST /repositories/ingest/upload
- GET /repositories/{id}/status
```

**Hour 11-12: Query Endpoints**
```python
# backend/app/routers/query.py
- POST /query
- POST /query/stream (SSE)
```

**Hour 12-13: Integration & Testing**
- Connect backend to AI engine
- Test all endpoints
- Handle errors

**Deliverable**: Working backend API

---

### Phase 4: Frontend Development (Hours 13-17)

**Hour 13-14: Repository Input Component**
```jsx
// frontend/src/components/RepositoryInput.jsx
- GitHub URL input
- ZIP/PDF upload
- Progress indicator
```

**Hour 14-15: Question Interface**
```jsx
// frontend/src/components/QuestionInterface.jsx
- Question input
- Response display
- Citation viewer
```

**Hour 15-16: API Integration**
```javascript
// frontend/src/services/api.js
- Axios client
- API methods
- Error handling
```

**Hour 16-17: UI Polish**
- Tailwind styling
- Loading states
- Error messages
- Responsive design

**Deliverable**: Working frontend UI

---

### Phase 5: Advanced Features (Hours 17-20)

**Hour 17-18: Documentation Generation**
```python
# ai_engine/documentation/doc_generator.py
- Generate overview
- Generate API docs
- Generate setup guide
```

**Hour 18-19: Health Scoring**
```python
# ai_engine/documentation/health_scorer.py
- Calculate metrics
- Identify issues
- Generate recommendations
```

**Hour 19-20: Frontend Dashboard**
```jsx
// frontend/src/components/HealthDashboard.jsx
- Display health metrics
- Show issues
- Recommendations
```

**Deliverable**: Documentation and health features

---

### Phase 6: Polish & Demo (Hours 20-24)

**Hour 20-21: Integration Testing**
- Test full workflow
- Fix critical bugs
- Optimize performance

**Hour 21-22: Demo Preparation**
- Ingest demo repositories
- Prepare demo script
- Create demo questions

**Hour 22-23: Documentation**
- README with setup instructions
- API documentation
- Architecture diagram

**Hour 23-24: Final Polish**
- UI improvements
- Error handling
- Deploy (if needed)

**Deliverable**: Demo-ready application

---

## Simplified API Flow

### 1. Repository Ingestion Flow

```
User (Frontend)
    ↓ [POST /repositories/ingest/github]
Backend API
    ↓ [Call ai_engine.ingestion.github_ingestion]
AI Engine
    ↓ [Clone repo, parse files, chunk, embed]
PostgreSQL + pgvector
    ↓ [Store chunks and embeddings]
Backend API
    ↓ [Return task_id and status]
Frontend
    ↓ [Poll /repositories/{id}/status]
Backend API
    ↓ [Check status from database]
Frontend
    ↓ [Display progress]
```

### 2. Query Flow

```
User (Frontend)
    ↓ [POST /query with question]
Backend API
    ↓ [Call ai_engine.rag.response_generator]
AI Engine
    ↓ [Generate query embedding]
pgvector
    ↓ [Similarity search, return chunks]
AI Engine
    ↓ [Build context with IBM BOB reasoning]
IBM Granite LLM
    ↓ [Generate response with citations]
AI Engine
    ↓ [Format response]
Backend API
    ↓ [Return response with sources]
Frontend
    ↓ [Display answer and citations]
```

### 3. Documentation Generation Flow

```
User (Frontend)
    ↓ [POST /repositories/{id}/documentation/generate]
Backend API
    ↓ [Call ai_engine.documentation.doc_generator]
AI Engine
    ↓ [Analyze repository structure]
AI Engine
    ↓ [Generate sections using IBM Granite]
PostgreSQL
    ↓ [Store generated documentation]
Backend API
    ↓ [Return task_id]
Frontend
    ↓ [Poll for completion]
Frontend
    ↓ [GET /repositories/{id}/documentation]
Backend API
    ↓ [Return documentation]
Frontend
    ↓ [Display in viewer]
```

---

## Environment Configuration

### Frontend (`.env`)
```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
```

### Backend (`.env`)
```bash
# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/repo_intelligence

# AI Engine
AI_ENGINE_URL=http://localhost:8001  # If using separate service
AI_ENGINE_DIRECT=true  # If using direct import

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# File Upload
MAX_UPLOAD_SIZE=100000000  # 100MB
UPLOAD_DIR=./uploads
```

### AI Engine (`.env`)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/repo_intelligence

# IBM Watsonx
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# IBM Granite Model
GRANITE_MODEL_ID=ibm/granite-13b-chat-v2
GRANITE_EMBEDDING_MODEL=ibm/slate-125m-english-rtrvr

# Processing
MAX_CHUNK_SIZE=512
CHUNK_OVERLAP=50
MAX_FILE_SIZE=10485760  # 10MB

# Vector Search
VECTOR_SEARCH_TOP_K=10
SIMILARITY_THRESHOLD=0.7
```

---

## Docker Compose (Optional)

```yaml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: repo_intelligence
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/repo_intelligence
    depends_on:
      - postgres
    volumes:
      - ./backend:/app
      - ./ai_engine:/ai_engine

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      VITE_API_BASE_URL: http://localhost:8000/api/v1
    volumes:
      - ./frontend:/app

volumes:
  postgres_data:
```

---

## Key Design Decisions

### 1. Why Separate Frontend/Backend/AI Engine?

**Frontend Separation**:
- Independent development and deployment
- Can be hosted on CDN
- Easy to swap UI framework
- Better for team collaboration

**Backend as Orchestrator**:
- Lightweight API layer
- Handles HTTP concerns (CORS, auth, file uploads)
- Easy to scale horizontally
- Clear separation of concerns

**AI Engine as Core**:
- Heavy processing isolated
- Can be scaled independently
- Reusable across different interfaces
- Easy to test and optimize

### 2. Why Direct Import vs HTTP API?

**For Hackathon**: Direct Import
- Simpler to implement
- Faster (no network overhead)
- Easier to debug
- Single deployment

**For Production**: HTTP API
- Better scalability
- Independent scaling
- Language agnostic
- Fault isolation

### 3. Why PostgreSQL + pgvector?

- Single database for all data
- Native vector search
- ACID compliance
- Easy to set up
- Good enough for MVP

### 4. Why React + Tailwind?

- Fast development
- Component reusability
- Large ecosystem
- Easy styling with Tailwind
- Good for demos

---

## Critical Success Factors

### 1. Keep It Simple
- Start with direct imports (not HTTP API)
- Use simple chunking initially
- Basic UI first, polish later
- Focus on core RAG pipeline

### 2. Test Early
- Test AI engine independently first
- Test backend endpoints with Postman
- Test frontend with mock data
- Integration test last

### 3. Modular Development
- Each component can be developed independently
- Clear interfaces between components
- Easy to swap implementations
- Easy to debug

### 4. Demo Focus
- Prepare demo repositories in advance
- Have backup questions ready
- Test demo flow multiple times
- Have fallback if live demo fails

---

## Next Steps

1. **Review this architecture** - Ensure it meets your needs
2. **Set up project structure** - Create folders and files
3. **Start with AI engine** - Get core RAG working first
4. **Build backend** - Create API layer
5. **Develop frontend** - Build UI last
6. **Integrate and test** - Connect all pieces
7. **Polish and demo** - Prepare for presentation

Ready to start implementation? I can help you:
- Generate boilerplate code for each component
- Create detailed implementation guides
- Set up the project structure
- Write specific code modules

Would you like me to switch to Code mode to start implementing?