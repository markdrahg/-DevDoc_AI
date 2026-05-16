from typing import List, Dict


class HybridSearch:

    def __init__(self, vector_search):
        self.vector_search = vector_search

    def keyword_score(self, query: str, text: str) -> int:
        query_words = query.lower().split()
        text = text.lower()

        return sum(word in text for word in query_words)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:

        #  1. Get more candidates
        chunks = self.vector_search.search(query, top_k=top_k * 2)

        if not chunks:
            return []

        #  2. Add keyword score
        for chunk in chunks:
            chunk["keyword_score"] = self.keyword_score(query, chunk["content"])

        #  3. Proper ranking
        # Higher similarity + higher keyword score = better
        ranked = sorted(
            chunks,
            key=lambda x: (x["score"], x["keyword_score"]),
            reverse=True
        )

        return ranked[:top_k]