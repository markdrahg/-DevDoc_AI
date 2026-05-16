"""
Test script for the documentation generation system.
Tests the DocumentationGenerator with sample code chunks.
"""

import os
import sys
from typing import Dict, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from documentation.doc_generator import DocumentationGenerator
from rag.granite_client import GraniteClient


def create_sample_chunks() -> List[Dict]:
    """Create sample code chunks for testing."""
    
    sample_code_1 = """
import os
from typing import List, Dict

class DataProcessor:
    '''Process and transform data.'''
    
    def __init__(self, config: Dict):
        self.config = config
        self.data = []
    
    def load_data(self, file_path: str) -> None:
        '''Load data from file.'''
        with open(file_path, 'r') as f:
            self.data = f.readlines()
    
    def process(self) -> List[str]:
        '''Process loaded data.'''
        return [line.strip() for line in self.data]

def validate_input(data: str) -> bool:
    '''Validate input data format.'''
    return len(data) > 0 and data.isalnum()
"""

    sample_code_2 = """
from typing import Optional
import json

def parse_config(config_path: str) -> Optional[Dict]:
    '''Parse JSON configuration file.'''
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_results(results: List, output_path: str) -> bool:
    '''Save processing results to file.'''
    try:
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        return True
    except Exception:
        return False
"""

    chunks = [
        {
            "file_path": "src/data_processor.py",
            "content": sample_code_1,
            "metadata": {"language": "python", "type": "module"}
        },
        {
            "file_path": "src/utils/config_parser.py",
            "content": sample_code_2,
            "metadata": {"language": "python", "type": "utility"}
        }
    ]
    
    return chunks


def test_documentation_generation():
    """Test the complete documentation generation workflow."""
    
    print("=" * 80)
    print("DOCUMENTATION GENERATION SYSTEM TEST")
    print("=" * 80)
    print()
    
    # Step 1: Initialize LLM client
    print("Step 1: Initializing Granite LLM client...")
    try:
        llm = GraniteClient()
        print("✓ LLM client initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize LLM client: {e}")
        print("\nMake sure .env file contains:")
        print("  - IBM_API_KEY")
        print("  - IBM_URL")
        print("  - IBM_PROJECT_ID")
        return
    print()
    
    # Step 2: Initialize DocumentationGenerator
    print("Step 2: Initializing DocumentationGenerator...")
    try:
        doc_gen = DocumentationGenerator(llm)
        print("✓ DocumentationGenerator initialized successfully")
        print(f"✓ Template loaded from: documentation/templates/doc_template.md")
    except Exception as e:
        print(f"✗ Failed to initialize DocumentationGenerator: {e}")
        return
    print()
    
    # Step 3: Create sample chunks
    print("Step 3: Creating sample code chunks...")
    chunks = create_sample_chunks()
    print(f"✓ Created {len(chunks)} sample code chunks")
    for i, chunk in enumerate(chunks, 1):
        print(f"  - Chunk {i}: {chunk['file_path']} ({len(chunk['content'])} chars)")
    print()
    
    # Step 4: Generate documentation for first chunk
    print("Step 4: Generating documentation for first chunk...")
    print("-" * 80)
    try:
        doc = doc_gen.generate_for_chunk(chunks[0])
        print("✓ Documentation generated successfully!")
        print()
        print("Generated Documentation:")
        print("-" * 80)
        print(doc)
        print("-" * 80)
    except Exception as e:
        print(f"✗ Failed to generate documentation: {e}")
        import traceback
        traceback.print_exc()
        return
    print()
    
    # Step 5: Generate documentation for all chunks
    print("Step 5: Generating documentation for all chunks...")
    try:
        all_docs = doc_gen.generate(chunks)
        print(f"✓ Generated documentation for {len(chunks)} chunks")
        
        # Save to file
        output_path = "test_generated_docs.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(all_docs)
        print(f"✓ Documentation saved to: {output_path}")
    except Exception as e:
        print(f"✗ Failed to generate all documentation: {e}")
        import traceback
        traceback.print_exc()
        return
    print()
    
    # Step 6: Verify template placeholders
    print("Step 6: Verifying template structure...")
    template_path = "documentation/templates/doc_template.md"
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    
    required_placeholders = [
        "{file_name}",
        "{brief_description}",
        "{file_path}",
        "{responsibilities_list}",
        "{classes_section}",
        "{functions_section}",
        "{code_example}",
        "{dependencies_list}",
        "{usage_example}",
        "{related_files_list}",
        "{summary_text}",
        "{language}"
    ]
    
    missing_placeholders = []
    for placeholder in required_placeholders:
        if placeholder not in template_content:
            missing_placeholders.append(placeholder)
    
    if missing_placeholders:
        print(f"✗ Missing placeholders in template: {missing_placeholders}")
    else:
        print(f"✓ All {len(required_placeholders)} required placeholders found in template")
    print()
    
    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print("✓ LLM client initialization: PASSED")
    print("✓ DocumentationGenerator initialization: PASSED")
    print("✓ Sample chunk creation: PASSED")
    print("✓ Single chunk documentation: PASSED")
    print("✓ Multiple chunks documentation: PASSED")
    print("✓ Template verification: PASSED" if not missing_placeholders else "✗ Template verification: FAILED")
    print()
    print(f"Output file: {output_path}")
    print("=" * 80)


if __name__ == "__main__":
    test_documentation_generation()

# Made with Bob
