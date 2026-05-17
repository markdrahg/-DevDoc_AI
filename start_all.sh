#!/bin/bash
# Quick Start Script for DevDoc AI - Mac/Linux
# Starts all three services in separate terminal tabs

echo "============================================================"
echo "Starting DevDoc AI Full Stack"
echo "============================================================"
echo ""
echo "This will start 3 services:"
echo "  1. AI Engine (Port 8001)"
echo "  2. Backend (Port 8000)"
echo "  3. Frontend (Port 5173)"
echo ""
echo "Press Ctrl+C in each terminal to stop the services"
echo "============================================================"
echo ""

# Function to start services based on OS
start_services() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Starting AI Engine..."
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"'/AI && source venv/bin/activate && python start_ai_engine.py"'
        sleep 3
        
        echo "Starting Backend..."
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"'/backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"'
        sleep 3
        
        echo "Starting Frontend..."
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"'/frontend && npm run dev"'
    else
        # Linux
        echo "Starting AI Engine..."
        gnome-terminal -- bash -c "cd AI && source venv/bin/activate && python start_ai_engine.py; exec bash"
        sleep 3
        
        echo "Starting Backend..."
        gnome-terminal -- bash -c "cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000; exec bash"
        sleep 3
        
        echo "Starting Frontend..."
        gnome-terminal -- bash -c "cd frontend && npm run dev; exec bash"
    fi
}

start_services

echo ""
echo "============================================================"
echo "All services are starting!"
echo "============================================================"
echo ""
echo "Check the opened terminals for status:"
echo "  - AI Engine: http://localhost:8001"
echo "  - Backend: http://localhost:8000"
echo "  - Frontend: http://localhost:5173"
echo ""
echo "Open your browser to: http://localhost:5173"
echo "============================================================"

# Made with Bob
