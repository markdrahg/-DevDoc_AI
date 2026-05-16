# test_processing.py
from typing import Any

from processing.chunkers import Chunker
from processing.embeddings import EmbeddingGenerator

# ---------------- SAMPLE FILES ----------------

files = [
    {
        "file_path": "auth.py",
        "content": """
def login(user):
    return True

class AuthService:
    pass
""" * 20
    },

    {
        "file_path": "utils.py",
        "content": """
def helper():
    return "hello"
""" * 20
    }
]
# ---------------- CHUNKING TEST ----------------

chunker = Chunker()

chunks = chunker.chunk_files(files)

print("\nTotal chunks created:")
print(len(chunks))


print("\nSample chunk:\n")

print(chunks[0])

# ---------------- EMBEDDING TEST ----------------

embedder = EmbeddingGenerator()

chunks_with_embeddings = embedder.generate_embeddings(chunks)

print("\nEmbedding vector length:")

print(len(chunks_with_embeddings[0]["embedding"]))


print("\nEmbedding generated successfully.")