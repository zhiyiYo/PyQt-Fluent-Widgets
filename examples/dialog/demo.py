# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

from qfluentwidgets import Dialog


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(1000, 500)
        self.btn = QPushButton('Click Me', parent=self)
        self.btn.move(425, 225)
        self.btn.clicked.connect(self.showDialog)
        with open('resource/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def showDialog(self):
        title = 'Are you sure you want to delete the folder?'
        content = """If you delete the "Music" folder from the list, the folder will no longer appear in the list, but will not be deleted."""
        w = Dialog(title, content, self)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
