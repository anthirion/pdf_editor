# Global variables for backend
from enum import IntEnum


class ViewConstants(IntEnum):
    # ATTENTION: utiliser un IntEnum plutôt qu'un enum
    MergerView = 1
    SplitterView = 2
    PDFtoPNGView = 3
    PNGtoPDFView = 4
    ReaderView = 5


output_file = "/home/thiran/projets_persos/pdf_editor/pdf_examples/merged.pdf"

# Global variables for GUI
default_spacing = 40
