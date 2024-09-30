from PySide6.QtWidgets import (
    QMessageBox, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QListWidget, QInputDialog
)
from PySide6.QtCore import Signal

from Backend.pdf_operations import (
    merge_pdf
)
import global_variables as GV


class PDFMergerView(QMainWindow):
    display_pdf_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent_window = parent
        self.display_pdf_signal.connect(parent.display_pdf)
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Bouton de sélection de fichiers
        self.select_button = QPushButton("Sélectionnez les fichiers")
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4136;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #FF7166;
            }
        """)
        self.select_button.clicked.connect(self.select_files)
        layout.addWidget(self.select_button)

        # Liste des fichiers sélectionnés
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        # Bouton de fusion
        self.merge_button = QPushButton("Fusionner les PDF")
        self.merge_button.setStyleSheet("""
            QPushButton {
                background-color: #2ECC40;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3D9970;
            }
        """)
        self.merge_button.clicked.connect(self.merge_pdfs)
        layout.addWidget(self.merge_button)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionner les fichiers PDF", "", "PDF Files (*.pdf)")
        if files:
            self.file_list.clear()
            self.file_list.addItems(files)

    def merge_pdfs(self):
        # Récupérer la liste des fichiers PDF sélectionnés par l'utilisateur
        pdf_files = [self.file_list.item(i).text()
                     for i in range(self.file_list.count())]

        if pdf_files:
            self._parent_window._topbar._current_file_path = GV.output_merged_pdf
            # Boîte de dialogue pour entrer le nom du fichier fusionné
            output_file_name_without_extension, ok = \
                QInputDialog.getText(self, "Renommer le fichier",
                                     "Entrez ci-dessous le nom du PDF fusionné:\nATTENTION: n'ajoutez pas l'extension !")
            # nom du fichier stockant le résultat de la fusion
            if ok and output_file_name_without_extension:
                extension = ".pdf"
                new_output_file_name = output_file_name_without_extension
                output_path = GV.default_save_dir + new_output_file_name + extension
            else:
                output_path = GV.output_merged_pdf  # nom par défaut
            merge_pdf(output_path, *pdf_files)
            QMessageBox.information(self, "Succès de la fusion de PDF",
                                    f"Le PDF fusionné a été enregistré à l'emplacement {output_path}")
            # Ouvrir le fichier fusionné
            self.display_pdf_signal.emit(output_path)
        else:
            QMessageBox.warning(self, "Echec de la fusion de PDF",
                                "Aucun fichier PDF à fusionner.")
