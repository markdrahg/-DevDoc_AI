@echo off
REM Quick Start Script for DevDoc AI - Windows
REM Starts all three services in separate windows

echo ============================================================
echo Starting DevDoc AI Full Stack
echo ============================================================
echo.
echo This will open 3 terminal windows:
echo   1. AI Engine (Port 8001)
echo   2. Backend (Port 8000)
echo   3. Frontend (Port 5173)
echo.
echo Press Ctrl+C in each window to stop the services
echo ============================================================
echo.

REM Start AI Engine
echo Starting AI Engine...
start "DevDoc AI - AI Engine" cmd /k "cd AI && venv\Scripts\activate && python start_ai_engine.py"
timeout /t 3 /nobreak >nul

REM Start Backend
echo Starting Backend...
start "DevDoc AI - Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul

REM Start Frontend
echo Starting Frontend...
start "DevDoc AI - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================================
echo All services are starting!
echo ============================================================
echo.
echo Check the opened windows for status:
echo   - AI Engine: http://localhost:8001
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:5173
echo.
echo Open your browser to: http://localhost:5173
echo ============================================================
pause

@REM Made with Bob
