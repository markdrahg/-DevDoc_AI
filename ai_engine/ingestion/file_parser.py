import os
import fitz  # pip install pymupdf

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

SKIP_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".exe", ".dll")


class FileParser:

    def parse_file(self, file_path):
        try:
            if file_path.endswith(SKIP_EXTENSIONS):
                return None

            if os.path.getsize(file_path) > MAX_FILE_SIZE:
                return None

            # PDF
            if file_path.endswith(".pdf"):
                content = self._parse_pdf(file_path)
            else:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

            if not content:
                return None

            return {
                "file_path": file_path,
                "content": content
            }

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def _parse_pdf(self, file_path):
        import fitz
    
        doc = fitz.open(file_path)
        text = ""
    
        for page in doc:
            text += str(page.get_text())
    
        return text