"""
Comprehensive System Test - 3 Loop Test
Tests all major features of the repo-intelligence system
"""
import os
import sys
import json
from pathlib import Path

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ai_engine.rag_cli import (
    run_pipeline, 
    ask_question, 
    generate_docs, 
    get_health,
    load_from_db
)

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_loop(loop_num, test_source):
    """Run a complete test loop"""
    print_section(f"LOOP {loop_num} - Testing with: {test_source}")
    
    try:
        # Test 1: Data Ingestion & Processing
        print("\n[1/5] Testing Data Ingestion & Processing...")
        chunks, repo_id = run_pipeline(test_source)
        
        if not chunks:
            print("❌ FAILED: No chunks generated")
            return False
        
        print(f"✅ SUCCESS: Generated {len(chunks)} chunks")
        print(f"✅ Repo ID: {repo_id}")
        
        # Test 2: Database Storage & Retrieval
        print("\n[2/5] Testing Database Storage & Retrieval...")
        loaded_chunks = load_from_db(repo_id)
        
        if not loaded_chunks:
            print("❌ FAILED: Could not load chunks from database")
            return False
        
        print(f"✅ SUCCESS: Loaded {len(loaded_chunks)} chunks from DB")
        
        # Test 3: RAG Query System
        print("\n[3/5] Testing RAG Query System...")
        test_queries = [
            "What does this project do?",
            "What are the main files?",
            "Explain the code structure"
        ]
        
        for query in test_queries:
            result = ask_question(query, loaded_chunks)
            
            if not result or "answer" not in result:
                print(f"❌ FAILED: Query failed for '{query}'")
                return False
            
            print(f"✅ Query: {query}")
            print(f"   Answer: {result['answer'][:100]}...")
        
        # Test 4: Documentation Generation
        print("\n[4/5] Testing Documentation Generation...")
        docs = generate_docs(loaded_chunks[:3])  # Test with first 3 chunks
        
        if not docs:
            print("❌ FAILED: Documentation generation failed")
            return False
        
        print(f"✅ SUCCESS: Generated {len(docs)} characters of documentation")
        
        # Test 5: Health Scoring
        print("\n[5/5] Testing Health Scoring...")
        health = get_health(loaded_chunks)
        
        if not health or "score" not in health:
            print("❌ FAILED: Health scoring failed")
            return False
        
        print(f"✅ SUCCESS: Health Score: {health['score']}")
        print(f"   Coverage: {health['coverage']}%")
        print(f"   Comments: {health['comments']}%")
        
        print(f"\n🎉 LOOP {loop_num} COMPLETED SUCCESSFULLY!")
        return True
        
    except Exception as e:
        print(f"\n❌ LOOP {loop_num} FAILED WITH ERROR:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print_section("COMPREHENSIVE SYSTEM TEST - 3 LOOPS")
    print("Testing all features across multiple iterations")
    
    # Test sources for each loop
    test_sources = [
        "test_repo",           # Loop 1: Local folder
        "test_repo",           # Loop 2: Same folder (test caching/reprocessing)
        "ai_engine/database"   # Loop 3: Different folder
    ]
    
    results = []
    
    for i, source in enumerate(test_sources, 1):
        success = test_loop(i, source)
        results.append(success)
        
        if not success:
            print(f"\n⚠️  Loop {i} failed, but continuing with remaining tests...")
    
    # Final Summary
    print_section("FINAL TEST SUMMARY")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    for i, result in enumerate(results, 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  Loop {i}: {status}")
    
    if passed == total:
        print("\n🎊 ALL TESTS PASSED! System is working correctly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review errors above.")
        return 1

if __name__ == "__main__":
    exit(main())

# Made with Bob
