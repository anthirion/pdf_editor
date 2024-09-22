from PySide6.QtWidgets import QMainWindow, QLineEdit
from PySide6.QtPdfWidgets import QPdfView
from PySide6 import QtPdf

from Backend.pdf_operations import search_text


class PDFViewer(QMainWindow):
    def __init__(self, parent=None, pdf_file_path: str = ""):
        super().__init__(parent)
        self._pdf_file_path = pdf_file_path
        self.pdf_view = QPdfView()
        # Permet l'affichage de toutes les pages du fichier pdf
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_doc = QtPdf.QPdfDocument()
        self.setCentralWidget(self.pdf_view)

        # Ajout d'une barre de recherche
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Rechercher...")
        self.search_bar.hide()  # Masquer la barre par défaut
        self.search_bar.returnPressed.connect(self.search_word)


################################# Méthodes #################################

    def display_pdf(self, pdf_file_path: str):
        self._pdf_file_path = pdf_file_path
        self.pdf_doc.load(self._pdf_file_path)
        self.pdf_view.setDocument(self.pdf_doc)

    def toggle_search_bar(self):
        # Afficher ou masquer la barre de recherche
        if self.search_bar.isVisible():
            self.search_bar.hide()
        else:
            self.search_bar.show()
            self.search_bar.setFocus()

    def search_word(self):
        print("Recherche de mot")
        # Réinitialiser la recherche à chaque nouvelle entrée
        text_to_search = self.search_bar.text()
        if not text_to_search:
            return

        occurences = search_text(self._pdf_file_path, text_to_search)
        print(f"Nombre d'occurences trouvées: {occurences}")
        # self.highlight_search_result()

    # def highlight_search_result(self):
    #     if not self.search_results:
    #         return

    #     page_num, search_text = self.search_results[self.current_search_index]
    #     self.pdf_view.setPage(page_num)  # Afficher la page avec l'occurrence
        # À ce stade, il est possible d'ajouter du surlignage (non implémenté ici)
