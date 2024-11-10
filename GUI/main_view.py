from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QStackedWidget, QHBoxLayout,
)
from PySide6.QtCore import Slot

from GUI.topbar import TopBar
from GUI.homepage import HomePage
from GUI.tool_view import ToolView
from GUI.pdf_viewer import PDFViewer


class PDFEditorMainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("PDF Editor")
        self.setGeometry(100, 100, 800, 600)
        self._app = app
        self._tool_view = ToolView(self)
        self._pdf_viewer = PDFViewer(self)
        # Barre de menu et d'outils
        self._topbar = TopBar(self)
        self.init_ui()

    def init_ui(self):

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Zone de contenu principale
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)

        # Ajout des différentes vues
        self.content_area.addWidget(HomePage(self))
        self.content_area.addWidget(self._tool_view)
        self.content_area.addWidget(self._pdf_viewer)

################################# Slots #################################

    @Slot(int)
    def display_tool_view(self, tool_index: int) -> None:
        self.content_area.setCurrentIndex(1)
        self._tool_view.tool_index = tool_index
        self._tool_view.treat_pdfs()

    @Slot(str)
    def display_pdf(self, pdf_file_path: str) -> None:
        self.content_area.setCurrentIndex(2)
        self._pdf_viewer.display_pdf(pdf_file_path)
