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

        all_chunks = []

        for file_data in files_dict:

            file_path = file_data["file_path"]

            content = file_data["content"]

            # metadata
            meta = self.meta_extractor.extract(
                file_path,
                content
            )

            # analysis
            analysis = self.analyzer.analyze(content)

            text_chunks = self.chunk_text(content)

            for idx, chunk in enumerate(text_chunks):

                all_chunks.append({

                    "file_path": file_path,

                    "content": chunk,

                    "chunk_index": idx,

                    "language": meta["language"],

                    "line_count": meta["line_count"],

                    "chunk_type": self.analyzer.detect_chunk_type(chunk),

                    "functions": analysis["functions"],

                    "classes": analysis["classes"]
                })

        return all_chunks