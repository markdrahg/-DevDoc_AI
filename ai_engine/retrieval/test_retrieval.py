from ai_engine.retrieval.vector_search import VectorSearch
from ai_engine.retrieval.hybrid_search import HybridSearch
from ai_engine.retrieval.context_builder import ContextBuilder
from sentence_transformers import SentenceTransformer

#  Load SAME embedding model used in processing
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

#  Initialize components
vector = VectorSearch(embedding_model)
retriever = HybridSearch(vector)
builder = ContextBuilder()

#  Test query
query = "authentication logic"

#  Run retrieval
chunks = retriever.search(query)

#  Build context
context = builder.build(chunks)

# Print results
print("\n--- RETRIEVED CONTEXT ---\n")
print(context)