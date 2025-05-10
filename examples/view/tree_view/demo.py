# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidgetItem, QFileSystemModel, QHBoxLayout

from qfluentwidgets import TreeWidget, setTheme, Theme, TreeView


class Demo(QWidget):

    def __init__(self, parent=None, enableCheck=False):
        super().__init__(parent)

        self.tree = TreeWidget(self)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)
        self.hBoxLayout.addWidget(self.tree)

        item1 = QTreeWidgetItem([self.tr('JoJo 1 - Phantom Blood')])
        item1.addChildren([
            QTreeWidgetItem([self.tr('Jonathan Joestar')]),
            QTreeWidgetItem([self.tr('Dio Brando')]),
            QTreeWidgetItem([self.tr('Will A. Zeppeli')]),
        ])
        self.tree.addTopLevelItem(item1)

        item2 = QTreeWidgetItem([self.tr('JoJo 3 - Stardust Crusaders')])
        item21 = QTreeWidgetItem([self.tr('Jotaro Kujo')])
        item21.addChildren([
            QTreeWidgetItem(['空条承太郎']),
            QTreeWidgetItem(['空条蕉太狼']),
            QTreeWidgetItem(['阿强']),
            QTreeWidgetItem(['卖鱼强']),
            QTreeWidgetItem(['那个无敌的男人']),
        ]*10)
        item22 = QTreeWidgetItem([self.tr('Jotaro Kujo')])
        item22.addChildren([
            QTreeWidgetItem(['空条承太郎']),
            QTreeWidgetItem(['空条蕉太狼']),
            QTreeWidgetItem(['阿强']),
            QTreeWidgetItem(['卖鱼强']),
            QTreeWidgetItem(['那个无敌的男人']),
        ]*10)
        item23 = QTreeWidgetItem([self.tr('Jotaro Kujo')])
        item23.addChildren([
            QTreeWidgetItem(['空条承太郎']),
            QTreeWidgetItem(['空条蕉太狼']),
            QTreeWidgetItem(['阿强']),
            QTreeWidgetItem(['卖鱼强']),
            QTreeWidgetItem(['那个无敌的男人']),
        ]*10)
        item2.addChild(item21)
        item2.addChild(item22)
        item2.addChild(item23)

        self.tree.addTopLevelItem(item2)
        self.tree.expandAll()
        self.tree.setHeaderHidden(True)

        self.resize(400, 500)



if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec_())
