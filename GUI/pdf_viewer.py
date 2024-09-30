from PySide6.QtWidgets import QMainWindow, QLineEdit
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument, QPdfSearchModel, QPdfLink
from PySide6.QtCore import QRectF, QPoint

from Backend.pdf_operations import text_occurences


class PDFViewer(QMainWindow):
    def __init__(self, parent=None, pdf_file_path: str = ""):
        super().__init__(parent)
        self._pdf_file_path = pdf_file_path
        self._pdf_view = QPdfView(self)
        # Permet l'affichage de toutes les pages du fichier pdf
        self._pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_doc = QPdfDocument(self)
        self._search_model = QPdfSearchModel(self)
        self._search_model.setDocument(self.pdf_doc)
        self._pdf_view.setSearchModel(self._search_model)
        self._nav = self._pdf_view.pageNavigator()
        self.setCentralWidget(self._pdf_view)

        # Ajout d'une barre de recherche
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Rechercher...")
        self.search_bar.hide()  # Masquer la barre par défaut
        self.search_bar.returnPressed.connect(self.search_word)
        # compter le nombre de fois que l'utilisateur a appuyé sur la touche Entrée
        self._return_pressed_times = 0
        self._text_to_search = None
        # nb d'occurences du mot cherché dans le document entier
        self._text_total_occurences = 0
        # occurence courante
        self._current_occurence_index = 0


################################# Méthodes #################################


    def display_pdf(self, pdf_file_path: str):
        self._pdf_file_path = pdf_file_path
        self.pdf_doc.load(self._pdf_file_path)
        self._pdf_view.setDocument(self.pdf_doc)

    def toggle_search_bar(self):
        # Afficher ou masquer la barre de recherche
        if self.search_bar.isVisible():
            self.search_bar.hide()
        else:
            self.search_bar.show()
            self.search_bar.setFocus()

    def search_word(self):
        self._return_pressed_times += 1
        if (self._return_pressed_times == 1):
            # La première fois que l'utilisateur appuie sur entrée,
            # chercher les occurences dans l'entièreté du document
            self._text_to_search = self.search_bar.text()
            self._search_model.setSearchString(self._text_to_search)
            # nb d'occurences du mot cherché dans le document entier
            self._text_total_occurences = text_occurences(self._pdf_file_path,
                                                          self._text_to_search)

        if (self._text_to_search is not None):
            # Si l'utilisateur n'a pas tapé sur entrée pour la première fois
            # aller simplement à l'occurence suivante
            while (self._current_occurence_index < self._text_total_occurences):
                link = self._search_model.resultAtIndex(
                    self._current_occurence_index)
                # surligner le résultat courant
                self._pdf_view.setCurrentSearchResultIndex(
                    self._current_occurence_index)
                self._current_occurence_index += 1
                self._nav.jump(link)
                break
