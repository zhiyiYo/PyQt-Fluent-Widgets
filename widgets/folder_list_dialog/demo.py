# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

from folder_list_dialog import FolderListDialog


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(1000, 800)
        self.btn = QPushButton('点我', parent=self)
        self.btn.move(425, 375)
        self.btn.clicked.connect(self.showDialog)
        self.btn.setObjectName('btn')
        with open('resource/style/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def showDialog(self):
        folder_paths = ['D:/KuGou', 'C:/Users/shoko/Documents/音乐']
        title = '从本地曲库创建个人"收藏"'
        content = '现在我们正在查看这些文件夹:'
        w = FolderListDialog(folder_paths, title, content, self)
        w.folderChanged.connect(lambda x: print(x))
        w.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
