# coding:utf-8
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

from qfluentwidgets import FolderListDialog, setTheme, Theme


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(800, 720)
        self.btn = QPushButton('Click Me', parent=self)
        self.btn.move(312, 300)
        self.btn.clicked.connect(self.showDialog)
        with open('resource/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

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
    w = Window()
    w.show()
    app.exec()
