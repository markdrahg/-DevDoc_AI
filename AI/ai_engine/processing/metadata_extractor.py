# processing/metadata_extractor.py

import os

class MetadataExtractor:

    def extract(self, file_path, content):
        ext = os.path.splitext(file_path)[1]

        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cpp": "cpp"
        }

        return {
            "file_path": file_path,
            "language": language_map.get(ext, "unknown"),
            "line_count": content.count("\n"),
            "size": len(content)
        }