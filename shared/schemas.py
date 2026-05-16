from typing import List, Optional


class DocumentSchema:
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.content = content


class ChunkSchema:
    def __init__(
        self,
        file_path: str,
        content: str,
        embedding: Optional[List[float]] = None
    ):
        self.file_path = file_path
        self.content = content
        self.embedding = embedding