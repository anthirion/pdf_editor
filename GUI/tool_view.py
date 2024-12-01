import PySide6.QtWidgets
from PySide6.QtCore import Signal
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

    def __init__(self, parent: PDFEditorMainWindow, tool: int = 0) -> None:
        super().__init__()
        self._parent = parent
        self.display_pdf_signal.connect(self._parent.display_pdf)
        self.setGeometry(100, 100, 600, 400)
        self.pdf_files: list[Path] = []
        self.tool_index = tool
        self._caption = ""

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

    def treat_pdfs(self) -> None:
        """
        Cette fonction demande à l'utilisateur de sélectionner des pdf puis leur applique une
        transformation (fusion, séparation, conversion) en fonction de l'outil choisi
        """
        self.set_caption()
        selected_files, _ = PySide6.QtWidgets.QFileDialog.getOpenFileNames(
            self, self._caption, "", "PDF Files (*.pdf)")
        self.pdf_files = [Path(file) for file in selected_files]
        # Récupérer la liste des fichiers PDF sélectionnés par l'utilisateur
        if self.pdf_files:
            self._parent.topbar._current_file_path = GV.output_pdf_path
            message_box_title = "Succès de la conversion de PDF"
            message_box_text = f"Le PDF converti a été enregistré à l'emplacement {GV.output_pdf_path}"
            try:
                match self.tool_index:
                    case GV.ToolConstants.MergerTool:
                        merge_pdf(GV.output_pdf_path, self.pdf_files)
                        message_box_title = message_box_title.replace("conversion", "fusion")
                        message_box_text = message_box_text.replace("converti", "fusionné")
                    case GV.ToolConstants.SplitterTool:
                        split_pdf(GV.output_pdf_path, self.pdf_files)
                        message_box_title = message_box_title.replace("conversion", "division")
                        message_box_text = message_box_text.replace("converti", "divisé")
                    case GV.ToolConstants.JPGtoPDFConverter:
                        jpg_to_pdf(GV.output_pdf_path, self.pdf_files)
                    case GV.ToolConstants.PDFtoJPGConverter:
                        # si plusieurs fichiers sont spécifiés, on ne convertit que le premier
                        pdf_to_convert = self.pdf_files[0]
                        pdf_to_jpg(pdf_to_convert)
                        message_box_text = f"Les images ont été enregistrées dans le dossier {GV.output_folder}"
            # exceptions rejetées après l'échec d'une transformation (fusion, division ou conversion)
            except FileNotFoundError:
                PySide6.QtWidgets.QMessageBox.warning(self, self.failure_msg,
                                                      GV.file_not_found_error_msg)
            except ValueError:
                PySide6.QtWidgets.QMessageBox.warning(self, self.failure_msg,
                                                      GV.empty_list_error_msg)
            except OSError:
                PySide6.QtWidgets.QMessageBox.warning(self, self.failure_msg,
                                                      "Une erreur système s'est produite")

            # revenir à la homepage en attendant le traitement des fichiers
            self._parent.content_area.setCurrentIndex(0)
            PySide6.QtWidgets.QMessageBox.information(self, message_box_title, message_box_text)
            # Afficher le fichier pdf obtenu après la transformation, sauf si le résultat de la
            # transformation n'est pas un fichier pdf
            if self.tool_index != GV.ToolConstants.PDFtoJPGConverter:
                self.display_pdf_signal.emit(str(GV.output_pdf_path))
        else:
            # revenir à la homepage
            self._parent.content_area.setCurrentIndex(0)
