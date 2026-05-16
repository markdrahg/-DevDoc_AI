# test_processing.py

from processing.chunkers import Chunker
from processing.embeddings import EmbeddingGenerator

# simulate ingestion output
files = {
    "auth.py": "def login(user): return True\n" * 50,
    "utils.py": "def helper(): pass\n" * 50
}

# step 1: chunking
chunker = Chunker()
chunks = chunker.chunk_files(files)

print("Total chunks:", len(chunks))
print("Sample chunk:", chunks[0])

# step 2: embeddings
embedder = EmbeddingGenerator()
chunks_with_embeddings = embedder.generate_embeddings(chunks)

print("Embedding length:", len(chunks_with_embeddings[0]["embedding"]))