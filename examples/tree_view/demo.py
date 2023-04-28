# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QTreeWidgetItem, QFileSystemModel, QHBoxLayout

from qfluentwidgets import TreeWidget, setTheme, Theme, TreeView


class Demo(QWidget):
    """ 树形控件演示 """

    def __init__(self):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)
        self.setStyleSheet("Demo{background:rgb(255,255,255)}")
        # setTheme(Theme.DARK)

        self.view = TreeView(self)
        model = QFileSystemModel()
        model.setRootPath('.')
        self.view.setModel(model)

        self.hBoxLayout.addWidget(self.view)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.resize(700, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec())
