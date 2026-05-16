from .models import Document
from .repositories import BaseRepository


class DocumentRepository(BaseRepository):

    def create(self, file_path, content):
        existing = self.get_by_path(file_path)
        if existing:
            return existing

        doc = Document(file_path=file_path, content=content)
        return self.add(doc)

    def get_by_path(self, file_path):
        return self.db.query(Document).filter_by(file_path=file_path).first()

    def get_all_docs(self):
        return self.db.query(Document).all()