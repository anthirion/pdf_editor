from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QStackedWidget, QHBoxLayout,
)
from PySide6.QtCore import Slot

from GUI.menubar import MenuBar
from GUI.homepage import HomePage
from GUI.pdf_merger_view import PDFMergerView
from GUI.pdf_splitter_view import PDFSplitterView
from GUI.pdf_to_jpg_view import PDFToJPGView
from GUI.jpg_to_pdf_view import JPGToPDFView
from GUI.pdf_viewer import PDFViewer
import global_variables as GV


class PDFEditorMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):

        # Barre de menu
        menubar = MenuBar(self)
        self.setMenuBar(menubar)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Zone de contenu principale
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)

        # Ajout des différentes vues
        self.content_area.addWidget(HomePage(self))
        self.content_area.addWidget(PDFMergerView(self))
        self.content_area.addWidget(PDFSplitterView(self))
        self.content_area.addWidget(PDFToJPGView(self))
        self.content_area.addWidget(JPGToPDFView(self))
        self._pdf_viewer = PDFViewer(self)
        self.content_area.addWidget(self._pdf_viewer)

################################# Slots #################################

    @Slot(int)
    def change_view(self, view_index):
        self.content_area.setCurrentIndex(view_index)

    @Slot(str)
    def display_pdf(self, pdf_file_path: str):
        self._pdf_viewer.display_pdf(pdf_file_path)
        self.content_area.setCurrentIndex(GV.ViewConstants.ReaderView)
