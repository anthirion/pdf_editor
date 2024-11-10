from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QGridLayout, QSpacerItem, QSizePolicy,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from GUI.resources import merge_icon
from global_variables import default_spacing


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.main_layout = QVBoxLayout(self)
        # ajouter de la marge en haut
        self.main_layout.addSpacing(default_spacing // 2)
        self.title_label, self.description_label = self.init_title_and_description()
        self.tools_grid = self.init_tools_grid()
        self.init_layout()

    def init_title_and_description(self):
        title_label = QLabel("Bienvenue dans PDF editor !")
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; qproperty-alignment: AlignCenter;")
        self.main_layout.addWidget(title_label)
        self.main_layout.addSpacing(default_spacing)

        description_label = QLabel(
            "Ce logiciel vous donne accès à plusieurs outils pour éditer vos fichiers PDF. Commencez avec nos outils les plus populaires :")
        description_label.setStyleSheet("qproperty-alignment: AlignCenter;")
        description_label.setWordWrap(True)
        return title_label, description_label

    def init_tools_grid(self):
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
            merge_icon,
            merge_icon,
            merge_icon,
            merge_icon,
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

        return tools_grid

    def init_layout(self):
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addSpacing(default_spacing * 2)
        self.main_layout.addLayout(self.tools_grid)
        # Ajouter un espace flexible en bas pour éviter que les éléments d'interface
        # ne prennent tout l'espace vertical disponible
        self.main_layout.addSpacerItem(QSpacerItem(20, 40,
                                                   QSizePolicy.Minimum,
                                                   QSizePolicy.Expanding,
                                                   )
                                       )
