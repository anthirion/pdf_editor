# Global variables for backend
from enum import IntEnum


class ViewConstants(IntEnum):
    # ATTENTION: utiliser un IntEnum plutôt qu'un enum
    MergerView = 1
    SplitterView = 2
    PDFtoJPGView = 3
    JPGtoPDFView = 4
    ReaderView = 5


output_merged_pdf = "/home/thiran/projets_persos/pdf_editor/pdf_examples/merged.pdf"
output_file_converted_from_jpg = "/home/thiran/projets_persos/pdf_editor/pdf_examples/converted.pdf"

# Global variables for GUI
default_spacing = 40
