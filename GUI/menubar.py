from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QFileDialog, QMessageBox
from PySide6.QtCore import Signal, Slot

import global_variables as GV


class MenuBar(QMenuBar):
    # Le signal envoie un entier qui indique la vue à afficher :
    # 1 si vue de fusion des pdf (pdf_merger_view)
    # 2 si vue de division des pdf (pdf_splitter_view), etc
    # pour plus de simplicité, les constantes sont définies dans l'enum ViewConstants
    change_view_signal = Signal(int)
    display_pdf_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.change_view_signal.connect(parent.change_view)
        self.display_pdf_signal.connect(parent.display_pdf)

        # Menu Fichier
        self.file_menu = self.addMenu("Fichier")
        self.new_action = QAction("Nouveau", self)
        self.open_action = QAction("Ouvrir", self)
        self.open_action.triggered.connect(self.open_file_dialog)
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)

        # Menu Outils
        tools_menu = self.addMenu("Outils")
        merge_pdf_action = QAction("Fusionner PDF", self)
        merge_pdf_action.triggered.connect(self.merge_pdf_selected)
        split_pdf_action = QAction("Diviser PDF", self)
        merge_pdf_action.triggered.connect(self.split_pdf_selected)
        convert_pdf_to_png_action = QAction("Convertir de PDF vers PNG", self)
        merge_pdf_action.triggered.connect(self.convert_pdf_to_png_selected)
        convert_png_to_pdf_action = QAction("Convertir de PNG vers PDF", self)
        merge_pdf_action.triggered.connect(self.convert_png_to_pdf_selected)

        tools_menu.addAction(merge_pdf_action)
        tools_menu.addAction(split_pdf_action)
        tools_menu.addAction(convert_pdf_to_png_action)
        tools_menu.addAction(convert_png_to_pdf_action)

        # Menu Aide
        help_menu = self.addMenu("Aide")
        get_online_help = QAction("Obtenir de l'aide en ligne", self)
        help_menu.addAction(get_online_help)


################################# Slots #################################

    @Slot()
    def open_file_dialog(self):
        # Ouvre une boîte de dialogue pour sélectionner un fichier PDF
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier", "", "PDF Files (*.pdf);;All Files (*)")

        if file_name:
            self.display_pdf_signal.emit(file_name)
        else:
            QMessageBox.warning(self, "Aucun Fichier",
                                "Aucun fichier n'a été sélectionné.")

    @Slot()
    def merge_pdf_selected(self):
        self.change_view_signal.emit(GV.ViewConstants.MergerView)

    @Slot()
    def split_pdf_selected(self):
        self.change_view_signal.emit(GV.ViewConstants.SplitterView)

    @Slot()
    def convert_pdf_to_png_selected(self):
        self.change_view_signal.emit(GV.ViewConstants.PDFtoPNGView)

    @Slot()
    def convert_png_to_pdf_selected(self):
        self.change_view_signal.emit(GV.ViewConstants.PNGtoPDFView)
