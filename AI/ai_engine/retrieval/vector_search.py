from typing import List, Dict
import numpy as np


class VectorSearch:

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.chunks: List[Dict] = []
        self.embeddings: np.ndarray = np.array([])

    def load_chunks(self, chunks: List[Dict]):
        self.chunks = chunks
        self.embeddings = np.array([c["embedding"] for c in chunks])

    def search(self, query: str, top_k: int = 5) -> List[Dict]:

        # safety check
        if not self.chunks or self.embeddings.size == 0:
            return []

        query_vec = self.embedding_model.encode(query)

        scores = np.dot(self.embeddings, query_vec) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_vec)
        )

        top_indices = np.argsort(scores)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            chunk = self.chunks[idx]

            results.append({
                "content": chunk["content"],
                "file_path": chunk["file_path"],
                "chunk_type": chunk.get("chunk_type", "unknown"),
                "score": float(scores[idx])
            })

        return results