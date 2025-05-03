import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class EditWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/editor_menu.ui', self)
        self.setFixedSize(self.size())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EditWindow()
    ex.show()
    sys.exit(app.exec())
