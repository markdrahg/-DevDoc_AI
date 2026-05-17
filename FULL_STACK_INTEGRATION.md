# 🚀 Full Stack Integration Guide - DevDoc AI

Complete guide to integrate and run Frontend → Backend → AI Engine

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
4. [Running the System](#running-the-system)
5. [Testing the Integration](#testing-the-integration)
6. [Troubleshooting](#troubleshooting)
7. [API Documentation](#api-documentation)

---

## 🏗️ Architecture Overview

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Backend   │─────▶│  AI Engine  │
│  (React)    │      │  (FastAPI)  │      │  (FastAPI)  │
│  Port 5173  │      │  Port 8000  │      │  Port 8001  │
└─────────────┘      └─────────────┘      └─────────────┘
```

### Component Responsibilities

**Frontend (React + Vite)**

- User interface for code upload and Q&A
- Communicates with Backend API
- Location: `frontend/`

**Backend (FastAPI)**

- API gateway and request routing
- File upload handling
- Forwards requests to AI Engine
- Location: `backend/`

**AI Engine (FastAPI + IBM Granite)**

- Code ingestion and processing
- RAG-based Q&A system
- Documentation generation
- Health scoring
- Location: `AI/`

---

## ✅ Prerequisites

### Required Software

- **Python 3.10+** (for Backend and AI Engine)
- **Node.js 18+** (for Frontend)
- **Git** (for repository cloning)

### Required Accounts

- **IBM Cloud Account** with watsonx.ai access
  - Get API Key from: https://cloud.ibm.com/iam/apikeys
  - Get Project ID from your watsonx.ai project

### System Requirements

- **RAM**: 8GB minimum (16GB recommended for AI Engine)
- **Storage**: 5GB free space
- **OS**: Windows, macOS, or Linux

---

## 🔧 Setup Instructions

### Step 1: Clone and Navigate

```bash
cd /path/to/DevDoc_AI
```

### Step 2: Setup AI Engine

```bash
cd AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r ai_engine/requirements.txt

# Configure environment variables
# Edit AI/.env and add your IBM credentials:
# IBM_API_KEY=your_actual_api_key
# IBM_PROJECT_ID=your_actual_project_id
# IBM_URL=https://us-south.ml.cloud.ibm.com
```

**Important**: Replace `your_actual_api_key` and `your_actual_project_id` with real values from IBM Cloud.

### Step 3: Setup Backend

```bash
cd ../backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify .env file exists (should already be configured)
# backend/.env should have:
# AI_ENGINE_URL=http://localhost:8001
```

### Step 4: Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Verify .env file exists (should already be configured)
# frontend/.env should have:
# VITE_API_BASE_URL=http://localhost:8000
```

---

## 🚀 Running the System

You need **3 terminal windows** to run all components:

### Terminal 1: Start AI Engine

```bash
cd AI
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

python start_ai_engine.py
```

**Expected Output:**

```
============================================================
🚀 Starting DevDoc AI Engine
============================================================
Host: 0.0.0.0
Port: 8001
URL: http://localhost:8001
Docs: http://localhost:8001/docs
============================================================
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

### Terminal 2: Start Backend

```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
[OK] CORS configured for origins: ['http://localhost:3000', 'http://localhost:5173']
```

### Terminal 3: Start Frontend

```bash
cd frontend
npm run dev
```

**Expected Output:**

```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

## 🧪 Testing the Integration

### Test 1: Health Checks

**AI Engine:**

```bash
curl http://localhost:8001/health
```

Expected: `{"status":"healthy","version":"1.0.0",...}`

**Backend:**

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy","ai_engine_status":"healthy",...}`

### Test 2: Frontend Access

1. Open browser: `http://localhost:5173`
2. You should see the DevDoc AI interface

### Test 3: GitHub Repository Ingestion

1. In the frontend, enter a GitHub URL:
   ```
   https://github.com/username/small-repo
   ```
2. Click "Generate Documentation"
3. Check all 3 terminal windows for logs:
   - Frontend: API call logs in browser console (F12)
   - Backend: Incoming request and forwarding to AI
   - AI Engine: Processing and ingestion logs

### Test 4: Q&A System

1. After ingestion completes, navigate to Q&A section
2. Ask a question: "What does this project do?"
3. Verify you get an AI-generated response

### Test 5: Full Flow Test

```bash
# From project root
cd backend
python -m pytest tests/test_integration.py -v
```

---

## 🐛 Troubleshooting

### Issue: AI Engine Won't Start

**Symptom:** `ModuleNotFoundError` or import errors

**Solution:**

```bash
cd AI
pip install -r ai_engine/requirements.txt --upgrade
```

**Symptom:** `ValueError: Missing IBM credentials`

**Solution:**

1. Check `AI/.env` file exists
2. Verify IBM_API_KEY and IBM_PROJECT_ID are set
3. Test credentials:

```bash
cd AI
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('IBM_API_KEY'))"
```

### Issue: Backend Can't Connect to AI Engine

**Symptom:** Backend returns `503 Service Unavailable`

**Solution:**

1. Verify AI Engine is running on port 8001
2. Check `backend/.env` has `AI_ENGINE_URL=http://localhost:8001`
3. Test connection:

```bash
curl http://localhost:8001/health
```

### Issue: Frontend Can't Connect to Backend

**Symptom:** CORS errors or connection refused

**Solution:**

1. Verify Backend is running on port 8000
2. Check `frontend/.env` has `VITE_API_BASE_URL=http://localhost:8000`
3. Restart frontend dev server:

```bash
cd frontend
npm run dev
```

### Issue: Port Already in Use

**Symptom:** `Address already in use` error

**Solution:**

```bash
# Windows - Find and kill process
netstat -ano | findstr :8001
taskkill /PID <process_id> /F

# Mac/Linux
lsof -ti:8001 | xargs kill -9
```

### Issue: Slow AI Responses

**Symptom:** Queries take >30 seconds

**Solution:**

1. Reduce chunk size in `AI/.env`:
   ```
   CHUNK_SIZE=300
   ```
2. Limit chunks processed (already set to 500 max)
3. Use smaller test repositories initially

---

## 📚 API Documentation

### AI Engine Endpoints (Port 8001)

#### Health Check

```http
GET /health
```

#### GitHub Ingestion

```http
POST /api/ingest/github
Content-Type: application/json

{
  "repo_url": "https://github.com/user/repo",
  "branch": "main"
}
```

#### ZIP Upload

```http
POST /api/ingest/zip
Content-Type: multipart/form-data

file: <zip_file>
```

#### Query (Q&A)

```http
POST /api/query/
Content-Type: application/json

{
  "question": "What does this code do?",
  "repo_id": "uuid-here",
  "max_results": 5
}
```

#### Generate Documentation

```http
POST /api/documentation/generate
Content-Type: application/json

{
  "repo_id": "uuid-here",
  "doc_type": "full"
}
```

#### Health Score

```http
GET /api/documentation/health/{repo_id}
```

### Backend Endpoints (Port 8000)

Backend mirrors AI Engine endpoints and forwards requests.

### Frontend (Port 5173)

- **Home**: Upload interface
- **Q&A**: Question interface
- **Docs**: Documentation viewer

---

## 🎯 Quick Start Commands

### Start Everything (3 terminals)

**Terminal 1 - AI Engine:**

```bash
cd AI && venv\Scripts\activate && python start_ai_engine.py
```

**Terminal 2 - Backend:**

```bash
cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --port 8000
```

**Terminal 3 - Frontend:**

```bash
cd frontend && npm run dev
```

### Stop Everything

- Press `Ctrl+C` in each terminal

---

## 📊 System Status Checklist

Before testing, verify:

- [ ] AI Engine running on port 8001
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] IBM credentials configured in `AI/.env`
- [ ] All health checks return `200 OK`
- [ ] No CORS errors in browser console

---

## 🎉 Success Criteria

Your system is fully integrated when:

1. ✅ All 3 services start without errors
2. ✅ Health checks pass for all services
3. ✅ Frontend can upload a GitHub repository
4. ✅ Backend forwards request to AI Engine
5. ✅ AI Engine processes and stores data
6. ✅ Q&A system returns AI-generated answers
7. ✅ No errors in any terminal window

---

## 📞 Support

If you encounter issues:

1. Check all 3 terminal windows for error messages
2. Verify all `.env` files are configured correctly
3. Ensure all dependencies are installed
4. Test each component individually before full integration
5. Check the [Troubleshooting](#troubleshooting) section

---

## 🔗 Related Files

- **Frontend API**: [`frontend/src/services/api.ts`](frontend/src/services/api.ts)
- **Backend AI Client**: [`backend/app/services/ai_client.py`](backend/app/services/ai_client.py)
- **AI Engine API**: [`AI/ai_engine/api.py`](AI/ai_engine/api.py)
- **AI Engine Core**: [`AI/ai_engine/rag_cli.py`](AI/ai_engine/rag_cli.py)

---

**Last Updated:** 2024-01-15
**Version:** 1.0.0
**Status:** ✅ Ready for Integration
