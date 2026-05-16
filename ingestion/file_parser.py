import os
from ingestion.pdf_processor import PDFProcessor


class FileParser:

    def __init__(self):
        pass

    def parse_file(self, file_path):

        try:

            if file_path.endswith(".pdf"):

                pdf_processor = PDFProcessor(file_path)

                return pdf_processor.extract_text()

            else:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as file:

                    return file.read()

        except Exception as error:

            print(f"Error parsing file: {file_path}")
            print(error)

            return ""