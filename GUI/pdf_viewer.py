from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout
)
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument, QPdfSearchModel
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon

from Backend.pdf_operations import text_occurences
from GUI.resources import arrow_up_icon, arrow_down_icon


class SearchBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent_widget = parent

        # Création de la barre de recherche et des boutons
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher...")
        self.search_input.setMinimumWidth(600)
        self.hide()  # Masquer la barre de recherche par défaut
        self.search_input.returnPressed.connect(self.search_word)
        self.button_up = QPushButton()
        self.button_down = QPushButton()

        # Ajouter des icônes aux boutons
        # Icône pour le bouton "up"
        self.button_up.setIcon(QIcon(arrow_up_icon))
        # Icône pour le bouton "down"
        self.button_down.setIcon(QIcon(arrow_down_icon))

        # Disposition en HBoxLayout
        layout = QHBoxLayout(self)
        layout.addWidget(self.search_input)
        layout.addWidget(self.button_up)
        layout.addWidget(self.button_down)

        # compter le nombre de fois que l'utilisateur a appuyé sur la touche Entrée
        self._return_pressed_times = 0
        self._text_to_search = None
        # nb d'occurences du mot cherché dans le document entier
        self._text_total_occurences = 0
        # occurence courante
        self._current_occurence_index = 0
        # Connexion des boutons aux slots
        self.button_up.clicked.connect(self.on_button_up_clicked)
        self.button_down.clicked.connect(self.on_button_down_clicked)

    ################################# Slots #################################

    @Slot()
    def on_button_up_clicked(self):
        print("Bouton up cliqué")
        # Logique pour la recherche vers le haut

    @Slot()
    def on_button_down_clicked(self):
        print("Bouton down cliqué")
        # Logique pour la recherche vers le bas

    @Slot()
    def toggle_search_bar(self):
        # Afficher ou masquer la barre de recherche
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.setFocus()

    @Slot()
    def search_word(self):
        self._return_pressed_times += 1
        if (self._return_pressed_times == 1):
            # La première fois que l'utilisateur appuie sur entrée,
            # chercher les occurences dans l'entièreté du document
            self._text_to_search = self.search_input.text()
            self._parent_widget._search_model.setSearchString(
                self._text_to_search)
            # nb d'occurences du mot cherché dans le document entier
            self._text_total_occurences = text_occurences(self._parent_widget._pdf_file_path,
                                                          self._text_to_search)

        if (self._text_to_search is not None):
            # Si l'utilisateur n'a pas tapé sur entrée pour la première fois
            # aller simplement à l'occurence suivante
            while (self._current_occurence_index < self._text_total_occurences):
                link = self._parent_widget._search_model.resultAtIndex(
                    self._current_occurence_index)
                # surligner le résultat courant
                self._parent_widget._pdf_view.setCurrentSearchResultIndex(
                    self._current_occurence_index)
                self._current_occurence_index += 1
                self._parent_widget._nav.jump(link)
                break


class PDFViewer(QMainWindow):
    def __init__(self, parent=None, pdf_file_path: str = ""):
        super().__init__(parent)
        self._pdf_file_path = pdf_file_path
        self._pdf_view = QPdfView()
        # Permet l'affichage de toutes les pages du fichier pdf
        self._pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_doc = QPdfDocument()
        self._search_model = QPdfSearchModel()
        self._search_model.setDocument(self.pdf_doc)
        self._pdf_view.setSearchModel(self._search_model)
        self._nav = self._pdf_view.pageNavigator()
        self.setCentralWidget(self._pdf_view)

        # Ajout d'une barre de recherche
        self.search_bar = SearchBar(self)

        # Disposition en HBoxLayout
        container = QWidget()
        containerLayout = QVBoxLayout(self)
        containerLayout.addWidget(self.search_bar)
        containerLayout.addWidget(self._pdf_view)
        container.setLayout(containerLayout)
        self.setCentralWidget(container)


################################# Méthodes #################################


    def display_pdf(self, pdf_file_path: str) -> None:
        self._pdf_file_path = pdf_file_path
        self.pdf_doc.load(self._pdf_file_path)
        self._pdf_view.setDocument(self.pdf_doc)
