# coding:utf-8
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QColor, QPalette
from PyQt6.QtWidgets import QTreeWidget, QStyledItemDelegate, QStyle, QTreeView, QApplication

from ...common.style_sheet import FluentStyleSheet, themeColor, isDarkTheme, setCustomStyleSheet
from ...common.font import getFont
from .scroll_area import SmoothScrollDelegate


class TreeItemDelegate(QStyledItemDelegate):
    """ Tree item delegate """

    def __init__(self, parent: QTreeView):
        super().__init__(parent)

    def paint(self, painter, option, index):
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        super().paint(painter, option, index)

        if not (option.state & (QStyle.StateFlag.State_Selected | QStyle.StateFlag.State_MouseOver)):
            return

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)

        # draw background
        h = option.rect.height() - 4
        c = 255 if isDarkTheme() else 0
        painter.setBrush(QColor(c, c, c, 9))
        painter.drawRoundedRect(
            4, option.rect.y() + 2, self.parent().width() - 8, h, 4, 4)

        # draw indicator
        if option.state & QStyle.StateFlag.State_Selected and self.parent().horizontalScrollBar().value() == 0:
            painter.setBrush(themeColor())
            painter.drawRoundedRect(4, 9+option.rect.y(), 3, h - 13, 1.5, 1.5)

        painter.restore()

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        # font
        option.font = index.data(Qt.ItemDataRole.FontRole) or getFont(13)

        # text color
        textColor = Qt.GlobalColor.white if isDarkTheme() else Qt.GlobalColor.black
        textBrush = index.data(Qt.ItemDataRole.ForegroundRole)
        if textBrush is not None:
            textColor = textBrush.color()

        option.palette.setColor(QPalette.ColorRole.Text, textColor)
        option.palette.setColor(QPalette.ColorRole.HighlightedText, textColor)


class TreeViewBase:
    """ Tree view base class """

    def __init__(self, *args, **kwargs):
        self.scrollDelagate = SmoothScrollDelegate(self)

        self.header().setHighlightSections(False)
        self.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setItemDelegate(TreeItemDelegate(self))
        self.setIconSize(QSize(16, 16))

        FluentStyleSheet.TREE_VIEW.apply(self)

    def drawBranches(self, painter, rect, index):
        rect.moveLeft(15)
        return QTreeView.drawBranches(self, painter, rect, index)

    def setBorderVisible(self, isVisible: bool):
        """ set the visibility of border """
        self.setProperty("isBorderVisible", isVisible)
        self.setStyle(QApplication.style())

    def setBorderRadius(self, radius: int):
        """ set the radius of border """
        qss = f"QTreeView{{border-radius: {radius}px}}"
        setCustomStyleSheet(self, qss, qss)


class TreeWidget(QTreeWidget, TreeViewBase):
    """ Tree widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)


class TreeView(QTreeView, TreeViewBase):
    """ Tree view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
