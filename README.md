# DevDocs AI - Intelligent Code Documentation System

An AI-powered tool that automatically generates comprehensive documentation for your codebase and answers questions about your code using IBM Watsonx.

## 🚀 Features

- **GitHub Repository Analysis**: Paste a GitHub URL and get instant documentation
- **ZIP File Upload**: Upload your project as a ZIP file for analysis
- **AI-Powered Q&A**: Ask questions about your codebase and get intelligent answers
- **Documentation Health Score**: Get metrics on your documentation quality
- **Source Citations**: See exactly where information comes from in your code
- **Beautiful UI**: Modern, responsive interface with dark mode support

## 📋 Prerequisites

- **Frontend**: Node.js 18+ and npm
- **Backend**: Python 3.9+
- **Browser**: Modern browser with JavaScript enabled

## 🛠️ Installation & Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd devdoc-backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd devdoc-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🎯 Usage

1. **Start Both Servers**: Make sure both backend (port 8000) and frontend (port 5173) are running

2. **Upload Your Code**:
   - Option A: Paste a GitHub repository URL
   - Option B: Upload a ZIP file of your project

3. **View Documentation**: The system will automatically generate comprehensive documentation

4. **Ask Questions**: Use the chat interface to ask questions about your codebase

5. **Check Health Metrics**: View documentation quality scores and metrics

## 📁 Project Structure

```
DevDoc AI/
├── devdoc-backend/          # FastAPI backend
│   ├── main.py             # Main API server
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Backend documentation
│
├── devdoc-frontend/         # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service layer
│   │   ├── assets/         # Images, icons, etc.
│   │   └── App.tsx         # Main app component
│   ├── package.json        # Node dependencies
│   └── README.md          # Frontend documentation
│
└── README.md               # This file
```

## 🔧 API Endpoints

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

## 🎨 Tech Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

### Backend
- **FastAPI** - Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## 🚧 Current Status

This is a **demo/hackathon version** with mock data responses. The system is fully functional for demonstration purposes.

### What Works:
✅ Full UI with 3-column layout
✅ GitHub URL and ZIP file upload
✅ Mock documentation generation
✅ AI-powered Q&A with contextual responses
✅ Health metrics dashboard
✅ Source citations display
✅ Dark mode support
✅ Responsive design

### Future Enhancements:
- Real IBM Watsonx API integration
- Database persistence (PostgreSQL + pgvector)
- Real-time code analysis
- Multiple programming language support
- Advanced code metrics
- Export functionality (PDF, Markdown)

## 🤝 Contributing

This is a hackathon project. Feel free to fork and enhance!

## 📝 License

MIT License - feel free to use this project for your own purposes.

## 🎉 Acknowledgments

- Built for hackathon submission
- Powered by IBM Watsonx (integration pending)
- UI inspired by modern developer tools

## 📞 Support

For issues or questions, please open an issue in the repository.

---

**Made with ❤️ for developers who love good documentation**