# Global variables for backend
from enum import IntEnum


class ToolConstants(IntEnum):
    # ATTENTION: utiliser un IntEnum plutôt qu'un enum
    MergerTool = 1
    SplitterTool = 2
    PDFtoJPGConverter = 3
    JPGtoPDFConverter = 4


default_save_dir = "/home/thiran/projets_persos/pdf_editor/pdf_examples/"
output_pdf_path = default_save_dir + "output.pdf"
output_folder = default_save_dir + "output_jpgs"
output_file_converted_from_jpg = default_save_dir + "converted.pdf"

# Global variables for GUI
default_spacing = 40
