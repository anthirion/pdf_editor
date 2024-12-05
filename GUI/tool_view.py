import PySide6.QtWidgets
from PySide6.QtCore import Signal, QTimer, QThread, Slot
from PySide6.QtWidgets import QLabel, QVBoxLayout, QMessageBox
from pathlib import Path

import global_variables as GV
from Backend.pdf_operations import (
    merge_pdf, split_pdf, jpg_to_pdf, pdf_to_jpg
)
from GUI.main_view import PDFEditorMainWindow


class ToolView(PySide6.QtWidgets.QWidget):
    """
    Cette classe gère l'affichage des outils du logiciel à savoir :
    la fusion et séparation de pdf, ainsi que les conversions de formats.
    Toutes les vues utilitaires sont regroupées au sein d'une même
    classe car les vues sont identiques pour tous les outils
    Pour savoir quel outil a été sélectionné par l'utilisateur,
    on passe au constructeur un entier qui indique le numéro de
    l'outil sélectionné
    """
    display_pdf_signal = Signal(str)
    failure_msg = "Echec de l'opération"

    def __init__(self, parent_window: PDFEditorMainWindow, tool: int = 0) -> None:
        super().__init__()
        self._parent_window = parent_window
        self.display_pdf_signal.connect(self._parent_window.display_pdf)
        self.setGeometry(100, 100, 600, 400)
        self.pdf_files: list[Path] = []
        self.tool_index = tool
        self._caption = ""
        self.message_box_title = "Succès de la conversion de PDF"
        self.message_box_text = f"Le PDF converti a été enregistré à l'emplacement {GV.output_pdf_path}"
        # fenêtre qui s'ouvre et se ferme automatiquement indiquant à l'utilisateur
        # de patienter pendant le traitement de sa requête
        self.loading_dialog = LoadingDialog()
        self.loading_timer = QTimer()
        self.loading_timer.setSingleShot(True)
        self.loading_timer.setInterval(3 * 1000)  # 3s
        self.loading_timer.timeout.connect(self.show_loader)
        # opération de transformation (fusion, split, conversion) est longue, elle
        # est faite parallèlement au sein d'un thread
        self.pdf_tranformation = TransformationThread(self)

    def set_caption(self) -> None:
        base_caption = "Sélectionner les fichier à traiter"
        match self.tool_index:
            case GV.ToolConstants.MergerTool:
                self._caption = base_caption.replace("traiter", "fusionner")
            case GV.ToolConstants.SplitterTool:
                self._caption = base_caption.replace("traiter", "diviser")
            case GV.ToolConstants.JPGtoPDFConverter:
                self._caption = base_caption.replace("traiter", "convertir")
            case GV.ToolConstants.PDFtoJPGConverter:
                self._caption = base_caption.replace("traiter", "convertir")
            case _:
                self._caption = base_caption

    def transform_pdfs(self) -> None:
        """
        Cette fonction demande à l'utilisateur de sélectionner des pdf puis leur applique une
        transformation (fusion, séparation, conversion) en fonction de l'outil choisi
        """
        self.set_caption()
        selected_files, _ = PySide6.QtWidgets.QFileDialog.getOpenFileNames(
            self, self._caption, "")
        self.pdf_files = [Path(file) for file in selected_files]
        # Récupérer la liste des fichiers PDF sélectionnés par l'utilisateur
        if self.pdf_files:
            self._parent_window.topbar._current_file_path = GV.output_pdf_path
            self.set_messages()
            self.loading_timer.start()
            self.pdf_tranformation.start()
        # revenir à la homepage en attendant le traitement des fichiers
        self._parent_window.content_area.setCurrentIndex(0)

    def set_messages(self) -> None:
        """
        Modifie les valeurs des variables self.message_box_title et self.message_box_text
        """
        match self.tool_index:
            case GV.ToolConstants.MergerTool:
                self.message_box_title = self.message_box_title.replace("conversion", "fusion")
                self.message_box_text = self.message_box_text.replace("converti", "fusionné")
            case GV.ToolConstants.SplitterTool:
                self.message_box_title = self.message_box_title.replace("conversion", "division")
                self.message_box_text = self.message_box_text.replace("converti", "divisé")
            case GV.ToolConstants.PDFtoJPGConverter:
                self.message_box_text = f"Les images ont été enregistrées dans le dossier {GV.output_folder}"

    @Slot(int, str)
    def transformation_process_finished(self, error, msg) -> None:
        # fermer la fenêtre de loading automatiquement à la fin du traitement
        if self.loading_dialog.isVisible():
            self.loading_dialog.close()
        self.loading_timer.stop()
        # afficher un message à l'utilisateur indiquant le résultat de la transformation
        if error:
            QMessageBox.warning(self, self.failure_msg, msg)
        else:
            QMessageBox.information(self, self.message_box_title, self.message_box_text)

        # Afficher le fichier pdf obtenu après la transformation, sauf si le résultat de la
        # transformation n'est pas un fichier pdf
        if self.tool_index != GV.ToolConstants.PDFtoJPGConverter:
            self.display_pdf_signal.emit(str(GV.output_pdf_path))

    def show_loader(self) -> None:
        """
        Ajouter un message indiquant à l'utilisateur de patienter.
        Ce message prend la forme d'une fenêtre qui s'ouvre par dessus la fenêtre principale
        """
        self.loading_dialog.show()


class LoadingDialog(PySide6.QtWidgets.QDialog):
    """
    Cette classe est une fenêtre de dialogue temporaire qui s'ouvre par dessus la
    fenêtre principale pendant le traitement d'un fichier (fusion, split, conversion).
    Cette fenêtre a pour but d'indiquer à l'utilisateur de patienter et se ferme automatiquement
    une fois le traitement terminé. La fenêtre n'attend donc pas d'intéraction de la part de
    l'utilisateur
    """

    def __init__(self) -> None:
        super().__init__()
        self.setModal(True)
        layout = QVBoxLayout()
        label = QLabel("Veuillez patienter pendant le traitement...")
        layout.addWidget(label)
        self.setLayout(layout)


class TransformationThread(QThread):
    """
    Ce thread effectue la transformation d'un ou de plusieurs fichiers pdf
    """
    # int: 0 si pas d'erreur, 1 sinon
    # str: message à afficher dans la boite de dialogue
    processing_finished_signal = Signal(int, str)

    def __init__(self, parent) -> None:
        super().__init__()
        self._parent = parent
        self.tool_index = parent.tool_index
        self.message_box_title = parent.message_box_title
        self.message_box_text = parent.message_box_text
        self.processing_finished_signal.connect(parent.transformation_process_finished)

    def run(self) -> None:
        pdf_files = self._parent.pdf_files
        try:
            match self.tool_index:
                case GV.ToolConstants.MergerTool:
                    merge_pdf(GV.output_pdf_path, pdf_files)
                case GV.ToolConstants.SplitterTool:
                    split_pdf(GV.output_pdf_path, pdf_files)
                case GV.ToolConstants.JPGtoPDFConverter:
                    jpg_to_pdf(GV.output_pdf_path, pdf_files)
                case GV.ToolConstants.PDFtoJPGConverter:
                    # si plusieurs fichiers sont spécifiés, on ne convertit que le premier
                    pdf_to_convert = pdf_files[0]
                    pdf_to_jpg(pdf_to_convert)
        # exceptions rejetées après l'échec d'un traitement (fusion, division ou conversion)
        except FileNotFoundError:
            self.processing_finished_signal.emit(1, GV.file_not_found_error_msg)
        except ValueError:
            self.processing_finished_signal.emit(1, GV.empty_list_error_msg)
        except OSError:
            self.processing_finished_signal.emit(1, "Une erreur système s'est produite")
        self.processing_finished_signal.emit(0, "")
