import PySide6.QtWidgets
from PySide6.QtCore import Signal

from Backend.pdf_operations import (
    merge_pdf, split_pdf, jpg_to_pdf, pdf_to_jpg
)
import global_variables as GV


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

    def __init__(self, parent: PySide6.QtWidgets.QWidget = None, tool: int = 0) -> None:
        super().__init__()
        self._parent = parent
        self.display_pdf_signal.connect(self._parent.display_pdf)
        self.setGeometry(100, 100, 600, 400)
        self.pdf_files: list[str] = []
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

    def treat_pdfs(self):
        """
        Cette fonction demande à l'utilisateur de sélectionner des pdf puis leur applique une
        transformation (fusion, séparation, conversion) en fonction de l'outil choisi
        """
        self.set_caption()
        self.pdf_files, _ = PySide6.QtWidgets.QFileDialog.getOpenFileNames(
            self, self._caption, "", "PDF Files (*.pdf)")
        # Récupérer la liste des fichiers PDF sélectionnés par l'utilisateur
        if self.pdf_files:
            self._parent.topbar._current_file_path = GV.merged_pdf_default_path
            message_box_title = "Succès de la conversion de PDF"
            message_box_text = f"Le PDF converti a été enregistré à l'emplacement {GV.merged_pdf_default_path}"
            match self.tool_index:
                case GV.ToolConstants.MergerTool:
                    merge_pdf(GV.merged_pdf_default_path, *self.pdf_files)
                    message_box_title = message_box_title.replace("conversion", "fusion")
                    message_box_text = message_box_text.replace("converti", "fusionné")
                case GV.ToolConstants.SplitterTool:
                    split_pdf(GV.merged_pdf_default_path, *self.pdf_files)
                    message_box_title = message_box_title.replace("conversion", "division")
                    message_box_text = message_box_text.replace("converti", "divisé")
                case GV.ToolConstants.JPGtoPDFConverter:
                    jpg_to_pdf(GV.merged_pdf_default_path, *self.pdf_files)
                case GV.ToolConstants.PDFtoJPGConverter:
                    pdf_to_jpg(GV.merged_pdf_default_path, *self.pdf_files)

            PySide6.QtWidgets.QMessageBox.information(self, message_box_title, message_box_text)
            # Ouvrir le fichier fusionné
            self.display_pdf_signal.emit(GV.merged_pdf_default_path)
        else:
            PySide6.QtWidgets.QMessageBox.warning(self, "Echec de l'opération",
                                                  "Aucun fichier PDF fourni")
