import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy,
)
from PySide6.QtGui import QPixmap, QAction, QPalette, QColor
from PySide6.QtCore import Qt

from GUI.resources import (
    fusion_pdf_icon,
)
from GUI.menubar import MenuBar
from global_variables import default_spacing


class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        # Barre de menu
        self.menubar = MenuBar(parent=self)
        self.setMenuBar(self.menubar)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Définir la couleur de fond en blanc
        # palette = central_widget.palette()
        # palette.setColor(QPalette.window(), QColor("white"))
        # central_widget.setPalette(palette)

        # Barre latérale
        # sidebar = QWidget()
        # sidebar_layout = QVBoxLayout(sidebar)
        # sidebar_layout.addWidget(QPushButton("Accueil"))
        # # ajouter de la marge entre chaque bouton
        # sidebar_layout.addSpacing(default_spacing // 2)
        # sidebar_layout.addWidget(QPushButton("Ouvrir"))
        # # ajouter de la marge entre chaque bouton
        # sidebar_layout.addSpacing(default_spacing // 2)
        # sidebar_layout.addWidget(QPushButton("Nouveau"))
        # # ajouter de la marge entre chaque bouton
        # sidebar_layout.addSpacing(default_spacing // 2)
        # sidebar_layout.addStretch()
        # sidebar.setFixedWidth(150)
        # main_layout.addWidget(sidebar)

        # Contenu principal
        content = QWidget()
        content_layout = QVBoxLayout(content)
        # ajouter de la marge en haut
        content_layout.addSpacing(default_spacing // 2)

        welcome_label = QLabel("Bienvenue dans PDF editor !")
        welcome_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; qproperty-alignment: AlignCenter;")
        content_layout.addWidget(welcome_label)
        content_layout.addSpacing(default_spacing)

        description = QLabel(
            "Ce logiciel vous donne accès à plusieurs outils pour éditer vos fichiers PDF. Commencez avec nos outils les plus populaires :")
        description.setStyleSheet("qproperty-alignment: AlignCenter;")
        description.setWordWrap(True)
        content_layout.addWidget(description)
        content_layout.addSpacing(default_spacing*2)

        # Grille des outils
        tools_grid = QGridLayout()

        tools_name = ["Fusionner PDF",
                      "Diviser PDF",
                      "PDF en JPG",
                      "JPG en PDF",
                      ]

        tools_desc = [
            "Combinez plusieurs fichiers PDF en un seul document. Glissez-déposez les fichiers pour les réorganiser.",
            "Séparez un document PDF en plusieurs fichiers. Choisissez les pages ou définissez des intervalles pour la division.",
            "Convertissez vos pages PDF en images JPG. Idéal pour extraire des graphiques ou des images d'un document.",
            "Transformez vos images JPG en un fichier PDF. Parfait pour créer des documents à partir de vos photos."
        ]

        icons = [
            fusion_pdf_icon,
            fusion_pdf_icon,
            fusion_pdf_icon,
            fusion_pdf_icon,
        ]

        for i, tool in enumerate(zip(tools_name, tools_desc, icons)):
            tool_name, tool_desc, tool_icon = tool
            tool_widget = QWidget()
            tool_layout = QVBoxLayout(tool_widget)

            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(tool_icon)
                                 .scaled(42, 42, Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation))
            tool_layout.addWidget(icon_label)

            tool_label = QLabel(tool_name)
            tool_label.setStyleSheet("font-weight: bold;")
            tool_layout.addWidget(tool_label)

            desc_label = QLabel(tool_desc)
            desc_label.setWordWrap(True)
            tool_layout.addWidget(desc_label)

            tools_grid.addWidget(tool_widget, i // 2, i % 2)

        content_layout.addLayout(tools_grid)
        # Ajouter un espace flexible en bas pour éviter que les éléments d'interface
        # ne prennent tout l'espace vertical disponible
        content_layout.addSpacerItem(QSpacerItem(20, 40,
                                                 QSizePolicy.Minimum,
                                                 QSizePolicy.Expanding,
                                                 )
                                     )

        main_layout.addWidget(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec())
