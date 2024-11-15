from pathlib import Path

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenuBar, QToolBar, QFileDialog, QMessageBox, QWidget

import global_variables as GV
# importation des icones
from GUI.resources import (
    open_icon, quit_icon, save_icon,
    save_as_icon, search_icon, merge_icon, help_icon
)


class TopBar(QMenuBar, QToolBar):
    """
    The TopBar is composed of a menubar and a topbar
    """
    # Le signal envoie un entier qui indique l'outil sélectionné par l'utilisateur.
    # L'entier correspondant est donné par l'enum ToolConstants défini dans les variables globales
    # Ensuite, en fonction de l'outil sélectionné, la vue adéquate sera affichée
    display_tool_view_signal = Signal(int)
    display_pdf_signal = Signal(str)
    search_text = Signal()
    # Le signal suivant envoie un entier indiquant le niveau de zoom que l'utilisateur souhaite
    # Si cet entier est 1, cela signifie que l'utilisateur souhaite zoomer
    # Si cet entier est -1, cela signifie que l'utilisateur souhaite dézoomer
    # Si cet entier est 0, cela signifie que l'utilisateur souhaite réinitialiser le zoom
    zoom_signal = Signal(int)

    def __init__(self, parent: QWidget):
        # le parent est la plupart du temps la main_view
        super().__init__(parent)
        self._parent_window = parent
        self._current_file_path = Path()
        menu = parent.menuBar()
        self.display_tool_view_signal.connect(parent.display_tool_view)
        self.display_pdf_signal.connect(parent.display_pdf)
        self.search_text.connect(
            parent.pdf_viewer.search_bar.toggle_search_bar)
        self.zoom_signal.connect(parent.pdf_viewer.zoom_handler)

        """
        MenuBar
        """
        # Menu Fichier
        self.file_menu = menu.addMenu("Fichier")
        # Sous-menu "Nouveau"
        # self.new_action = QAction(QIcon(add_icon), "Nouveau", self)
        # self.new_action.setShortcut("Ctrl+N")
        # Sous-menu "Enregistrer"
        self.save_action = QAction(QIcon(save_icon), "Enregistrer", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file)
        # Sous-menu "Enregistrer sous"
        self.save_as_action = QAction(
            QIcon(save_as_icon), "Enregistrer sous", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.save_as_action.triggered.connect(self.save_file_as)
        # Sous-menu "Ouvrir"
        self.open_action = QAction(QIcon(open_icon), "Ouvrir", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file_dialog)
        # Sous-menu "Quitter"
        self.quit_action = QAction(QIcon(quit_icon), "Quitter", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.quit_application)
        # Ajouter les actions au menu Fichier
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.quit_action)

        # Menu Edition
        edition_menu = menu.addMenu("Edition")
        # Sous-menu "Rechercher"
        self.search_action = QAction(QIcon(search_icon), "Rechercher", self)
        self.search_action.setShortcut("Ctrl+F")
        self.search_action.triggered.connect(self.search_action_selected)
        edition_menu.addAction(self.search_action)

        # Menu Affichage
        view_menu = menu.addMenu("Affichage")
        # Sous-menu "Zoom"
        zoom_menu = view_menu.addMenu("Zoom")
        # Action "Zoom In"
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self.zoom_in)
        # Action "Zoom Out"
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.zoom_out)
        # Action "Reset Zoom"
        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.triggered.connect(self.reset_zoom)
        # Ajouter les actions au sous-menu "Zoom"
        zoom_menu.addAction(zoom_in_action)
        zoom_menu.addAction(zoom_out_action)
        zoom_menu.addAction(reset_zoom_action)

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
        # toolbar.addAction(self.new_action)
        toolbar.addAction(self.save_as_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.search_action)

        parent.addToolBar(toolbar)

    ################################# Slots génériques #################################

    @Slot()
    def open_file_dialog(self):
        # Ouvre une boîte de dialogue pour sélectionner un fichier PDF
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier", "", "PDF Files (*.pdf);;All Files (*)")

        if file_path:
            self.display_pdf_signal.emit(file_path)

    def save_file(self):
        pass

    def save_file_as(self):
        default_directory = "/home/thiran/projets_persos/pdf_editor/pdf_examples/"
        # Ouvrir une boîte de dialogue pour choisir le nom et l'emplacement du fichier à enregistrer
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le fichier sous", default_directory, "PDF Files (*.pdf);;All Files (*)"
        )

        if file_path:
            try:
                # TODO: enregistrer un fichier non existant
                source_file_path = Path(self._parent_window._displayed_file)
                destination_file = Path(file_path)
                self._parent_window._displayed_file = file_path

                # Copier le contenu du fichier actuel vers le fichier de destination
                destination_file.write_bytes(
                    source_file_path.read_bytes())

                QMessageBox.information(
                    self, "Enregistrement", "Fichier enregistré avec succès.")

            except Exception as e:
                # Message d'erreur en cas de problème lors de l'enregistrement
                QMessageBox.critical(
                    self, "Erreur d'enregistrement", f"Impossible d'enregistrer le fichier : {e}")
        else:
            # Si aucun chemin n'est sélectionné
            QMessageBox.warning(self, "Enregistrement annulé",
                                "Aucun fichier n'a été enregistré.")

    @Slot()
    def quit_application(self):
        self._parent_window._app.instance().quit()

    @Slot()
    def search_action_selected(self):
        self.search_text.emit()

    ####################### Slots changement de vue d'affichage #######################

    @Slot()
    def merge_pdf_selected(self):
        self._parent_window.setWindowTitle("PDF Editor - Outil de fusion")
        self.display_tool_view_signal.emit(GV.ToolConstants.MergerTool)

    @Slot()
    def split_pdf_selected(self):
        self._parent_window.setWindowTitle("PDF Editor - Outil de séparation")
        self.display_tool_view_signal.emit(GV.ToolConstants.SplitterTool)

    @Slot()
    def convert_pdf_to_jpg_selected(self):
        self._parent_window.setWindowTitle(
            "PDF Editor - Outil de convertion de PDF vers JPG")
        self.display_tool_view_signal.emit(GV.ToolConstants.PDFtoJPGConverter)

    @Slot()
    def convert_jpg_to_pdf_selected(self):
        self._parent_window.setWindowTitle(
            "PDF Editor - Outil de convertion de JPG vers PDF")
        self.display_tool_view_signal.emit(GV.ToolConstants.JPGtoPDFConverter)

    ################################# Slots gérant le zoom #################################
    @Slot()
    def zoom_in(self):
        self.zoom_signal.emit(1)

    @Slot()
    def zoom_out(self):
        self.zoom_signal.emit(-1)

    @Slot()
    def reset_zoom(self):
        self.zoom_signal.emit(0)
