# Global variables for backend
from enum import IntEnum


class ViewConstants(IntEnum):
    # ATTENTION: utiliser un IntEnum plutôt qu'un enum
    MergerView = 1
    SplitterView = 2
    PDFtoJPGView = 3
    JPGtoPDFView = 4
    ReaderView = 5


default_save_dir = "/home/thiran/projets_persos/pdf_editor/pdf_examples/"
merged_pdf_default_name = default_save_dir + "merged.pdf"
converted_pdf_from_jpg_name = default_save_dir + "converted.pdf"

# Global variables for GUI
default_spacing = 40
