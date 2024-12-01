from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, )
from pathlib import Path

from GUI.homepage import HomePage
from GUI.pdf_viewer import PDFViewer


class PDFEditorMainWindow(QMainWindow):
    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.setWindowTitle("PDF Editor")
        self.setGeometry(100, 100, 800, 600)
        self.displayed_file = ""
        self._files_to_delete: list[str] = []
        self.app = app
        self.barmenu = self.menuBar()
        # Import différé pour éviter les imports circulaires
        from GUI.tool_view import ToolView
        self._tool_view = ToolView(self)
        self.pdf_viewer = PDFViewer()
        # Barre de menu et d'outils
        from GUI.topbar import TopBar
        self.topbar = TopBar(self)

        # Zone de contenu principale
        self.content_area = QStackedWidget()
        self.setCentralWidget(self.content_area)

        # Ajout des différentes vues
        self.content_area.addWidget(HomePage())
        self.content_area.addWidget(self._tool_view)
        self.content_area.addWidget(self.pdf_viewer)

    def closeEvent(self, event) -> None:
        # supprimer les fichiers renommés par l'utilisateur pour éviter de garder
        # des fichiers inutiles
        for file in self._files_to_delete:
            file_path = Path(file)
            file_path.unlink()
        event.accept()

    ################################# Slots #################################

    @Slot(int)
    def display_tool_view(self, tool_index: int) -> None:
        self.content_area.setCurrentIndex(1)
        self._tool_view.tool_index = tool_index
        self._tool_view.treat_pdfs()

    @Slot(str)
    def display_pdf(self, pdf_file: str) -> None:
        self.displayed_file = pdf_file
        self.content_area.setCurrentIndex(2)
        self.pdf_viewer.display_pdf(pdf_file)
