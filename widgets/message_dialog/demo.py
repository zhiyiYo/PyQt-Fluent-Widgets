# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

from message_dialog import MessageDialog


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(1000, 500)
        self.btn = QPushButton('点我', parent=self)
        self.btn.move(425, 25)
        self.btn.clicked.connect(self.showDialog)
        with open('resource/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def showDialog(self):
        content = '如果将"音乐"文件夹从音乐中移除，则该文件夹不会再出现在音乐中。'
        w = MessageDialog('删除此文件夹吗？', content, self)
        w.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
