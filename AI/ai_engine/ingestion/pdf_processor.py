import fitz

class PDFProcessor:

    def __init__(self, pdf_path) -> None:
        self.pdf_path = pdf_path

    def extract_text(self) -> str:
        document = fitz.open(filename=self.pdf_path)
        full_text = ""

        for page in document:
            text = str(page.get_text())
            full_text += text

        return full_text