# 🚀 DevDoc AI - AI-Powered Code Documentation System

An intelligent code documentation and analysis system powered by IBM watsonx.ai Granite models. Built for the 24-hour hackathon.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.0-61DAFB.svg)](https://reactjs.org)
[![IBM watsonx](https://img.shields.io/badge/IBM-watsonx.ai-0062FF.svg)](https://www.ibm.com/watsonx)

---

## 📋 Overview

DevDoc AI automatically generates comprehensive documentation for your codebase using advanced AI. Simply upload your GitHub repository, ZIP file, or PDF documentation, and get instant insights through our intelligent Q&A system.

### Key Features

- 🤖 **AI-Powered Analysis** - IBM Granite 8B Code Instruct model
- 📚 **Auto Documentation** - Generate comprehensive docs automatically
- 💬 **Intelligent Q&A** - Ask questions about your codebase
- 📊 **Health Scoring** - Assess code quality and documentation coverage
- 🔍 **RAG System** - Retrieval-Augmented Generation for accurate answers
- 🌐 **Multi-Source** - GitHub repos, ZIP files, and PDFs

---

## 🏗️ Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│    Frontend     │─────▶│     Backend     │─────▶│   AI Engine     │
│  React + Vite   │      │     FastAPI     │      │     FastAPI     │
│   Port 5173     │      │    Port 8000    │      │    Port 8001    │
└─────────────────┘      └─────────────────┘      └─────────────────┘
        │                         │                         │
        │                         │                         │
    User Interface          API Gateway              AI Processing
    - Upload repos          - Request routing        - Code ingestion
    - Q&A interface         - File handling          - RAG pipeline
    - Doc viewer            - CORS handling          - IBM Granite LLM
                                                     - Vector search
                                                     - Doc generation
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **IBM Cloud Account** with watsonx.ai access

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd DevDoc_AI
```

### 2. Setup IBM Credentials

Get your credentials from [IBM Cloud](https://cloud.ibm.com):

1. Create a watsonx.ai project
2. Get your API Key from IAM
3. Copy your Project ID

Edit `AI/.env`:

```env
IBM_API_KEY=your_actual_api_key_here
IBM_PROJECT_ID=your_actual_project_id_here
IBM_URL=https://us-south.ml.cloud.ibm.com
```

### 3. Install Dependencies

**AI Engine:**

```bash
cd AI
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r ai_engine/requirements.txt
```

**Backend:**

```bash
cd ../backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

**Frontend:**

```bash
cd ../frontend
npm install
```

### 4. Start All Services

**Option A: Automatic (Windows)**

```bash
start_all.bat
```

**Option B: Automatic (Mac/Linux)**

```bash
chmod +x start_all.sh
./start_all.sh
```

**Option C: Manual (3 terminals)**

Terminal 1 - AI Engine:

```bash
cd AI
venv\Scripts\activate
python start_ai_engine.py
```

Terminal 2 - Backend:

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Terminal 3 - Frontend:

```bash
cd frontend
npm run dev
```

### 5. Access the Application

Open your browser to: **http://localhost:5173**

---

## 📚 Documentation

- **[Full Stack Integration Guide](FULL_STACK_INTEGRATION.md)** - Complete setup and integration
- **[Frontend-Backend Integration](INTEGRATION_GUIDE.md)** - API integration details
- **[Architecture Overview](fullstack_architecture.md)** - System design

---

## 🧪 Testing

### Health Checks

```bash
# AI Engine
curl http://localhost:8001/health

# Backend
curl http://localhost:8000/health
```

### Test GitHub Ingestion

```bash
curl -X POST http://localhost:8001/api/ingest/github \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/user/repo"}'
```

### Run Comprehensive Tests

```bash
cd AI
python comprehensive_test.py
```

---

## 📁 Project Structure

```
DevDoc_AI/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── services/        # API client
│   │   └── pages/           # Page components
│   └── .env                 # Frontend config
│
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   └── middleware/      # CORS, error handling
│   └── .env                 # Backend config
│
├── AI/                       # AI Engine
│   ├── ai_engine/
│   │   ├── api.py           # FastAPI wrapper
│   │   ├── rag_cli.py       # Core RAG logic
│   │   ├── ingestion/       # Data ingestion
│   │   ├── processing/      # Chunking, embeddings
│   │   ├── retrieval/       # Vector search
│   │   ├── rag/             # RAG pipeline
│   │   └── documentation/   # Doc generation
│   └── .env                 # AI Engine config
│
├── start_all.bat            # Windows quick start
├── start_all.sh             # Mac/Linux quick start
└── FULL_STACK_INTEGRATION.md
```

---

## 🔧 Configuration

### Environment Variables

**AI Engine (`AI/.env`)**

```env
IBM_API_KEY=your_key
IBM_PROJECT_ID=your_project_id
IBM_URL=https://us-south.ml.cloud.ibm.com
PORT=8001
```

**Backend (`backend/.env`)**

```env
AI_ENGINE_URL=http://localhost:8001
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Frontend (`frontend/.env`)**

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🎯 Usage

### 1. Upload Code

- **GitHub Repository**: Paste repository URL
- **ZIP File**: Upload compressed codebase
- **PDF**: Upload documentation files

### 2. Ask Questions

Navigate to Q&A interface and ask:

- "What does this project do?"
- "Explain the main architecture"
- "How does authentication work?"
- "What are the API endpoints?"

### 3. Generate Documentation

Click "Generate Documentation" to create:

- Project overview
- Architecture diagrams
- API documentation
- Code structure analysis

### 4. View Health Score

Get insights on:

- Documentation coverage
- Code quality metrics
- Improvement recommendations

---

## 🛠️ Technology Stack

### Frontend

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling

### Backend

- **FastAPI** - Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### AI Engine

- **IBM watsonx.ai** - LLM platform
- **Granite 8B** - Code-specialized model
- **SentenceTransformers** - Embeddings
- **SQLAlchemy** - Database ORM
- **PyMuPDF** - PDF processing
- **GitPython** - Repository handling

---

## 🐛 Troubleshooting

### AI Engine Won't Start

**Issue**: Missing IBM credentials

**Solution**:

```bash
cd AI
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('IBM_API_KEY'))"
```

### Backend Can't Connect to AI Engine

**Issue**: AI Engine not running

**Solution**:

```bash
curl http://localhost:8001/health
```

### Frontend CORS Errors

**Issue**: Backend CORS misconfigured

**Solution**: Check `backend/.env` has correct origins

See [FULL_STACK_INTEGRATION.md](FULL_STACK_INTEGRATION.md#troubleshooting) for more.

---

## 📊 API Endpoints

### AI Engine (Port 8001)

- `GET /health` - Health check
- `POST /api/ingest/github` - Ingest GitHub repo
- `POST /api/ingest/zip` - Upload ZIP file
- `POST /api/query/` - Ask questions
- `POST /api/documentation/generate` - Generate docs
- `GET /api/documentation/health/{repo_id}` - Health score

### Backend (Port 8000)

Backend mirrors AI Engine endpoints and forwards requests.

---

## 🤝 Team

Built during 24-hour hackathon by:

- **Frontend Team** - React UI and user experience
- **Backend Team** - API gateway and integration
- **AI Team** - RAG pipeline and IBM Granite integration

---

## 📝 License

This project was created for educational purposes during a hackathon.

---

## 🙏 Acknowledgments

- **IBM watsonx.ai** for providing the Granite LLM
- **FastAPI** for the excellent web framework
- **React** for the powerful UI library

---

## 📞 Support

For issues and questions:

1. Check [FULL_STACK_INTEGRATION.md](FULL_STACK_INTEGRATION.md)
2. Review terminal logs for errors
3. Verify all `.env` files are configured
4. Ensure all services are running

---

**Status**: ✅ Ready for Production
**Version**: 1.0.0
**Last Updated**: 2024-01-15
