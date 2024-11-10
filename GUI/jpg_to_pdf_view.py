from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QFileDialog, QMessageBox
)
from PySide6.QtCore import Signal
import global_variables as GV
from Backend.pdf_operations import jpg_to_pdf


class JPGToPDFView(QMainWindow):
    display_pdf_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent_window = parent
        self.setGeometry(100, 100, 600, 400)
        self.display_pdf_signal.connect(parent.display_pdf)
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

        # Bouton de convertion
        self.merge_button = QPushButton("Convertir")
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
        self.merge_button.clicked.connect(self.convert_files)
        layout.addWidget(self.merge_button)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionner les fichiers JPG", "", "JPG Files (*.jpg)")
        if files:
            self.file_list.clear()
            self.file_list.addItems(files)

    def convert_files(self):
        self._parent_window.topbar._current_file_path = GV.output_file_converted_from_jpg
        # Récupérer la liste des fichiers JPG sélectionnés par l'utilisateur
        jpg_files = [self.file_list.item(i).text()
                     for i in range(self.file_list.count())]

        result = jpg_to_pdf(jpg_files, GV.output_file_converted_from_jpg)
        if result != "NO_ERROR":
            QMessageBox.warning(self, "Erreur lors de la conversion",
                                result)
        else:
            QMessageBox.warning(self, "Succès de la conversion",
                                f"Le PDF convertit a été enregistré dans le dossier {GV.output_file_converted_from_jpg}")
            # Ouvrir le fichier obtenu après conversion
            self.display_pdf_signal.emit(GV.output_file_converted_from_jpg)
