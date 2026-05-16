# processing/chunker.py

from processing.metadata_extractor import MetadataExtractor
from processing.code_analyzer import CodeAnalyzer


class Chunker:

    def __init__(self, chunk_size=300, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.meta_extractor = MetadataExtractor()
        self.analyzer = CodeAnalyzer()

    def chunk_text(self, text):
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.overlap

        return chunks

    def chunk_files(self, files_dict):
        """
        files_dict = {
            file_path: {
                "content": ...
            }
        }
        """

        all_chunks = []

        for file_path, file_data in files_dict.items():
            content = file_data["content"]

            # extract metadata (file level)
            meta = self.meta_extractor.extract(file_path, content)

            # analyze code (file level)
            analysis = self.analyzer.analyze(content)

            text_chunks = self.chunk_text(content)

            for idx, chunk in enumerate(text_chunks):
                all_chunks.append({
                    "file_path": file_path,
                    "content": chunk,
                    "chunk_index": idx,

                    #  metadata
                    "language": meta["language"],
                    "line_count": meta["line_count"],

                    #  code awareness
                    "chunk_type": self.analyzer.detect_chunk_type(chunk),
                    "functions": analysis["functions"],
                    "classes": analysis["classes"]
                })

        return all_chunks