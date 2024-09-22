from PySide6.QtWidgets import QMainWindow
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument


class PDFViewer(QMainWindow):
    def __init__(self, parent=None, pdf_file_path: str = ""):
        super().__init__(parent)
        self.setWindowTitle("PDF Editor - Lecture")
        self._pdf_file_path = pdf_file_path
        self.pdf_view = QPdfView()
        # Permet l'affichage de toutes les pages du fichier pdf
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_doc = QPdfDocument()
        self.setCentralWidget(self.pdf_view)

    def display_pdf(self, pdf_file_path: str):
        self._pdf_file_path = pdf_file_path
        self.pdf_doc.load(self._pdf_file_path)
        self.pdf_view.setDocument(self.pdf_doc)
