from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox
)
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument, QPdfSearchModel, QPdfLink, QPdfPageNavigator
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon

from GUI.resources import arrow_up_icon, arrow_down_icon


class PDFViewer(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._pdf_view = QPdfView()
        # affiche toutes les pages du pdf
        self._pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self._pdf_doc = QPdfDocument()
        self._search_model = QPdfSearchModel()
        self._search_model.setDocument(self._pdf_doc)
        self._pdf_view.setSearchModel(self._search_model)
        self._nav: QPdfPageNavigator = self._pdf_view.pageNavigator()
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

    def display_pdf(self, pdf_file_path: str):
        self._pdf_doc.load(pdf_file_path)
        self._pdf_view.setDocument(self._pdf_doc)
        self.search_bar._page_count = self._pdf_doc.pageCount()


class SearchBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._pdf_view = parent._pdf_view
        self._page_navigator = parent._nav
        self._search_model = parent._search_model

        # Création de la barre de recherche et des boutons
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher...")
        self.hide()  # Masquer la barre de recherche par défaut
        self.is_visible = False

        self.button_up = QPushButton(QIcon(arrow_up_icon), "")
        self.button_down = QPushButton(QIcon(arrow_down_icon), "")

        # Disposition en HBoxLayout
        layout = QHBoxLayout(self)
        layout.addWidget(self.search_input)
        layout.addWidget(self.button_up)
        layout.addWidget(self.button_down)

        # connecter les widgets à leurs slots
        self.connect_slots()
        # initialiser un certain nombre de variables utiles
        self.set_utils_attributes()

    def connect_slots(self):
        # pour éviter que les actions editingFinished et returnPressed ne
        # rentrent en conflit à la fin de la saisie, il n'est pas possible
        # de naviguer à travers les résultats en appuyant sur Entrée
        self.search_input.editingFinished.connect(self.edit_finished)
        self.button_up.clicked.connect(self.on_button_up_clicked)
        self.button_down.clicked.connect(self.on_button_down_clicked)

    def set_utils_attributes(self):
        """
        Initialise des attributs utiles à la recherche d'un mot
        """
        # nombre de pages du document chargé
        self._page_count = 0
        self._text_to_search = ""
        # numéros de page où des résultats de recherche ont été trouvés
        self._text_locations: list[QPdfLink] = []
        self._current_location = 0

    def show_warning(self, message: str):
        # Créer et configurer la boîte de dialogue d'avertissement
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Avertissement")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        # Afficher la boîte de dialogue
        msg_box.exec()

    def get_result(self, current_result: int):
        """
        Surligne le résultat courant et amène l'utilisateur à l'emplacement
        du résultat
        @param current_result: numéro du résultat à afficher
        """
        if not self._text_locations:
            self.show_warning("Aucun résultat trouvé")
        elif current_result < len(self._text_locations):
            self._page_navigator.jump(self._text_locations[current_result])
            # surligne le résultat courant
            self._pdf_view.setCurrentSearchResultIndex(current_result)

    ################################# Slots #################################

    @Slot()
    def on_button_up_clicked(self):
        if (self._page_navigator.backAvailable):
            self._current_location -= 1
            # breakpoint()
            self.get_result(self._current_location)

    @Slot()
    def on_button_down_clicked(self):
        if (self._page_navigator.forwardAvailable):
            self._current_location += 1
            self.get_result(self._current_location)

    @Slot()
    def toggle_search_bar(self):
        if self.is_visible:
            self.hide()
            self.is_visible = False
        else:
            self.show()
            self.search_input.setFocus()
            self.is_visible = True

    @Slot()
    def edit_finished(self):
        """
        Lorsque l'utilisateur écrit un mot dans la barre de recherche,
        rechercher toutes les occurences du mot dans le fichier
        """
        self._text_locations.clear()
        self._current_location = 0
        self._text_to_search = self.search_input.text()
        if self._text_to_search:
            self._search_model.setSearchString(self._text_to_search)
            for page in range(self._page_count):
                self._text_locations.extend(
                    self._search_model.resultsOnPage(page))
        # aller directement à l'emplacement du premier résultat
        self.get_result(0)
