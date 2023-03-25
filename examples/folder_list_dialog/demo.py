# coding:utf-8
import sys
from PyQt6.QtWidgets import QApplication, QWidget

from qfluentwidgets import FolderListDialog, setTheme, Theme, PrimaryPushButton


class Demo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(800, 720)
        self.btn = PrimaryPushButton('Click Me', parent=self)
        self.btn.move(352, 300)
        self.btn.clicked.connect(self.showDialog)
        self.setStyleSheet('Demo{background:white}')

        # setTheme(Theme.DARK)

    def showDialog(self):
        folder_paths = ['D:/KuGou', 'C:/Users/shoko/Documents/Music']
        title = 'Build your collection from your local music files'
        content = "Right now, we're watching these folders:"
        w = FolderListDialog(folder_paths, title, content, self)
        w.folderChanged.connect(lambda x: print(x))
        w.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
