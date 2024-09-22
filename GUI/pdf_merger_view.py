from PySide6.QtWidgets import (QMessageBox, QMainWindow, QWidget, QVBoxLayout,
                               QPushButton, QFileDialog, QListWidget)
from PySide6.QtCore import Signal

from Backend.pdf_operations import (
    merge_pdf
)
import global_variables as GV


class PDFMergerView(QMainWindow):
    display_pdf_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.display_pdf_signal.connect(parent.display_pdf)
        self.setWindowTitle("PDF Editor - Fusion de PDF")
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
            merge_pdf(GV.output_file, *pdf_files)
            QMessageBox.information(self, "Succès de la fusion de PDF",
                                    f"Le PDF fusionné a été enregistré dans le dossier {GV.output_file}")
            # Ouvrir le fichier fusionné
            self.display_pdf_signal.emit(GV.output_file)
        else:
            QMessageBox.warning(self, "Echec de la fusion de PDF",
                                "Aucun fichier PDF à fusionner.")
