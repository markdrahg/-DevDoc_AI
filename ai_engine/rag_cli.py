import os
import pickle
import json

from shared.utils import log

from ai_engine.retrieval.vector_search import VectorSearch
from ai_engine.retrieval.hybrid_search import HybridSearch
from ai_engine.retrieval.context_builder import ContextBuilder

from ai_engine.rag.pipeline import RAGPipeline
from ai_engine.rag.granite_client import GraniteClient

from ai_engine.processing.chunkers import Chunker
from ai_engine.processing.embeddings import EmbeddingGenerator

from ai_engine.ingestion.ingestion_manager import IngestionManager

from ai_engine.documentation.doc_generator import DocumentationGenerator
from ai_engine.documentation.health_scorer import DocumentationHealthScorer

from ai_engine.database import init_db
from ai_engine.database.db import SessionLocal
from ai_engine.database.documents import DocumentRepository
from ai_engine.database.chunks import ChunkRepository

from ai_engine.save_docs import save_docs
from sentence_transformers import SentenceTransformer


# ✅ cache folder
def get_cache_file(source):
    os.makedirs("cache", exist_ok=True)
    safe = source.replace("\\", "_").replace(":", "").replace("/", "_")
    return f"cache/{safe}.pkl"


def load_data(source):
    cache_file = get_cache_file(source)

    if os.path.exists(cache_file):
        log("⚡ Loading cached data...")
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    log("⚙️ Processing data...")

    manager = IngestionManager()
    files = manager.ingest(source)

    if not files:
        log("❌ No files found")
        return []

    init_db()
    db = SessionLocal()

    doc_repo = DocumentRepository(db)
    chunk_repo = ChunkRepository(db)

    chunker = Chunker()
    chunks = chunker.chunk_files(files)

    embedder = EmbeddingGenerator()
    chunks = embedder.generate_embeddings(chunks)

    log("💾 Storing in DB...")

    for chunk in chunks:
        doc = doc_repo.create(chunk["file_path"], chunk["content"])
        chunk_repo.create(doc.id, chunk["content"], chunk.get("embedding"))

    log("✅ Stored in DB")

    with open(cache_file, "wb") as f:
        pickle.dump(chunks, f)

    return chunks


def load_from_db():
    log("📦 Loading from DB...")

    db = SessionLocal()
    chunk_repo = ChunkRepository(db)

    db_chunks = chunk_repo.get_all_chunks()

    chunks = []

    for c in db_chunks:
        chunks.append({
            "file_path": c.document.file_path if hasattr(c, "document") else str(c.document_id),
            "content": c.content,
            "embedding": json.loads(c.embedding) if c.embedding else None
        })

    log(f"✅ Loaded {len(chunks)} chunks")
    return chunks


def main():
    log("🚀 DevDoc AI READY\n")

    source = input("Enter repo / zip / pdf / folder: ").strip()

    chunks = load_data(source)

    if not chunks:
        log("❌ Nothing to process")
        return

    chunks = load_from_db()

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    vector = VectorSearch(embedding_model)
    vector.load_chunks(chunks)

    retriever = HybridSearch(vector)
    builder = ContextBuilder()
    rag = RAGPipeline(retriever, builder)

    llm = GraniteClient()
    doc_generator = DocumentationGenerator(llm)
    scorer = DocumentationHealthScorer()

    while True:
        print("\n1. Ask (RAG)")
        print("2. Generate Docs")
        print("3. Health")
        print("4. Save Docs")
        print("5. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            query = input("Question: ")
            result = rag.run(query)

            print("\n💡", result["answer"])
            print("\nSources:")
            for s in result["sources"]:
                print("-", s)

        elif choice == "2":
            log("📘 Generating docs...")
            docs = doc_generator.generate(chunks[:5])
            print(docs[:1500])

        elif choice == "3":
            print(scorer.score(chunks))

        elif choice == "4":
            log("💾 Saving docs...")
            save_docs(chunks, doc_generator)

        elif choice == "5":
            log("👋 Exiting...")
            break

        else:
            print("Invalid choice")