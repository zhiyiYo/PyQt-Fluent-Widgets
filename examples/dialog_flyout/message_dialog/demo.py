# coding:utf-8
import sys
from PyQt6.QtWidgets import QApplication, QWidget

from qfluentwidgets import MessageDialog, MessageBox, setTheme, Theme, PrimaryPushButton


class Demo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(1000, 500)
        self.btn = PrimaryPushButton('Click Me', parent=self)
        self.btn.move(455, 25)
        self.btn.clicked.connect(self.showDialog)
        self.setStyleSheet('Demo{background:white}')

        # setTheme(Theme.DARK)

    def showDialog(self):
        title = 'Are you sure you want to delete the folder?'
        content = """If you delete the "Music" folder from the list, the folder will no longer appear in the list, but will not be deleted."""
        # w = MessageDialog(title, content, self)   # Win10 style message box
        w = MessageBox(title, content, self)

        # close the message box when mask is clicked
        w.setClosableOnMaskClicked(True)

        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
