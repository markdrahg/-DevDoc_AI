from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import time
import random

app = FastAPI(title="DevDocs AI API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class GitHubIngestRequest(BaseModel):
    url: HttpUrl

class QueryRequest(BaseModel):
    repo_id: str
    query: str

class QueryResponse(BaseModel):
    answer: str
    citations: List[dict]
    processing_time: float

class HealthScoreResponse(BaseModel):
    overall_score: int
    coverage: int
    quality: int
    completeness: int

# Mock data storage
repositories = {}
query_history = {}

# Mock responses for demo
MOCK_README = """# E-Commerce API

Production-ready REST API for a modern e-commerce platform — authentication, products, and Stripe payments out of the box.

## Overview

This project is a **REST API** powering an online storefront. It ships with JWT authentication, a Prisma-backed Postgres layer, Stripe Checkout, and a clean controller/route/middleware architecture.

## Quick Start

### 1. Install dependencies
```bash
npm install
```

### 2. Configure environment
Create a `.env` file with:
```
DATABASE_URL="postgresql://..."
JWT_SECRET="your-secret"
STRIPE_SECRET_KEY="sk_test_..."
```

### 3. Run migrations
```bash
npx prisma migrate dev
```

### 4. Start the server
```bash
npm run dev
```

## Features
- JWT Authentication
- Product Management
- Stripe Integration
- PostgreSQL Database
- RESTful API Design
- Error Handling Middleware
- Input Validation
- Rate Limiting

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh token

### Products
- `GET /api/products` - List all products
- `GET /api/products/:id` - Get product details
- `POST /api/products` - Create product (admin)
- `PUT /api/products/:id` - Update product (admin)
- `DELETE /api/products/:id` - Delete product (admin)

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders` - Get user orders
- `GET /api/orders/:id` - Get order details

## Architecture

The project follows a clean architecture pattern:
- **Controllers**: Handle HTTP requests/responses
- **Services**: Business logic
- **Models**: Data models (Prisma)
- **Middleware**: Authentication, validation, error handling
- **Routes**: API route definitions

## Testing

```bash
npm test
```

## License

MIT License
"""

MOCK_CITATIONS = [
    {
        "id": "1",
        "file": "src/auth/login.ts",
        "line": 42,
        "snippet": "async function authenticateUser(credentials: UserCredentials)",
        "url": "https://github.com/user/repo/blob/main/src/auth/login.ts#L42"
    },
    {
        "id": "2",
        "file": "src/api/routes.ts",
        "line": 18,
        "snippet": "router.post('/api/login', validateCredentials, handleLogin)",
        "url": "https://github.com/user/repo/blob/main/src/api/routes.ts#L18"
    },
    {
        "id": "3",
        "file": "src/database/user.model.ts",
        "line": 67,
        "snippet": "interface User { id: string; email: string; role: UserRole }",
        "url": "https://github.com/user/repo/blob/main/src/database/user.model.ts#L67"
    }
]

@app.get("/")
async def root():
    return {"message": "DevDocs AI API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/api/ingest/github")
async def ingest_github(request: GitHubIngestRequest):
    """Ingest a GitHub repository"""
    repo_id = f"repo_{int(time.time())}"
    
    # Simulate processing time
    time.sleep(1)
    
    repositories[repo_id] = {
        "id": repo_id,
        "url": str(request.url),
        "name": "ecommerce-api",
        "description": "Production-ready REST API for e-commerce",
        "language": "TypeScript",
        "files": 184,
        "loc": 12483,
        "status": "completed",
        "created_at": time.time()
    }
    
    return {
        "repo_id": repo_id,
        "status": "success",
        "message": "Repository ingested successfully",
        "metadata": repositories[repo_id]
    }

@app.post("/api/ingest/zip")
async def ingest_zip(file: UploadFile = File(...)):
    """Ingest a ZIP file"""
    repo_id = f"repo_{int(time.time())}"
    
    # Simulate processing
    time.sleep(1)
    
    repositories[repo_id] = {
        "id": repo_id,
        "name": file.filename.replace(".zip", ""),
        "description": "Uploaded project",
        "language": "Multiple",
        "files": random.randint(50, 200),
        "loc": random.randint(5000, 20000),
        "status": "completed",
        "created_at": time.time()
    }
    
    return {
        "repo_id": repo_id,
        "status": "success",
        "message": "ZIP file processed successfully",
        "metadata": repositories[repo_id]
    }

@app.post("/api/query")
async def query_repository(request: QueryRequest):
    """Query a repository"""
    start_time = time.time()
    
    if request.repo_id not in repositories:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Simulate AI processing
    time.sleep(0.5)
    
    # Generate contextual response based on query
    query_lower = request.query.lower()
    
    if "authentication" in query_lower or "auth" in query_lower or "login" in query_lower:
        answer = """The authentication system uses JWT (JSON Web Tokens) for secure user authentication. Here's how it works:

1. **User Registration**: Users register with email and password. Passwords are hashed using bcrypt before storage.

2. **Login Process**: When users log in, the system validates credentials and generates a JWT token containing the user ID and role.

3. **Token Usage**: The token is sent with each request in the Authorization header as a Bearer token.

4. **Middleware Protection**: Protected routes use authentication middleware that validates the JWT token before allowing access.

The main authentication functions are in `src/auth/login.ts` and the middleware is in `src/middleware/auth.ts`."""
        
    elif "database" in query_lower or "prisma" in query_lower:
        answer = """The project uses Prisma as an ORM with PostgreSQL database. Key aspects:

1. **Schema Definition**: Database schema is defined in `prisma/schema.prisma` with models for User, Product, and Order.

2. **Migrations**: Database migrations are managed through Prisma Migrate, ensuring version control of schema changes.

3. **Type Safety**: Prisma generates TypeScript types automatically, providing full type safety for database operations.

4. **Connection**: Database connection is configured through the DATABASE_URL environment variable.

The database models are located in `src/database/` directory."""
        
    elif "api" in query_lower or "endpoints" in query_lower or "routes" in query_lower:
        answer = """The API follows RESTful principles with the following main endpoints:

**Authentication Routes** (`/api/auth`):
- POST /register - Create new user account
- POST /login - Authenticate and get JWT token
- POST /refresh - Refresh expired token

**Product Routes** (`/api/products`):
- GET / - List all products with pagination
- GET /:id - Get specific product details
- POST / - Create new product (admin only)
- PUT /:id - Update product (admin only)
- DELETE /:id - Delete product (admin only)

**Order Routes** (`/api/orders`):
- POST / - Create new order
- GET / - Get user's orders
- GET /:id - Get order details

All routes are defined in `src/api/routes.ts` and use controllers from `src/controllers/`."""
        
    else:
        answer = f"""Based on your question about "{request.query}", this e-commerce API provides a comprehensive solution for building online stores.

The project is built with TypeScript and uses modern best practices including:
- JWT authentication for secure user management
- Prisma ORM for type-safe database operations
- Stripe integration for payment processing
- RESTful API design with proper error handling
- Middleware for validation and authentication

The codebase is well-structured with 184 files and approximately 12,483 lines of code, organized into controllers, services, models, and middleware layers.

Would you like more specific information about any particular aspect?"""
    
    processing_time = time.time() - start_time
    
    # Store query in history
    if request.repo_id not in query_history:
        query_history[request.repo_id] = []
    
    query_history[request.repo_id].append({
        "query": request.query,
        "answer": answer,
        "timestamp": time.time()
    })
    
    return QueryResponse(
        answer=answer,
        citations=MOCK_CITATIONS,
        processing_time=processing_time
    )

@app.get("/api/docs/{repo_id}")
async def get_documentation(repo_id: str):
    """Get generated documentation for a repository"""
    if repo_id not in repositories:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    return {
        "repo_id": repo_id,
        "documentation": MOCK_README,
        "format": "markdown",
        "generated_at": time.time()
    }

@app.get("/api/health/score/{repo_id}")
async def get_health_score(repo_id: str):
    """Get documentation health score"""
    if repo_id not in repositories:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    return HealthScoreResponse(
        overall_score=85,
        coverage=78,
        quality=92,
        completeness=88
    )

@app.get("/api/repositories")
async def list_repositories():
    """List all ingested repositories"""
    return {"repositories": list(repositories.values())}

@app.get("/api/repositories/{repo_id}")
async def get_repository(repo_id: str):
    """Get repository details"""
    if repo_id not in repositories:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    return repositories[repo_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Made with Bob
