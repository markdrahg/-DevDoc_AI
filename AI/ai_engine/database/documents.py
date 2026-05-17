from .models import Document
from .repositories import BaseRepository


class DocumentRepository:
    def __init__(self, db):
        self.db = db

    def create(self, repo_id, file_path, content):
        doc = Document(
            repo_id=repo_id,
            file_path=file_path,
            content=content
        )
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc