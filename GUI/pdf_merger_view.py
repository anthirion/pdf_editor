import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QPushButton, QFileDialog, QListWidget)


class PDFMergerView(QMainWindow):
    def __init__(self):
        super().__init__()
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
        # Ici, vous implémenterez la logique de fusion des PDF
        # Pour l'instant, nous allons juste afficher un message
        print("Fusion des PDF sélectionnés")
        # Vous pouvez utiliser une bibliothèque comme PyPDF2 pour la fusion réelle
