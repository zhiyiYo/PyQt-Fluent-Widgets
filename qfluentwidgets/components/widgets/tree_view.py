# coding:utf-8
import typing

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget, QTreeWidget, QStyledItemDelegate, QStyle, QTreeView

from ...common.style_sheet import FluentStyleSheet, themeColor, isDarkTheme
from .scroll_area import SmoothScrollDelegate


class TreeItemDelegate(QStyledItemDelegate):
    """ Tree item delegate """

    def __init__(self, parent: QTreeView):
        super().__init__(parent)

    def paint(self, painter, option, index):
        painter.setRenderHints(
            QPainter.Antialiasing | QPainter.TextAntialiasing)
        super().paint(painter, option, index)

        if not (option.state & (QStyle.State_Selected | QStyle.State_MouseOver)):
            return

        painter.save()
        painter.setPen(Qt.NoPen)

        # draw background
        h = option.rect.height() - 4
        c = 255 if isDarkTheme() else 0
        painter.setBrush(QColor(c, c, c, 9))
        painter.drawRoundedRect(
            4, option.rect.y() + 2, self.parent().width() - 8, h, 4, 4)

        # draw indicator
        if option.state & QStyle.State_Selected and self.parent().horizontalScrollBar().value() == 0:
            painter.setBrush(themeColor())
            painter.drawRoundedRect(4, 9+option.rect.y(), 3, h - 13, 1.5, 1.5)

        painter.restore()


class TreeViewBase:
    """ Tree view base class """

    def _initView(self):
        self.scrollDelagate = SmoothScrollDelegate(self)

        self.setHorizontalScrollMode(QTreeView.ScrollPerPixel)
        self.setVerticalScrollMode(QTreeView.ScrollPerPixel)
        self.setItemDelegate(TreeItemDelegate(self))
        self.setIconSize(QSize(16, 16))

        FluentStyleSheet.TREE_VIEW.apply(self)
        FluentStyleSheet.TREE_VIEW.apply(self.verticalScrollBar())
        FluentStyleSheet.TREE_VIEW.apply(self.horizontalScrollBar())

    def drawBranches(self, painter, rect, index):
        rect.moveLeft(15)
        return QTreeView.drawBranches(self, painter, rect, index)


class TreeWidget(TreeViewBase, QTreeWidget):
    """ Tree widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initView()


class TreeView(TreeViewBase, QTreeView):
    """ Tree view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initView()
