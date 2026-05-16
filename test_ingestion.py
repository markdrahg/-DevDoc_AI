
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from ingestion.github_ingestion import GitHubIngestion
from ingestion.zip_handler import ZipHandler
from ingestion.file_parser import FileParser

from processing.chunkers import Chunker
from processing.embeddings import EmbeddingGenerator


# -------------------------------
# CONFIG
# -------------------------------
REPO_URL = "https://github.com/fastapi/fastapi"
ZIP_PATH = "sample_project.zip"

SUPPORTED_EXTENSIONS = (".py", ".js", ".ts", ".md", ".txt", ".json")


# -------------------------------
# STEP 1: INGESTION
# -------------------------------
def run_ingestion():
    print("\n--- INGESTION START ---\n")

    parser = FileParser()
    processed_files = {}

    # 🔹 GitHub repo
    repo_ingestion = GitHubIngestion(REPO_URL)
    repo_path = repo_ingestion.clone_repository()

    # 🔹 ZIP (optional)
    zip_path = None
    if os.path.exists(ZIP_PATH):
        zip_handler = ZipHandler(ZIP_PATH)
        zip_path = zip_handler.extract_zip()

    # 🔹 collect all paths
    paths_to_scan = [repo_path]
    if zip_path:
        paths_to_scan.append(zip_path)

    # 🔹 scan files
    for base_path in paths_to_scan:
        for root, dirs, files in os.walk(base_path):

            # ignore heavy folders
            dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__")]

            for file in files:
                if not file.endswith(SUPPORTED_EXTENSIONS):
                    continue

                file_path = os.path.join(root, file)

                content = parser.parse_file(file_path)

                # skip invalid files
                if content is None or content.strip() == "":
                    continue

                processed_files[file_path] = {
                    "content": content
                }

    print(f"\n Processed {len(processed_files)} files\n")
    return processed_files


# -------------------------------
# STEP 2: PROCESSING
# -------------------------------
def run_processing(files_dict):
    print("\n--- PROCESSING START ---\n")

    chunker = Chunker()
    chunks = chunker.chunk_files(files_dict)

    print(f" Total chunks created: {len(chunks)}")

    # show sample
    print("\nSample chunk:")
    print(chunks[0])

    # embeddings
    embedder = EmbeddingGenerator()
    chunks = embedder.generate_embeddings(chunks)

    print(f"\n Embedding size: {len(chunks[0]['embedding'])}")

    return chunks


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    # ingestion
    files = run_ingestion()

    # processing
    chunks = run_processing(files)

    print("\n Pipeline working successfully!")