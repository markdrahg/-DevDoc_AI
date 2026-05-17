# 🚀 Quick Start Guide

Follow these simple steps to get DevDocs AI running on your machine.

## Step 1: Start the Backend (Terminal 1)

Open a terminal and run:

```bash
cd devdoc-backend
python -m venv venv
```

Activate the virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

Install dependencies and start:
```bash
pip install -r requirements.txt
python main.py
```

✅ Backend should now be running at `http://localhost:8000`

## Step 2: Start the Frontend (Terminal 2)

Open a **new terminal** and run:

```bash
cd devdoc-frontend
npm install
npm run dev
```

✅ Frontend should now be running at `http://localhost:5173`

## Step 3: Use the Application

1. Open your browser to `http://localhost:5173`
2. You'll see the DevDocs AI landing page
3. Try one of these options:
   - **GitHub URL**: Paste `https://github.com/yourusername/yourrepo`
   - **ZIP Upload**: Click "Upload ZIP" tab and select a project ZIP file

4. Click "Generate Documentation"
5. Wait a few seconds for processing
6. Explore the generated documentation and ask questions!

## 🎯 Demo Features to Try

### 1. View Documentation
- The center panel shows auto-generated README
- Scroll through to see the comprehensive documentation

### 2. Ask Questions
- Use the chat interface on the right
- Try questions like:
  - "How does authentication work?"
  - "Explain the database structure"
  - "What API endpoints are available?"

### 3. Check Health Metrics
- Bottom left shows documentation health score
- View coverage, quality, and completeness metrics

### 4. View Source Citations
- Bottom right shows code references
- See exactly where information comes from

## 🐛 Troubleshooting

### Backend won't start
- Make sure Python 3.9+ is installed: `python --version`
- Try: `pip install --upgrade pip`
- Then reinstall: `pip install -r requirements.txt`

### Frontend won't start
- Make sure Node.js 18+ is installed: `node --version`
- Delete `node_modules` and try again: `rm -rf node_modules && npm install`

### CORS errors
- Make sure backend is running on port 8000
- Make sure frontend is running on port 5173
- Check `.env` file in frontend has: `VITE_API_URL=http://localhost:8000`

### Port already in use
- Backend: Change port in `main.py` (line 344): `uvicorn.run(app, host="0.0.0.0", port=8001)`
- Frontend: Change port with: `npm run dev -- --port 3000`

## 📝 Notes

- This is a demo version with mock AI responses
- Perfect for hackathon demonstrations
- All data is temporary (not persisted to database)
- Works completely offline once started

## 🎉 You're Ready!

Your DevDocs AI system is now running. Enjoy exploring your codebase with AI-powered documentation!