"""
Quick integration test script
Tests that backend starts and frontend can connect
"""

import subprocess
import time
import requests
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def test_backend_health():
    """Test if backend health endpoint responds"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend health check passed!")
            print(f"   Status: {data.get('status')}")
            print(f"   Version: {data.get('version')}")
            print(f"   AI Engine: {data.get('ai_engine_status')}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running on http://localhost:8000?")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints"""
    base_url = "http://localhost:8000"
    
    tests = [
        ("GET", "/", "API Info"),
        ("GET", "/health", "Health Check"),
    ]
    
    print("\n🧪 Testing API Endpoints:")
    all_passed = True
    
    for method, endpoint, name in tests:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.request(method, url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {name}: {endpoint}")
            else:
                print(f"   ❌ {name}: {endpoint} (Status: {response.status_code})")
                all_passed = False
        except Exception as e:
            print(f"   ❌ {name}: {endpoint} (Error: {e})")
            all_passed = False
    
    return all_passed

def check_frontend_env():
    """Check if frontend .env file exists and is configured"""
    env_file = Path("frontend/.env")
    if env_file.exists():
        content = env_file.read_text()
        if "VITE_API_BASE_URL=http://localhost:8000" in content:
            print("✅ Frontend .env configured correctly")
            return True
        else:
            print("⚠️  Frontend .env exists but may not be configured correctly")
            return False
    else:
        print("❌ Frontend .env file not found")
        return False

def check_api_service():
    """Check if frontend API service exists"""
    api_file = Path("frontend/src/services/api.ts")
    if api_file.exists():
        print("✅ Frontend API service (api.ts) exists")
        return True
    else:
        print("❌ Frontend API service not found")
        return False

def main():
    print("=" * 60)
    print("DevDoc AI Integration Test")
    print("=" * 60)
    
    # Check frontend files
    print("\nChecking Frontend Files:")
    frontend_ok = check_frontend_env() and check_api_service()
    
    # Test backend
    print("\nTesting Backend Connection:")
    backend_ok = test_backend_health()
    
    if backend_ok:
        endpoints_ok = test_api_endpoints()
    else:
        endpoints_ok = False
        print("\nSkipping endpoint tests (backend not running)")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    print(f"Frontend Configuration: {'PASS' if frontend_ok else 'FAIL'}")
    print(f"Backend Connection: {'PASS' if backend_ok else 'FAIL'}")
    print(f"API Endpoints: {'PASS' if endpoints_ok else 'FAIL' if backend_ok else 'SKIPPED'}")
    
    if frontend_ok and backend_ok and endpoints_ok:
        print("\nAll tests passed! Frontend and backend are ready to communicate.")
        print("\nNext steps:")
        print("   1. Start backend: cd backend && uvicorn app.main:app --reload")
        print("   2. Start frontend: cd frontend && npm run dev")
        print("   3. Open browser: http://localhost:5173")
        return 0
    else:
        print("\nSome tests failed. Please check the errors above.")
        if not backend_ok:
            print("\nTo start the backend:")
            print("   cd backend")
            print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return 1

if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
