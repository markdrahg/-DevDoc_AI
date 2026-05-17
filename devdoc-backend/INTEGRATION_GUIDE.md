# Frontend-Backend Integration Guide

## Integration Complete!

The frontend and backend are now fully connected and ready to communicate.

## What Was Done

### 1. API Service Layer Created

- **File**: `frontend/src/services/api.ts`
- **Features**:
  - Health check endpoint
  - GitHub repository ingestion
  - ZIP file upload
  - PDF file upload
  - Ingestion status tracking
  - Q&A queries with citations
  - Documentation generation
  - Health score metrics

### 2. Environment Configuration

- **File**: `frontend/.env`
- **Backend URL**: `http://localhost:8000`
- Vite will automatically load this during development

### 3. Components Updated

- **RepositoryInput.tsx**: Now uses real API for GitHub and ZIP ingestion
- **QuestionInterface.tsx**: Now uses real API for Q&A queries
- Both components have proper error handling and user feedback

### 4. CORS Configuration Verified

- Backend allows origins: `http://localhost:3000` and `http://localhost:5173`
- All HTTP methods and headers allowed
- Credentials enabled for secure communication

## How to Test

### Step 1: Start the Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
[OK] CORS configured for origins: ['http://localhost:3000', 'http://localhost:5173']
```

### Step 2: Start the Frontend

```bash
cd frontend
npm run dev
```

Expected output:

```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Step 3: Test Health Check

Open a new terminal and run:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "ai_engine_status": "unavailable",
  "uptime": 123.45
}
```

### Step 4: Test in Browser

1. **Open the app**: Navigate to `http://localhost:5173`

2. **Test GitHub Ingestion**:
   - Enter a GitHub URL (e.g., `https://github.com/username/repo`)
   - Click "Generate Documentation"
   - Check browser console for API call logs
   - Check backend terminal for incoming request

3. **Test ZIP Upload**:
   - Switch to "Upload ZIP" tab
   - Select a ZIP file
   - Click "Generate Documentation"
   - Check console and backend logs

4. **Test Q&A Interface**:
   - Navigate to the Q&A section
   - Type a question
   - Click Send
   - Check console for API response

## Expected Behavior

### What Will Work

- Frontend → Backend communication
- File uploads (ZIP files)
- GitHub URL submission
- Request validation
- Error handling with user-friendly messages
- CORS (no browser errors)
- Loading states and animations

### What Won't Work Yet

- Backend → AI Engine communication (returns "AI engine unavailable")
- Actual code analysis
- Real documentation generation
- Citation retrieval

**Why?** The AI Engine (port 8001) hasn't been implemented yet by the AI team.

## Debugging Tips

### CORS Errors

If you see CORS errors in browser console:

1. Verify backend `.env` has: `CORS_ORIGINS=http://localhost:3000,http://localhost:5173`
2. Restart the backend server
3. Clear browser cache

### Connection Refused

If frontend can't connect to backend:

1. Verify backend is running: `netstat -ano | findstr :8000` (Windows) or `lsof -i :8000` (Mac/Linux)
2. Check `frontend/.env` has correct URL: `VITE_API_BASE_URL=http://localhost:8000`
3. Restart frontend dev server

### 503 Service Unavailable

This is expected! It means:

- Frontend → Backend: Working
- Backend → AI Engine: Not working (AI engine not running)

The backend will return this error until the AI team completes their service on port 8001.

## API Endpoints Available

### Health & Info

- `GET /health` - System health check
- `GET /` - API information

### Ingestion

- `POST /api/ingest/github` - Ingest GitHub repository
- `POST /api/ingest/zip` - Upload ZIP file
- `POST /api/ingest/pdf` - Upload PDF file
- `GET /api/ingest/status/{job_id}` - Check ingestion status

### Query

- `POST /api/query/` - Ask questions about code

### Documentation

- `POST /api/documentation/generate` - Generate documentation
- `GET /api/documentation/health/{repo_id}` - Get health score
- `GET /api/documentation/{repo_id}` - Get documentation

## Console Logs to Look For

### Successful GitHub Ingestion

```
 GitHub ingestion started: {
  job_id: "abc123",
  status: "processing",
  message: "GitHub repository ingestion started",
  ingestion_type: "github",
  created_at: "2024-01-15T10:30:00Z"
}
```

### Successful Query

```
 Query response: {
  answer: "...",
  citations: [...],
  confidence: 0.95,
  processing_time: 1.23
}
```

### Expected Error (AI Engine Not Running)

```
 Query failed: Error: AI engine unavailable
```

## Next Steps

1. **For Frontend Team**: Integration is complete! You can now test all UI flows.

2. **For Backend Team**: Backend is ready and waiting for AI engine.

3. **For AI Team**:
   - Implement AI engine on `http://localhost:8001`
   - Follow the API contract in `backend/app/services/ai_client.py`
   - Test with backend using the endpoints

## Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Health check returns 200 OK
- [ ] GitHub URL submission triggers API call
- [ ] ZIP upload triggers API call
- [ ] Q&A question triggers API call
- [ ] No CORS errors in browser console
- [ ] Error messages are user-friendly
- [ ] Loading states work correctly

## Success Criteria

**Integration is successful when:**

1. Frontend can call all backend endpoints
2. Backend receives and validates requests
3. Proper error handling on both sides
4. No CORS issues
5. User sees appropriate feedback (loading, success, errors)

The only expected failure is the AI engine communication, which is normal at this stage.

---

**Status**: Frontend-Backend Integration Complete
**Next**: Waiting for AI Engine implementation
