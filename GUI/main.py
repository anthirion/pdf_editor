from PySide6.QtWidgets import QApplication
from GUI.homepage import HomePage

app = QApplication([])
window = HomePage()
window.show()
app.exec()
