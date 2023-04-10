# coding:utf-8
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QFrame, QTreeWidgetItem, QHBoxLayout, QTreeWidgetItemIterator
from qtfluentwidgets import TreeWidget

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.style_sheet import StyleSheet


class ViewInterface(GalleryInterface):
    """ View interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.view,
            subtitle="qtfluentwidgets.components.widgets",
            parent=parent
        )

        frame = TreeFrame(self)
        self.addExampleCard(
            title=self.tr('A simple TreeView'),
            widget=frame,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/tree_view/demo.py'
        )

        frame = TreeFrame(self, True)
        self.addExampleCard(
            title=self.tr('A TreeView with Multi-selection enabled'),
            widget=frame,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/tree_view/demo.py'
        )



class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)


class TreeFrame(Frame):

    def __init__(self, parent=None, enableCheck=False):
        super().__init__(parent)
        self.tree = TreeWidget(self)
        self.addWidget(self.tree)

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
        ])
        item2.addChild(item21)
        self.tree.addTopLevelItem(item2)
        self.tree.expandAll()
        self.tree.setHeaderHidden(True)

        self.setFixedSize(300, 380)

        if enableCheck:
            it = QTreeWidgetItemIterator(self.tree)
            while(it.value()):
                it.value().setCheckState(0, Qt.Unchecked)
                it += 1
