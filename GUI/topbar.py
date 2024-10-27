from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenuBar, QToolBar, QFileDialog, QMessageBox, QInputDialog
from PySide6.QtCore import Signal, Slot

from pathlib import Path

import global_variables as GV
# importation des icones
from GUI.resources import (
    add_icon, open_icon, quit_icon, rename_icon,
    search_icon, merge_icon, help_icon
)


class TopBar(QMenuBar, QToolBar):
    """
    The TopBar is composed of a menubar and a topbar
    """
    # Le signal envoie un entier correspondant au numéro de la vue à afficher (voir fichier main_view.py)
    # pour plus de simplicité, les constantes sont définies dans l'enum ViewConstants
    change_view_signal = Signal(int)
    display_pdf_signal = Signal(str)
    search_text = Signal()

    def __init__(self, parent=None):
        # le parent est la plupart du temps la main_view
        super().__init__(parent)
        self._parent_window = parent
        self._current_file_path = Path()
        menu = parent.menuBar()
        self.change_view_signal.connect(parent.change_view)
        self.display_pdf_signal.connect(parent.display_pdf)
        self.search_text.connect(
            parent._pdf_viewer.search_bar.toggle_search_bar)

        """
        MenuBar
        """
        # Menu Fichier
        self.file_menu = menu.addMenu("Fichier")
        # Sous-menu "Nouveau"
        self.new_action = QAction(QIcon(add_icon), "Nouveau", self)
        # Sous-menu "Ouvrir"
        self.open_action = QAction(QIcon(open_icon), "Ouvrir", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file_dialog)
        # Sous-menu "Quitter"
        self.quit_action = QAction(QIcon(quit_icon), "Quitter", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.quit_application)

        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.quit_action)

        # Menu Edition
        edition_menu = menu.addMenu("Edition")
        # Sous-menu "Rechercher"
        self.search_action = QAction(QIcon(search_icon), "Rechercher", self)
        self.search_action.setShortcut("Ctrl+F")
        self.search_action.triggered.connect(self.search_action_selected)
        edition_menu.addAction(self.search_action)
        # Sous-menu "Renommer"
        self.rename_action = QAction(QIcon(rename_icon), "Renommer", self)
        self.rename_action.setShortcut("Ctrl+R")
        self.rename_action.triggered.connect(self.rename)
        edition_menu.addAction(self.rename_action)

        # Menu Outils
        tools_menu = menu.addMenu("Outils")
        # Sous-menu "Fusionner PDF"
        merge_pdf_action = QAction(QIcon(merge_icon), "Fusionner PDF", self)
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
        get_online_help = QAction(QIcon(help_icon), "Obtenir de l'aide", self)
        help_menu.addAction(get_online_help)

        """
        ToolBar
        """
        toolbar = QToolBar("Barre d'outils", self)
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.search_action)
        toolbar.addAction(self.rename_action)

        parent.addToolBar(toolbar)

################################# Slots #################################

    @Slot()
    def open_file_dialog(self):
        # Ouvre une boîte de dialogue pour sélectionner un fichier PDF
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier", "", "PDF Files (*.pdf);;All Files (*)")

        if file_path:
            self.display_pdf_signal.emit(file_path)
            self._current_file_path = Path(file_path)
            final_path_component = Path(file_path).name
            self._parent_window.setWindowTitle(
                "PDF Editor - " + final_path_component)

    @Slot()
    def rename(self):
        # Boîte de dialogue pour entrer le nouveau nom du fichier
        new_file_name_without_extension, ok = \
            QInputDialog.getText(self, "Renommer le fichier",
                                 "Entrez ci-dessous le nouveau nom du fichier:\nATTENTION: n'ajoutez pas l'extension !")

        if ok and new_file_name_without_extension:
            try:
                old_file = self._current_file_path
                extension = old_file.suffix
                new_file_name = new_file_name_without_extension + extension
                new_file = old_file.parent / new_file_name
                old_file.rename(new_file)
                QMessageBox.information(
                    self, "Succès", "Le fichier a été renommé avec succès !")
            except Exception as e:
                QMessageBox.warning(
                    self, "Erreur", f"Impossible de renommer le fichier : {e}")

    @Slot()
    def quit_application(self):
        self._parent_window._app.instance().quit()

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
