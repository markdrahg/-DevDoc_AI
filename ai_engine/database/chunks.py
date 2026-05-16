from .models import Chunk
from .repositories import BaseRepository
import json

class ChunkRepository(BaseRepository):

    def create(self, document_id, content, embedding):
        chunk = Chunk(
            document_id=document_id,
            content=content,
            embedding=json.dumps(embedding.tolist())
        )
        return self.add(chunk)

    def get_all_chunks(self):
        return self.db.query(Chunk).all()