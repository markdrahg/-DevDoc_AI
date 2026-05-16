import os

from ai_engine.ingestion.github_ingestion import GitHubIngestion
from ai_engine.ingestion.zip_handler import ZipHandler
from ai_engine.ingestion.pdf_processor import PDFProcessor
from ai_engine.ingestion.file_parser import FileParser

# 🔥 NEW
from shared.utils import log, clean_path


class IngestionManager:

    def __init__(self):
        self.parser = FileParser()

    def ingest(self, source: str):
        if source.startswith("http"):
            log("🌐 GitHub repo detected...")
            return self._handle_repo(source)

        elif source.endswith(".zip"):
            log("📦 ZIP detected...")
            return self._handle_zip(source)

        elif source.endswith(".pdf"):
            log("📄 PDF detected...")
            return self._handle_pdf(source)

        else:
            log("📁 Local folder detected...")
            return self._handle_local(source)

    # ---------------------

    def _handle_repo(self, url):
        repo = GitHubIngestion(repo_url=url)
        path = repo.clone_repository()
        return self._read_folder(path)

    def _handle_zip(self, zip_path):
        handler = ZipHandler(zip_path)
        extract_path = handler.extract()
        return self._read_folder(extract_path)

    def _handle_pdf(self, pdf_path):
        processor = PDFProcessor(pdf_path)
        text = processor.extract_text()

        return [{
            "file_path": clean_path(pdf_path),  # ✅ applied
            "content": text
        }]

    def _handle_local(self, path):
        return self._read_folder(path)

    # ---------------------

    def _read_folder(self, folder_path):
        files = []

        folder_path = clean_path(folder_path)  # ✅ applied
        log(f"🔍 Scanning: {folder_path}")

        for root, dirs, filenames in os.walk(folder_path):

            dirs[:] = [d for d in dirs if d not in (
                ".git", "__pycache__", "node_modules", "docs"
            )]

            for f in filenames:
                path = os.path.join(root, f)
                path = clean_path(path)  # ✅ applied

                result = self.parser.parse_file(path)

                if result:
                    files.append(result)

        log(f"✅ Loaded {len(files)} files")
        return files