# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QApplication, QWidget, QTreeWidgetItem, QHBoxLayout

from qfluentwidgets import TreeWidget, setTheme, Theme, TreeView


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)
        self.setStyleSheet("Demo{background:rgb(255,255,255)}")
        # setTheme(Theme.DARK)

        self.view = TreeView(self)
        model = QFileSystemModel()
        model.setRootPath('.')
        self.view.setModel(model)

        self.view.setBorderVisible(True)
        self.view.setBorderRadius(8)

        self.hBoxLayout.addWidget(self.view)
        self.hBoxLayout.setContentsMargins(50, 30, 50, 30)
        self.resize(800, 660)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec())
