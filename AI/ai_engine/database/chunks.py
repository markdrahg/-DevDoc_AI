from ai_engine.database.models import Chunk
import json

class ChunkRepository:

    def __init__(self, db):
        self.db = db

    def create(self, repo_id, document_id, content, embedding):

        if embedding is None:
            emb = None
        elif hasattr(embedding, "tolist"):
            emb = embedding.tolist()
        else:
            emb = embedding

        chunk = Chunk(
            repo_id=repo_id,
            document_id=document_id,
            content=content,
            embedding=json.dumps(emb) if emb is not None else None
        )

        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)

        return chunk

    def get_by_repo(self, repo_id):
        return (
            self.db.query(Chunk)
            .filter(Chunk.repo_id == repo_id)
            .all()
        )