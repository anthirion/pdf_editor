from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox
)
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument, QPdfSearchModel, QPdfLink, QPdfPageNavigator
from PySide6.QtCore import Slot, Qt, QEvent
from PySide6.QtGui import QKeyEvent


class PDFViewer(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
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
        # Ajout d'une fonctionnalité de zoom avec la molette de la souris
        self.zoom_manager = ZoomManager(self._pdf_view)

        # Disposer les éléments les uns en dessous des autres
        container = QWidget()
        containerLayout = QVBoxLayout(self)
        containerLayout.addWidget(self.search_bar)
        containerLayout.addWidget(self._pdf_view)
        container.setLayout(containerLayout)
        self.setCentralWidget(container)

    def display_pdf(self, pdf_file_path: str) -> None:
        self._pdf_doc.load(pdf_file_path)
        self._pdf_view.setDocument(self._pdf_doc)
        self.search_bar._page_count = self._pdf_doc.pageCount()

    ############################# Gestion d'évènements #############################

    def event(self, event: QEvent) -> bool:
        if event.type() is QEvent.KeyPress:
            self.zoom_manager.key_pressed(event)
            if self.zoom_manager.should_zoom_in():
                self.zoom_manager.zoom_in()
            elif self.zoom_manager.should_zoom_out():
                self.zoom_manager.zoom_out()
        elif event.type() is QEvent.KeyRelease:
            self.zoom_manager.key_released(event)
        return False    # l'évènement n'est pas bloqué et remonte aux objets parents


class SearchBar(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._pdf_view = parent._pdf_view
        self._page_navigator = parent._nav
        self._search_model = parent._search_model

        # Création de la barre de recherche et des boutons
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher...")
        self.hide()  # Masquer la barre de recherche par défaut
        self.is_visible = False

        self.button_up = QPushButton("↑", self)
        self.button_down = QPushButton("↓", self)

        # Disposition en HBoxLayout
        layout = QHBoxLayout(self)
        layout.addWidget(self.search_input)
        layout.addWidget(self.button_up)
        layout.addWidget(self.button_down)

        # connecter les widgets à leurs slots
        self.connect_slots()
        # initialiser un certain nombre de variables utiles
        self.set_utils_attributes()

    def connect_slots(self) -> None:
        # pour éviter que les actions editingFinished et returnPressed ne
        # rentrent en conflit à la fin de la saisie, il n'est pas possible
        # de naviguer à travers les résultats en appuyant sur Entrée
        self.search_input.editingFinished.connect(self.edit_finished)
        self.button_up.clicked.connect(self.on_button_up_clicked)
        self.button_down.clicked.connect(self.on_button_down_clicked)

    def set_utils_attributes(self) -> None:
        """
        Initialise des attributs utiles à la recherche d'un mot
        """
        # nombre de pages du document chargé
        self._page_count = 0
        self._text_to_search = ""
        # numéros de page où des résultats de recherche ont été trouvés
        self._text_locations: list[QPdfLink] = []
        self._current_location = 0

    def show_warning(self, message: str) -> None:
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Avertissement")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def get_result(self, current_result: int) -> None:
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
    def on_button_up_clicked(self) -> None:
        self._current_location -= 1
        self.get_result(self._current_location)

    @Slot()
    def on_button_down_clicked(self) -> None:
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
    def edit_finished(self) -> None:
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


class ZoomManager:
    def __init__(self, pdf_view) -> None:
        self._pdf_view = pdf_view
        self.zoom_level = 1.0  # Niveau de zoom initial
        self._ctrl_pressed = False
        self._plus_pressed = False
        self._minus_pressed = False

    def should_zoom_in(self) -> bool:
        return self._ctrl_pressed and self._plus_pressed

    def should_zoom_out(self) -> bool:
        return self._ctrl_pressed and self._minus_pressed

    def zoom_in(self) -> None:
        """
        Augmente le niveau de zoom
        [ATTENTION] Toujours vérifier que le zoom doit être fait
        avec la fonction should_zoom_in
        """
        if self.zoom_level < 2.1:   # limite pour ne pas trop zoomer
            self.zoom_level += 0.1
            self._apply_zoom()

    def zoom_out(self) -> None:
        """
        Diminue le niveau de zoom
        [ATTENTION] Toujours vérifier que le dézoom doit être fait
        avec la fonction should_zoom_out
        """
        if self.zoom_level > 0.2:   # limite pour ne pas trop dézoomer
            self.zoom_level -= 0.1
            self._apply_zoom()

    def reset_zoom(self) -> None:
        """ Remet le zoom au niveau normal   """
        self.zoom_level = 1.0
        self._apply_zoom()

    def _apply_zoom(self) -> None:
        """ Applique le niveau de zoom au QPdfView."""
        self._pdf_view.setZoomFactor(self.zoom_level)

    ############################# Gestion d'évènements #############################

    def key_pressed(self, event: QKeyEvent) -> None:
        if (event.key() == Qt.Key_Control):
            self._ctrl_pressed = True
        elif (event.text() == '+'):
            self._plus_pressed = True
        elif (event.text() == '-'):
            self._minus_pressed = True

    def key_released(self, event: QKeyEvent) -> None:
        if (event.key() == Qt.Key_Control):
            self._ctrl_pressed = False
        elif (event.text() == '+'):
            self._plus_pressed = False
        elif (event.text() == '-'):
            self._minus_pressed = False
