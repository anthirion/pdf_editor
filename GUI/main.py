from PySide6.QtWidgets import QApplication
from GUI.main_view import PDFEditorMainWindow

if __name__ == "__main__":
    app = QApplication([])
    window = PDFEditorMainWindow(app)
    window.show()
    app.exec()
