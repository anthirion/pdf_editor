from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QFileDialog, QMessageBox


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        split_pdf_action = QAction("Diviser PDF", self)
        convert_pdf_to_png_action = QAction("Convertir de PDF vers PNG", self)
        convert_png_to_pdf_action = QAction("Convertir de PNG vers PDF", self)

        tools_menu.addAction(merge_pdf_action)
        tools_menu.addAction(split_pdf_action)
        tools_menu.addAction(convert_pdf_to_png_action)
        tools_menu.addAction(convert_png_to_pdf_action)

        # Menu Aide
        help_menu = self.addMenu("Aide")
        get_online_help = QAction("Obtenir de l'aide en ligne", self)
        help_menu.addAction(get_online_help)

################################# Signaux #################################

    def open_file_dialog(self):
        # Ouvre une boîte de dialogue pour sélectionner un fichier PDF
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier", "", "PDF Files (*.pdf);;All Files (*)")

        if file_name:  # Si un fichier est sélectionné
            QMessageBox.information(self,
                                    "Fichier Sélectionné",
                                    f"Vous avez sélectionné : {file_name}")
        else:
            QMessageBox.warning(self, "Aucun Fichier",
                                "Aucun fichier n'a été sélectionné.")
