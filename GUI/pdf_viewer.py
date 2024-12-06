from PySide6.QtCore import Slot, QTimer, Qt
from PySide6.QtPdf import QPdfDocument, QPdfSearchModel, QPdfLink, QPdfPageNavigator
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox
)


class PDFViewer(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.pdf_view = ZoomablePDFView(self)
        self._pdf_doc = QPdfDocument()
        self.search_model = QPdfSearchModel()
        self.search_model.setDocument(self._pdf_doc)
        self.pdf_view.setSearchModel(self.search_model)
        self.nav: QPdfPageNavigator = self.pdf_view.pageNavigator()

        # Ajout d'une barre de recherche
        self.search_bar = SearchBar(self)

        # Disposer les éléments les uns en dessous des autres
        pdf_layout = QVBoxLayout(self)
        pdf_layout.addWidget(self.search_bar)
        pdf_layout.addWidget(self.pdf_view)

    def display_pdf(self, pdf_file_path: str) -> None:
        self._pdf_doc.load(pdf_file_path)
        self.pdf_view.setDocument(self._pdf_doc)
        self.search_bar.page_count = self._pdf_doc.pageCount()

    def show_warning(self, message: str) -> None:
        """Affiche une boite de dialogue avec un message d'avertissement qui indique
        à l'utilisateur qu'il a atteint la limite de zoom/dézoom
        :message: message d'avertissement affiché à l'utilisateur
        """
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Avertissement")
        msg_box.setText(message)
        msg_box.exec()


class ZoomablePDFView(QPdfView):
    """
    Cette classe est une PDF view à laquelle est ajoutée une fonctionnalité de zoom
    avec la molette
    """
    ZOOM_STEP = 0.1
    ZOOM_UPPER_LIMIT = 2.1
    ZOOM_LOWER_LIMIT = 0.2
    ZOOM_INIT_LEVEL = 1.0
    TIMER_TIMEOUT = 100  # 100 ms

    def __init__(self, parent_window: PDFViewer) -> None:
        super().__init__()
        self._pdf_viewer = parent_window
        # affiche toutes les pages du pdf
        self.setPageMode(QPdfView.PageMode.MultiPage)
        # permet de focus via le clic de la souris
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.zoom_level = self.ZOOM_INIT_LEVEL
        self._warning_message = ""
        self.warning_timer = QTimer()
        self.set_timer()
        self.ctrl_pressed = False

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Control:
            self.ctrl_pressed = True
        event.accept()

    def keyReleaseEvent(self, event) -> None:
        self.ctrl_pressed = False
        event.accept()

    def wheelEvent(self, event) -> None:
        """Gérer le zoom avec la molette de la souris."""
        if self.ctrl_pressed:
            if event.angleDelta().y() > 0:  # Molette vers le haut
                self.zoom_in()
            else:  # Molette vers le bas
                self.zoom_out()
            event.accept()
        else:
            # Appeler l'implémentation par défaut si CTRL n'est pas enfoncé
            super().wheelEvent(event)

    def set_timer(self) -> None:
        """
        Lors de l'affichage d'un warning, les évènements ne sont plus pris en compte
        Ce timer permet de mettre en place un court délai avant l'affichage d'un message
        d'avertissement pour donner le temps à PyQt de capturer les évènements
        """
        self.warning_timer.setSingleShot(True)
        self.warning_timer.timeout.connect(self.show_zoom_warning)

    def zoom_in(self) -> None:
        if self.zoom_level < self.ZOOM_UPPER_LIMIT:  # limite pour ne pas trop zoomer
            self.zoom_level += self.ZOOM_STEP
            self.apply_zoom()
        else:
            # afficher un message d'avertissement pour avertir que l'utilisateur
            # ne peut plus zoomer davantage
            self._warning_message = "Vous avez atteint le niveau de zoom maximal"
            # attendre 100ms pour prendre en compte le relachement de la touche +
            self.warning_timer.start(self.TIMER_TIMEOUT)

    def zoom_out(self) -> None:
        if self.zoom_level > self.ZOOM_LOWER_LIMIT:  # limite pour ne pas trop dézoomer
            self.zoom_level -= self.ZOOM_STEP
            self.apply_zoom()
        else:
            # afficher un message d'avertissement pour avertir que l'utilisateur
            # ne peut plus dézoomer davantage
            self._warning_message = "Vous avez atteint le niveau de dézoom maximal"
            # attendre 100ms pour prendre en compte le relachement de la touche +
            self.warning_timer.start(self.TIMER_TIMEOUT)

    def reset_zoom(self) -> None:
        self.zoom_level = self.ZOOM_INIT_LEVEL
        self.apply_zoom()

    def apply_zoom(self) -> None:
        self.setZoomFactor(self.zoom_level)

    def show_zoom_warning(self) -> None:
        self._pdf_viewer.show_warning(self._warning_message)

    ############################# Réception de signaux #############################
    @Slot(int)
    def zoom_handler(self, signal_value: int) -> None:
        match signal_value:
            case 0:
                self.reset_zoom()
            case 1:
                self.zoom_in()
            case -1:
                self.zoom_out()
            case _:
                raise ValueError(
                    f"Le signal zoom_signal a envoyé la valeur incorrecte {signal_value}")


class SearchBar(QWidget):
    def __init__(self, parent_window: PDFViewer) -> None:
        super().__init__(parent_window)
        self._parent_window = parent_window
        self.pdf_view = parent_window.pdf_view
        self._pagenavigator = parent_window.nav
        self.search_model = parent_window.search_model

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
        self.page_count = 0
        self._text_to_search = ""
        # numéros de page où des résultats de recherche ont été trouvés
        self._text_locations: list[QPdfLink] = []
        self._current_location = 0

    def get_result(self, current_result: int) -> None:
        """
        Surligne le résultat courant et amène l'utilisateur à l'emplacement
        du résultat
        @param current_result: numéro du résultat à afficher
        """
        if self._text_locations and current_result < len(self._text_locations):
            self._pagenavigator.jump(self._text_locations[current_result])
            # surligne le résultat courant
            self.pdf_view.setCurrentSearchResultIndex(current_result)

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
    def toggle_search_bar(self) -> None:
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
            self.search_model.setSearchString(self._text_to_search)
            for page in range(self.page_count):
                self._text_locations.extend(
                    self.search_model.resultsOnPage(page))
        # aller directement à l'emplacement du premier résultat
        self.get_result(0)
