import os
import fitz  # for PDFs

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

class FileParser:

    def __init__(self):
        pass

    def parse_file(self, file_path):
        """
        Parse different file types safely
        """

        try:
            # 🔥 FILE SIZE LIMIT
            if os.path.getsize(file_path) > MAX_FILE_SIZE:
                print(f"Skipping large file: {file_path}")
                return None

            # 🧠 HANDLE PDF
            if file_path.endswith(".pdf"):
                return self._parse_pdf(file_path)

            # 🧠 HANDLE TEXT/CODE FILES
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            return content

        except Exception as e:
            # 🔥 ERROR HANDLING
            print(f"Error parsing {file_path}: {e}")
            return None

    def _parse_pdf(self, file_path):
        try:
            doc = fitz.open(file_path)
            text = ""

            for page in doc:
                text += str(page.get_text())

            return text

        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return None