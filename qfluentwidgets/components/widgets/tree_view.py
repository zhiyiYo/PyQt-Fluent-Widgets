# coding:utf-8
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget, QTreeWidget, QStyledItemDelegate, QStyle, QTreeView

from ...common.style_sheet import FluentStyleSheet, themeColor, isDarkTheme
from ...common.smooth_scroll import SmoothScroll


class TreeItemDelegate(QStyledItemDelegate):
    """ Tree item delegate """

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
        if option.state & QStyle.State_Selected:
            painter.setBrush(themeColor())
            painter.drawRoundedRect(4, 9+option.rect.y(), 3, h - 13, 1.5, 1.5)

        painter.restore()


class TreeWidget(QTreeWidget):
    """ Tree widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.verticalSmoothScroll = SmoothScroll(self, Qt.Vertical)
        self.horizonSmoothScroll = SmoothScroll(self, Qt.Horizontal)

        self.setItemDelegate(TreeItemDelegate(self))
        self.setIconSize(QSize(16, 16))
        FluentStyleSheet.TREE_VIEW.apply(self)

    def drawBranches(self, painter, rect, index):
        rect.moveLeft(15)
        return super().drawBranches(painter, rect, index)

    def wheelEvent(self, e):
        if e.modifiers() == Qt.NoModifier:
            self.verticalSmoothScroll.wheelEvent(e)
        else:
            self.horizonSmoothScroll.wheelEvent(e)


class TreeView(QTreeView):
    """ Tree view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.verticalSmoothScroll = SmoothScroll(self, Qt.Vertical)
        self.horizonSmoothScroll = SmoothScroll(self, Qt.Horizontal)

        self.setItemDelegate(TreeItemDelegate(self))
        self.setIconSize(QSize(16, 16))
        FluentStyleSheet.TREE_VIEW.apply(self)
        FluentStyleSheet.TREE_VIEW.apply(self.verticalScrollBar())

    def drawBranches(self, painter, rect, index):
        rect.moveLeft(15)
        return super().drawBranches(painter, rect, index)

    def wheelEvent(self, e):
        if e.modifiers() == Qt.NoModifier:
            self.verticalSmoothScroll.wheelEvent(e)
        else:
            self.horizonSmoothScroll.wheelEvent(e)
