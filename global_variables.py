# Global variables for backend
from enum import IntEnum
from pathlib import Path


class ToolConstants(IntEnum):
    # ATTENTION: utiliser un IntEnum plutôt qu'un enum
    MergerTool = 1
    SplitterTool = 2
    PDFtoJPGConverter = 3
    JPGtoPDFConverter = 4


default_save_dir = "/home/thiran/projets_persos/pdf_editor/tests/"
output_pdf_path = Path(default_save_dir) / Path("output.pdf")
output_folder = Path(default_save_dir) / Path("output_jpgs")
output_file_converted_from_jpg = Path(default_save_dir) / Path("converted.pdf")

############ Error messages ############
file_not_found_error_msg = "Le fichier spécifié est introuvable"
file_exists_error_msg = "Le fichier spécifié n'existe pas"
empty_list_error_msg = "La liste des fichiers PDF fournie est vide"

# Global variables for GUI
default_spacing = 40
