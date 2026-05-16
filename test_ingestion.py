import os
import shutil
from ingestion.github_ingestion import GitHubIngestion
from ingestion.zip_handler import ZipHandler
from ingestion.file_parser import FileParser


class RepositoryManager:

    def __init__(self):

        self.parser = FileParser()

    def process_github_repository(self, repo_url):

        github = GitHubIngestion(repo_url)

        repo_path = github.clone_repository()

        parsed_files = self.collect_repository_content(repo_path)

        return {
            "source": "github",
            "repository_path": repo_path,
            "total_files": len(parsed_files),
            "files": parsed_files
        }

    def process_zip_repository(self, zip_path):

        zip_handler = ZipHandler(zip_path)
        extract_path = zip_handler.extract_zip()

        supported_files = zip_handler.get_supported_files()

        parsed_files = []

        for file in supported_files:

            content = self.parser.parse_file(file)

            parsed_files.append({
                "file_path": file,
                "content": content
            })

        return {
            "source": "zip",
            "extract_path": extract_path,
            "total_files": len(parsed_files),
            "files": parsed_files
        }

    def collect_repository_content(self, repository_path):

        parsed_files = []

        for root, dirs, files in os.walk(repository_path):

            dirs[:] = [
                directory
                for directory in dirs
                if directory not in [
                    ".git",
                    "node_modules",
                    "venv",
                    "__pycache__"
                ]
            ]

            for file in files:

                if file.endswith((
                    ".py",
                    ".js",
                    ".ts",
                    ".java",
                    ".cpp",
                    ".c",
                    ".md",
                    ".txt",
                    ".json"
                )):

                    full_path = os.path.join(root, file)

                    content = self.parser.parse_file(full_path)

                    parsed_files.append({
                        "file_path": full_path,
                        "content": content
                    })

        return parsed_files
    
    

class MetadataExtractor:

    def __init__(self):
        pass

    def extract_repository_metadata(self, repository_path):

        total_files = 0
        total_directories = 0
        programming_languages = {}

        for root, dirs, files in os.walk(repository_path):

            total_directories += len(dirs)

            for file in files:

                total_files += 1

                extension = os.path.splitext(file)[1]

                if extension:

                    programming_languages[extension] = (
                        programming_languages.get(extension, 0) + 1
                    )

        return {
            "repository_path": repository_path,
            "total_files": total_files,
            "total_directories": total_directories,
            "languages": programming_languages
        }
        
        
SUPPORTED_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".swift",
    ".kt",
    ".scala",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".xml",
    ".html",
    ".css",
    ".pdf"
)

IGNORED_DIRECTORIES = [
    ".git",
    "node_modules",
    "venv",
    "dist",
    "build",
    "__pycache__",
    ".next",
    ".idea",
    ".vscode"
]

class WorkspaceManager:

    def __init__(self):

        self.workspace_path = "workspace"
        self.uploads_path = "uploads"

    def create_directories(self):

        os.makedirs(self.workspace_path, exist_ok=True)
        os.makedirs(self.uploads_path, exist_ok=True)

    def clean_directory(self, directory_path):

        if os.path.exists(directory_path):

            shutil.rmtree(directory_path)

            os.makedirs(directory_path, exist_ok=True)
            
            
            
            
# ---------- GITHUB TEST ----------

repo_url = "https://github.com/fastapi/fastapi"

repo_ingestion = GitHubIngestion(repo_url)

repo_path = repo_ingestion.clone_repository()

print(f"Repository stored at: {repo_path}")


# ---------- ZIP TEST ----------

zip_handler = ZipHandler("sample_project.zip")

zip_handler.extract_zip()

files = zip_handler.get_supported_files()

print(f"Found {len(files)} supported files")


# ---------- FILE PARSING TEST ----------

parser = FileParser()

for file in files[:5]:

    print(f"\nProcessing: {file}")

    content = parser.parse_file(file)

    print(content[:300])