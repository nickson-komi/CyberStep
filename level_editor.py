import sys
from connecting import loading_maps, save_results, save_maps
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class EditWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/editor_menu.ui', self)
        self.check_passing.setCheckState(Qt.CheckState.Checked)
        self.setFixedSize(self.size())
        self.mapsBox.currentTextChanged.connect(self.combo_selection)
        self.maps = loading_maps(self.path_file.text())
        self.combo_update()
        self.current_id = -1
        self.save_but.clicked.connect(self.save_map)

    def combo_update(self):
        self.mapsBox.clear()
        for n, name in enumerate([x['name'] for x in self.maps], start=1):
            self.mapsBox.addItem(f'{n} --- {name}')

    def combo_selection(self):
        num = int(self.mapsBox.currentText().split('---')[0].strip()) - 1
        self.current_id = self.maps[num]['id']
        self.map_name.setText(self.maps[num]['name'])
        if not self.maps[num]['status']:
            self.check_passing.setChecked(False)
        else:
            self.check_passing.setChecked(True)

        self.levelMapTable.setColumnCount(10)
        self.levelMapTable.setRowCount(10)
        for i, row in enumerate(self.maps[num]['texture'].split('\n')):
            self.levelMapTable.setColumnWidth(i, 10)
            self.levelMapTable.setRowHeight(i, 10)
            for j, elem in enumerate(row.split('-')):
                self.levelMapTable.setItem(i, j, QTableWidgetItem(str(elem)))

    def save_map(self):
        for row in range(self.levelMapTable.rowCount()):
            for cols in range(self.levelMapTable.columnCount()):
                print(self.levelMapTable.itemAt(row, cols).text(), end=' ')
            print()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EditWindow()
    ex.show()
    sys.exit(app.exec())
