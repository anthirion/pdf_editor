from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QToolBar, QFileDialog, QMessageBox
from PySide6.QtCore import Signal, Slot

from pathlib import Path

import global_variables as GV


class TopBar(QMenuBar, QToolBar):
    """
    The TopBar class creates a menubar and a topbar
    """
    # Le signal envoie un entier qui indique la vue à afficher :
    # 1 si vue de fusion des pdf (pdf_merger_view)
    # 2 si vue de division des pdf (pdf_splitter_view), etc
    # pour plus de simplicité, les constantes sont définies dans l'enum ViewConstants
    change_view_signal = Signal(int)
    display_pdf_signal = Signal(str)
    search_text = Signal()

    def __init__(self, parent=None):
        # le parent est la plupart du temps la main_view
        super().__init__(parent)
        self._parent_window = parent
        self._current_file_path = ""
        menu = parent.menuBar()
        self.change_view_signal.connect(parent.change_view)
        self.display_pdf_signal.connect(parent.display_pdf)
        self.search_text.connect(parent._pdf_viewer.toggle_search_bar)

        """
        MenuBar
        """
        # Menu Fichier
        self.file_menu = menu.addMenu("Fichier")
        # Sous-menu "Nouveau"
        self.new_action = QAction("Nouveau", self)
        # Sous-menu "Ouvrir"
        self.open_action = QAction("Ouvrir", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file_dialog)
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)

        # Menu Edition
        edition_menu = menu.addMenu("Edition")
        # Sous-menu "Rechercher"
        self.search_action = QAction("Rechercher", self)
        self.search_action.setShortcut("Ctrl+F")
        self.search_action.triggered.connect(self.search_action_selected)
        edition_menu.addAction(self.search_action)

        # Menu Outils
        tools_menu = menu.addMenu("Outils")
        # Sous-menu "Fusionner PDF"
        merge_pdf_action = QAction("Fusionner PDF", self)
        merge_pdf_action.triggered.connect(self.merge_pdf_selected)
        # Sous-menu "Diviser PDF"
        split_pdf_action = QAction("Diviser PDF", self)
        split_pdf_action.triggered.connect(self.split_pdf_selected)
        # Sous-menu "Convertir de PDF vers JPG"
        convert_pdf_to_jpg_action = QAction("Convertir de PDF vers JPG", self)
        convert_pdf_to_jpg_action.triggered.connect(
            self.convert_pdf_to_jpg_selected)
        # Sous-menu "Convertir de JPG vers PDF"
        convert_jpg_to_pdf_action = QAction("Convertir de JPG vers PDF", self)
        convert_jpg_to_pdf_action.triggered.connect(
            self.convert_jpg_to_pdf_selected)

        tools_menu.addAction(merge_pdf_action)
        tools_menu.addAction(split_pdf_action)
        tools_menu.addAction(convert_pdf_to_jpg_action)
        tools_menu.addAction(convert_jpg_to_pdf_action)

        # Menu Aide
        help_menu = menu.addMenu("Aide")
        # Sous-menu "Obtenir de l'aide"
        get_online_help = QAction("Obtenir de l'aide", self)
        help_menu.addAction(get_online_help)

        """
        ToolBar
        """
        toolbar = QToolBar("Barre d'outils", self)
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.search_action)

        parent.addToolBar(toolbar)


################################# Slots #################################


    @ Slot()
    def open_file_dialog(self):
        # Ouvre une boîte de dialogue pour sélectionner un fichier PDF
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier", "", "PDF Files (*.pdf);;All Files (*)")

        if file_path:
            self.display_pdf_signal.emit(file_path)
            last_path_component = Path(file_path).name
            self._parent_window.setWindowTitle(
                "PDF Editor - " + last_path_component)

    @Slot()
    def search_action_selected(self):
        self.search_text.emit()

    @ Slot()
    def merge_pdf_selected(self):
        self._parent_window.setWindowTitle("PDF Editor - Outil de fusion")
        self.change_view_signal.emit(GV.ViewConstants.MergerView)

    @ Slot()
    def split_pdf_selected(self):
        self._parent_window.setWindowTitle("PDF Editor - Outil de division")
        self.change_view_signal.emit(GV.ViewConstants.SplitterView)

    @ Slot()
    def convert_pdf_to_jpg_selected(self):
        self._parent_window.setWindowTitle(
            "PDF Editor - Outil de convertion de PDF vers JPG")
        self.change_view_signal.emit(GV.ViewConstants.PDFtoJPGView)

    @ Slot()
    def convert_jpg_to_pdf_selected(self):
        self._parent_window.setWindowTitle(
            "PDF Editor - Outil de convertion de JPG vers PDF")
        self.change_view_signal.emit(GV.ViewConstants.JPGtoPDFView)
