import zipfile
import os
import shutil

SUPPORTED_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c",
    ".md",
    ".txt",
    ".json",
    ".pdf"
)

class ZipHandler:

    def __init__(self, zip_path, extract_to="workspace/uploaded_zip"):
        self.zip_path = zip_path
        self.extract_to = extract_to

    def _clean_workspace(self):
        if os.path.exists(self.extract_to):
            shutil.rmtree(self.extract_to)

    # ✅ MAIN METHOD (used by ingestion_manager)
    def extract(self):
        self._clean_workspace()

        os.makedirs(self.extract_to, exist_ok=True)

        with zipfile.ZipFile(self.zip_path, "r") as zip_ref:
            zip_ref.extractall(self.extract_to)

        print("📦 ZIP extracted successfully")

        return self.extract_to

    # ✅ OPTIONAL (if you want filtered files later)
    def get_supported_files(self):
        collected_files = []

        for root, dirs, files in os.walk(self.extract_to):
            for file in files:
                if file.endswith(SUPPORTED_EXTENSIONS):
                    full_path = os.path.join(root, file)
                    collected_files.append(full_path)

        return collected_files