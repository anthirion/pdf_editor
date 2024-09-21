from PySide6.QtWidgets import QMainWindow
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument


class PDFReaderView(QMainWindow):
    def __init__(self, pdf_file_path: str = "/home/thiran/projets_persos/pdf_editor/pdf_examples/attestation_suivi_cours_python.pdf"):
        super().__init__()
        self.setWindowTitle("PDF Editor - Lecture")
        self._pdf_file_path = pdf_file_path
        self.pdf_view = QPdfView()
        self.pdf_doc = QPdfDocument()
        self.setCentralWidget(self.pdf_view)

    def display_pdf(self, pdf_file_path: str):
        self._pdf_file_path = pdf_file_path
        self.pdf_doc.load(self._pdf_file_path)
        self.pdf_view.setDocument(self.pdf_doc)
