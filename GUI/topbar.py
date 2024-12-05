from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QFileDialog, QMessageBox, QWidget
from pathlib import Path

import global_variables as GV
from GUI.main_view import PDFEditorMainWindow
# importation des icones
from GUI.resources import (
    open_icon, quit_icon, save_icon,
    save_as_icon, search_icon, help_icon,
    merge_icon, pdf_to_jpg_icon, jpg_to_pdf_icon
)


class TopBar(QWidget):
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

    def __init__(self, parent_window: PDFEditorMainWindow) -> None:
        super().__init__()
        self._parent_window = parent_window
        self._current_file_path = Path()
        self._menu = parent_window.barmenu
        self.connect_signals()
        self.init_topbar()

    def connect_signals(self) -> None:
        self.display_tool_view_signal.connect(self._parent_window.display_tool_view)
        self.display_pdf_signal.connect(self._parent_window.display_pdf)
        self.search_text.connect(
            self._parent_window.pdf_viewer.search_bar.toggle_search_bar)
        self.zoom_signal.connect(self._parent_window.pdf_viewer.zoom_handler)

    def init_topbar(self) -> None:
        """
        MenuBar initialization
        """
        # Menu Fichier
        file_menu = self._menu.addMenu("Fichier")
        # Sous-menu "Nouveau"
        # self.new_action = QAction(QIcon(add_icon), "Nouveau", self)
        # self.new_action.setShortcut("Ctrl+N")
        # Sous-menu "Enregistrer"
        save_action = QAction(QIcon(save_icon), "Enregistrer", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        # Sous-menu "Enregistrer sous"
        save_as_action = QAction(
            QIcon(save_as_icon), "Enregistrer sous", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        # Sous-menu "Ouvrir"
        open_action = QAction(QIcon(open_icon), "Ouvrir", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        # Sous-menu "Quitter"
        quit_action = QAction(QIcon(quit_icon), "Quitter", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.quit_application)
        # Ajouter les actions au menu Fichier
        # file_menu.addAction(self.new_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(open_action)
        file_menu.addAction(quit_action)

        # Menu Edition
        edition_menu = self._menu.addMenu("Edition")
        # Sous-menu "Rechercher"
        search_action = QAction(QIcon(search_icon), "Rechercher", self)
        search_action.setShortcut("Ctrl+F")
        search_action.triggered.connect(self.search_action_selected)
        edition_menu.addAction(search_action)

        # Menu Affichage
        view_menu = self._menu.addMenu("Affichage")
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
        tools_menu = self._menu.addMenu("Outils")
        # Sous-menu "Fusionner PDF"
        merge_pdf_action = QAction(QIcon(merge_icon), "Fusionner PDF", self)
        merge_pdf_action.triggered.connect(self.merge_pdf_selected)
        # Sous-menu "Diviser PDF"
        # split_pdf_action = QAction(QIcon(split_icon), "Diviser PDF", self)
        # split_pdf_action.triggered.connect(self.split_pdf_selected)
        # Sous-menu "Convertir de PDF vers JPG"
        convert_pdf_to_jpg_action = QAction(QIcon(pdf_to_jpg_icon), "Convertir de PDF vers JPG", self)
        convert_pdf_to_jpg_action.triggered.connect(
            self.convert_pdf_to_jpg_selected)
        # Sous-menu "Convertir de JPG vers PDF"
        convert_jpg_to_pdf_action = QAction(QIcon(jpg_to_pdf_icon), "Convertir de JPG vers PDF", self)
        convert_jpg_to_pdf_action.triggered.connect(
            self.convert_jpg_to_pdf_selected)

        tools_menu.addAction(merge_pdf_action)
        # tools_menu.addAction(split_pdf_action)
        tools_menu.addAction(convert_pdf_to_jpg_action)
        tools_menu.addAction(convert_jpg_to_pdf_action)

        # Menu Aide
        help_menu = self._menu.addMenu("Aide")
        # Sous-menu "Obtenir de l'aide"
        get_online_help = QAction(QIcon(help_icon), "Obtenir de l'aide", self)
        help_menu.addAction(get_online_help)

        """
        ToolBar initialization
        """
        toolbar = QToolBar("Barre d'outils", self)
        # toolbar.addAction(self.new_action)
        toolbar.addAction(save_as_action)
        toolbar.addAction(open_action)
        toolbar.addAction(search_action)

        self._parent_window.addToolBar(toolbar)

    ################################# Slots génériques #################################

    @Slot()
    def open_file_dialog(self) -> None:
        # Ouvre une boîte de dialogue pour sélectionner un fichier PDF
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier", "", "PDF Files (*.pdf);;All Files (*)")

        if file_path:
            self.display_pdf_signal.emit(file_path)

    def save_file(self) -> None:
        # TODO
        pass

    def save_file_as(self) -> None:
        # Ouvrir une boîte de dialogue pour choisir le nom et l'emplacement du fichier à enregistrer
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le fichier sous", GV.default_save_dir, "PDF Files (*.pdf);;All Files (*)"
        )

        if file_path:
            try:
                # TODO: enregistrer un fichier non existant
                # Dans cette version du code, on ne fait que renommer le fichier
                source_path = Path(self._parent_window.displayed_file)
                destination_path = Path(file_path)
                source_path.rename(destination_path)
                QMessageBox.information(
                    self, "Enregistrement", "Fichier enregistré avec succès.")

            except Exception as e:
                # Message d'erreur en cas de problème lors de l'enregistrement
                QMessageBox.critical(
                    self, "Erreur d'enregistrement", f"Impossible d'enregistrer le fichier : {e}")

    @Slot()
    def quit_application(self) -> None:
        app = self._parent_window.app.instance()
        if app is not None:
            app.quit()
        else:
            raise RuntimeError("Aucune instance de l'application n'est disponible.")

    @Slot()
    def search_action_selected(self) -> None:
        self.search_text.emit()

    ####################### Slots changement de vue d'affichage #######################

    @Slot()
    def merge_pdf_selected(self) -> None:
        self._parent_window.setWindowTitle("PDF Editor - Outil de fusion")
        self.display_tool_view_signal.emit(GV.ToolConstants.MergerTool)

    @Slot()
    def split_pdf_selected(self) -> None:
        self._parent_window.setWindowTitle("PDF Editor - Outil de séparation")
        self.display_tool_view_signal.emit(GV.ToolConstants.SplitterTool)

    @Slot()
    def convert_pdf_to_jpg_selected(self) -> None:
        self._parent_window.setWindowTitle(
            "PDF Editor - Outil de convertion de PDF vers JPG")
        self.display_tool_view_signal.emit(GV.ToolConstants.PDFtoJPGConverter)

    @Slot()
    def convert_jpg_to_pdf_selected(self) -> None:
        self._parent_window.setWindowTitle(
            "PDF Editor - Outil de convertion de JPG vers PDF")
        self.display_tool_view_signal.emit(GV.ToolConstants.JPGtoPDFConverter)

    ################################# Slots gérant le zoom #################################
    @Slot()
    def zoom_in(self) -> None:
        self.zoom_signal.emit(1)

    @Slot()
    def zoom_out(self) -> None:
        self.zoom_signal.emit(-1)

    @Slot()
    def reset_zoom(self) -> None:
        self.zoom_signal.emit(0)
