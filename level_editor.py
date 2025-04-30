import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class EditWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("Редактор уровней")
        uic.loadUi('data/editor_menu.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EditWindow()
    ex.show()
    sys.exit(app.exec())
