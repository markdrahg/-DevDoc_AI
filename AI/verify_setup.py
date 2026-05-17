"""
Setup Verification Script
Checks if all AI Engine dependencies are installed correctly
"""

import sys

def check_import(module_name, package_name=None):
    """Try to import a module and report status"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name} - MISSING")
        print(f"   Error: {e}")
        return False

def main():
    print("=" * 60)
    print("AI Engine Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("ibm_watsonx_ai", "IBM watsonx.ai SDK"),
        ("sentence_transformers", "SentenceTransformers"),
        ("torch", "PyTorch"),
        ("fitz", "PyMuPDF"),
        ("git", "GitPython"),
        ("dotenv", "python-dotenv"),
        ("numpy", "NumPy"),
        ("sqlalchemy", "SQLAlchemy"),
        ("tqdm", "tqdm"),
        ("colorama", "colorama"),
    ]
    
    results = []
    for module, name in checks:
        results.append(check_import(module, name))
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print()
        print("🎉 All dependencies installed successfully!")
        print()
        print("Next steps:")
        print("1. Configure IBM credentials in AI/.env")
        print("2. Run: python start_ai_engine.py")
        return 0
    else:
        print()
        print("⚠️  Some dependencies are missing.")
        print("Run: pip install -r ai_engine/requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
