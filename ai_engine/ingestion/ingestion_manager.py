import os

from ai_engine.ingestion.github_ingestion import GitHubIngestion
from ai_engine.ingestion.zip_handler import ZipHandler
from ai_engine.ingestion.pdf_processor import PDFProcessor
from ai_engine.ingestion.file_parser import FileParser

from shared.utils import log, clean_path


def resolve_path(path: str) -> str:
    path = path.strip().strip('"')

    if os.path.isabs(path) and os.path.exists(path):
        return path

    cwd_path = os.path.join(os.getcwd(), path)
    if os.path.exists(cwd_path):
        return cwd_path

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    # ✅ project root
    project_path = os.path.join(base_dir, path)
    if os.path.exists(project_path):
        return project_path

    # 🔥 ADD THIS (ai_engine folder)
    ai_engine_path = os.path.join(base_dir, "ai_engine", path)
    if os.path.exists(ai_engine_path):
        return ai_engine_path

    # workspace
    workspace_path = os.path.join(base_dir, "workspace", path)
    if os.path.exists(workspace_path):
        return workspace_path

    return path

class IngestionManager:
    def __init__(self):
        self.parser = FileParser()

    # ---------------------

    def ingest(self, source: str):
        source = resolve_path(source)

        if source.startswith("http"):
            log("🌐 GitHub repo detected...")
            return self._handle_repo(source)

        elif source.lower().endswith(".zip"):
            if not os.path.exists(source):
                log(f"❌ ZIP not found: {source}")
                return []
            log("📦 ZIP detected...")
            return self._handle_zip(source)

        elif source.lower().endswith(".pdf"):
            if not os.path.exists(source):
                log(f"❌ PDF not found: {source}")
                return []
            log("📄 PDF detected...")
            return self._handle_pdf(source)

        else:
            if not os.path.exists(source):
                log(f"❌ Folder not found: {source}")
                return []
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
            "file_path": clean_path(pdf_path),
            "content": text
        }]

    def _handle_local(self, path):
        return self._read_folder(path)

    # ---------------------

    def _read_folder(self, folder_path):
        files = []

        folder_path = clean_path(folder_path)
        log(f"🔍 Scanning: {folder_path}")

        IMPORTANT_EXTENSIONS = (
            ".py", ".js", ".ts", ".java",
            ".md", ".txt", ".json", ".yaml", ".yml"
        )

        MAX_FILE_SIZE = 2_000_000   # 2MB
        MAX_JSON_SIZE = 200_000     # 200KB

        for root, dirs, filenames in os.walk(folder_path):

            dirs[:] = [d for d in dirs if d not in (
                ".git", "__pycache__", "node_modules",
                "docs", "dist", "build"
            )]

            for filename in filenames:
                path = clean_path(os.path.join(root, filename))
                path_lower = path.lower()

                if not path_lower.endswith(IMPORTANT_EXTENSIONS):
                    continue

                try:
                    size = os.path.getsize(path)
                except OSError:
                    continue

                if path_lower.endswith(".json") and size > MAX_JSON_SIZE:
                    continue

                if size > MAX_FILE_SIZE:
                    continue

                result = self.parser.parse_file(path)

                if result:
                    files.append(result)

        log(f"✅ Loaded {len(files)} valid files")
        return files