"""
AI Engine Startup Script
Starts the FastAPI server on port 8001
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    host = os.getenv("HOST", "0.0.0.0")
    
    print("=" * 60)
    print("🚀 Starting DevDoc AI Engine")
    print("=" * 60)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"URL: http://localhost:{port}")
    print(f"Docs: http://localhost:{port}/docs")
    print("=" * 60)
    
    uvicorn.run(
        "ai_engine.api:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

# Made with Bob
